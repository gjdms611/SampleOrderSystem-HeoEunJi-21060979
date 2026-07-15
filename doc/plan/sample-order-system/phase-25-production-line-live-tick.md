# Phase 25: 생산라인 실시간 진행 (경과시간 추산 + 조회 화면 전용 스레드)

계층: model + controller + view

## 배경

Phase 9/10에서 `ProductionQueue.produce_unit()`은 "물리적으로 1개 생산 완료"를 나타내지만, 콘솔 앱엔 시계/타이머가 없어서 실제로 그 호출을 대신 트리거해줄 것이 없다. 라인 배정(유휴 라인에 대기작업 넣기, Phase8/19)은 이미 자동이지만, 배정된 이후 "시간이 지남에 따라 실제로 몇 개 만들어졌는지"는 아무도 계산해주지 않는다. 지금까지는 이 Phase를 "Textual 전환에 흡수"로 보류했으나, 사용자가 지금 콘솔 구조에서 바로 필요로 해서 보류를 해제하고 진행한다.

결정된 방식: 실제 경과시간(wall-clock)을 추산해 그만큼 `produce_unit()`을 몰아서 호출("따라잡기"). 상시 백그라운드 스레드는 두지 않고, 사용자가 "생산라인 조회" 화면에 들어가 있는 동안만 스레드를 돌려 화면을 갱신하고, 화면을 나가면 스레드를 종료한다.

## 목표 (사용자 요구사항 반영, 최종 확정)

"생산라인 조회" 화면에서:
- 생산라인 총 개수와 현재 시각을 보여준다.
- 각 라인의 상태(작업이 있으면 RUNNING, 없으면 IDLE)를 보여준다.
- 처리중(RUNNING) 라인마다: 주문번호 / 시료정보(이름) / 주문량 / 현재 재고 / 부족분 / 실생산량 / 수율 / 진행률 / 예상완료시각.
- 대기중(FIFO) 목록: 순서 / 주문번호 / 시료 / 주문량 / 부족분 / 실생산량 / 예상완료시각(라인에 배정된 시점부터 계산 가능한 것만 — 아직 배정 안 된 대기 작업은 시작시각이 없으므로 예상완료시각을 "대기중"으로 표시).
- 화면 진입 시점에 경과시간만큼 `tick()`으로 한 번 따라잡기 계산한 뒤, 그 시점의 스냅샷(진행률 포함)을 정적으로 보여준다. 실시간 갱신(스레드)은 사용해보니 콘솔 입력 프롬프트와 뒤섞여 화면이 지저분해 보이는 문제가 있어 제거하고, 조회할 때마다 새로 계산하는 정적 스냅샷으로 확정한다.
- 생산이 완료되어 CONFIRMED로 전환된 주문은 화면 진입 시점의 `tick()` 호출로 즉시 반영된다 (`OrderController.complete_production()` 연동).

## 단계 구성 (Phase가 크므로 하위 RED-GREEN 사이클로 쪼갬)

### 25-A: ProductionJob 시작시각 기록 (model)
- `model/production_job.py`: `ProductionJob.__init__`에 `started_at: float | None = None` 필드 추가.
- `model/production_queue.py`: `assign_idle_lines()`가 대기작업을 라인에 배정하는 시점에 `job.started_at = time.time()`을 설정한다.

### 25-B: 경과시간 기반 tick + 주문 완료 연동 (controller)
- `controller/production_line_controller.py`에 `tick(self, inventory_repo, order_controller) -> list` 추가:
  - `queue.lines`의 각 job(있는 것만)에 대해 `경과시간 = time.time() - job.started_at`, `단위당시간 = job.total_production_time / job.actual_qty`, `목표생산량 = min(job.actual_qty, floor(경과시간 / 단위당시간))`을 계산.
  - `job.produced_qty`가 목표생산량에 도달할 때까지 `queue.produce_unit(line_index, inventory)`를 반복 호출 (job의 `sample_id`에 해당하는 `Inventory`를 `inventory_repo.find_by_sample_id`로 불러오고, 호출 후 `inventory_repo.save`로 저장).
  - 이번 호출로 confirmed된 `ProductionJob` 목록이 생기면, `order_controller.complete_production(confirmed_jobs)`를 호출해 실제 `Order` 상태까지 CONFIRMED로 반영한다 (지금까지는 이 연동이 없어서 생산완료 후에도 Order.status가 PRODUCING에 머무는 공백이 있었다 — 이 Phase에서 메운다).
  - confirmed된 `Order` 목록을 반환한다 (view가 "OO 주문 CONFIRMED" 안내를 띄울 수 있게).

### 25-C: 생산라인 조회 상세 정보 조합 (controller)
- `ProductionLineController`에 필요한 조회 정보를 조합하는 메서드를 추가한다 (예: `describe_current(self, order_repo, sample_repo, inventory_repo) -> list[dict]`, `describe_waiting(self, order_repo, sample_repo) -> list[dict]`):
  - 처리중 라인마다: `order_repo.find_by_id(job.order_id)`(주문량), `sample_repo.find_by_id(job.sample_id)`(이름/수율), `inventory_repo.find_by_sample_id(job.sample_id)`(현재 재고)를 조회해 job의 `shortage`/`actual_qty`/`produced_qty`/`started_at`/`total_production_time`과 함께 하나의 표시용 구조로 묶는다. 진행률과 예상완료시각(`datetime.fromtimestamp(job.started_at + job.total_production_time)`)도 이 메서드가 계산해 포함시킨다.
  - 대기중 목록도 같은 방식으로 순서(도착순 인덱스) / 주문번호 / 시료 / 주문량 / 부족분 / 실생산량을 묶는다 (아직 `started_at`이 없으므로 예상완료시각은 없음/"대기중"으로 표시).
  - 라인 상태(RUNNING/IDLE)와 총 라인 개수는 `queue.lines`(길이 = 라인 개수, 각 요소가 `None`이면 IDLE, job이 있으면 RUNNING)로 바로 판단 가능 — 별도 저장 상태 불필요.

### 25-D: 조회 화면 정적 스냅샷 출력 (view + main_controller) — 스레드 방식 폐기, 정적 스냅샷으로 변경
- `view/console_view.py`에 조합된 정보를 표로 그리는 함수(`show_production_line_screen`) 추가 (라인별 상태 요약 + 현재시각 + 처리중 상세 표 + 대기중 상세 표).
- `controller/main_controller.py`의 "생산라인 조회" 처리: 화면 진입 시 `tick()` 한 번 호출 → `describe_current`/`describe_waiting` 조회 → 화면 출력 → 바로 메뉴로 복귀. 백그라운드 스레드/자동 재갱신 없음.
- (변경 이력) 최초 구현은 0.5초 간격으로 재조회/재렌더링하는 스레드를 두고 Enter 입력까지 대기하는 방식이었으나, 실제로 써보니 스레드 출력과 입력 프롬프트가 뒤섞여 화면이 지저분해지는 문제가 있어 폐기하고 정적 스냅샷 방식으로 확정했다.

## 엣지 케이스

- 화면을 여러 번 들어갔다 나갔다 해도 각 진입마다 새 스레드 하나만 존재해야 한다.
- 경과시간이 이미 완료 시점을 넘었다면 목표생산량은 `actual_qty`로 캡되어 한 번에 완료까지 처리된다.
- 라인이 비어있으면(`job is None`) 그 라인은 IDLE로만 표시하고 tick/조합 대상에서 제외한다.
- 대기중 작업은 아직 `started_at`이 없으므로 예상완료시각을 계산하지 않는다(라인 배정 후에만 의미가 있음).

## 완료 조건

- [x] (25-A) `job.started_at`이 `assign_idle_lines()` 시점에 설정되는지 테스트
- [x] (25-B) `tick()`이 경과시간에 비례해 `produce_unit()`을 반복 호출하고, 완료된 job에 대해 `order_controller.complete_production()`까지 연동되어 Order.status가 CONFIRMED로 바뀌는지 테스트 (`time.sleep` 없이 `started_at`을 과거로 세팅해 결정론적으로 검증)
- [x] (25-C) 처리중/대기중 목록 조합 메서드가 요구된 필드(주문번호/시료정보/주문량/재고/부족분/실생산량/수율/진행률/예상완료시각 등)를 정확히 채우는지 테스트
- [x] (25-D) `python main.py`로 "생산라인 조회" 진입 시 라인개수/상태/현재시각/처리중 상세/대기중 상세가 그 시점 스냅샷으로 보이는지 수동 확인 (스레드 자동 갱신 없이 조회할 때마다 재계산)
