# Phase 25: 생산라인 실시간 진행 (경과시간 추산 + 조회 화면 전용 스레드)

계층: model + controller + view

## 배경

Phase 9/10에서 `ProductionQueue.produce_unit()`은 "물리적으로 1개 생산 완료"를 나타내지만, 콘솔 앱엔 시계/타이머가 없어서 실제로 그 호출을 대신 트리거해줄 것이 없다. 라인 배정(유휴 라인에 대기작업 넣기, Phase8/19)은 이미 자동이지만, 배정된 이후 "시간이 지남에 따라 실제로 몇 개 만들어졌는지"는 아무도 계산해주지 않는다.

결정된 방식: 실제 경과시간(wall-clock)을 추산해 그만큼 `produce_unit()`을 몰아서 호출("따라잡기"). 상시 백그라운드 스레드는 두지 않고, 사용자가 "생산라인 조회" 화면에 들어가 있는 동안만 스레드를 돌려 화면을 갱신하고, 화면을 나가면 스레드를 종료한다. 이렇게 하면 생산 진행은 오직 그 화면이 열려있는 동안에만(그리고 그 스레드 하나만) 상태를 바꾸므로, 파일 동시쓰기 경합이나 다른 화면과의 레이스 컨디션을 피할 수 있다.

## 목표

`ProductionJob`이 라인에 배정된 실제 시각을 기록하고, "생산라인 조회" 화면에서 그 이후 경과시간만큼 생산이 진행된 것으로 계산해 실시간처럼 보이게 한다.

## 설계

- `model/production_job.py`: `ProductionJob.__init__`에 `started_at: float | None = None` 필드 추가 (기본값 `None`, 아직 라인 배정 전 상태).
- `model/production_queue.py`: `assign_idle_lines()`가 대기작업을 라인에 배정하는 시점에 `job.started_at = time.time()`을 설정한다. (`produce_unit`은 그대로 두되, `job.started_at`이 없는 job에 대해 호출되면 안 되므로 — 배정 시점에 반드시 세팅되게 함.)
- `controller/production_line_controller.py`에 추가:
  - `tick(self, inventory_repo) -> list`: `queue.lines`의 각 job에 대해 `경과시간 = time.time() - job.started_at`, `단위당시간 = job.total_production_time / job.actual_qty`, `목표생산량 = min(job.actual_qty, floor(경과시간 / 단위당시간))`을 계산. `job.produced_qty`가 목표생산량에 도달할 때까지 `queue.produce_unit(line_index, inventory)`를 반복 호출한다 (job의 `sample_id`에 해당하는 `Inventory`를 `inventory_repo.find_by_sample_id`로 불러오고, 호출 후 `inventory_repo.save`로 저장). 이번 호출로 확정된(confirmed) `ProductionJob` 목록을 모아 반환한다 — 호출자(view)가 "OO 주문 CONFIRMED" 안내를 띄울 수 있게.
  - 이 메서드는 라인이 이미 완료돼 비었으면(`None`) 건너뛴다.
- `view/console_view.py` + `controller/main_controller.py`: "생산라인 조회"를 선택하면
  1. 별도 스레드를 시작해 0.5초 간격으로 `production_line_controller.tick(inventory_repo)` 호출 + 현재 라인/대기열 상태를 화면에 다시 그림.
  2. 메인 스레드는 사용자의 Enter 입력을 기다린다(그동안 화면은 스레드가 갱신).
  3. Enter를 누르면 스레드 종료 신호(`threading.Event`)를 보내고 `join()`한 뒤 메뉴로 복귀.
- **예상완료시각 표시**: 별도 타이머 없이, `job.started_at + job.total_production_time`이 곧 완료 예정 시각(epoch)이다 — 라인 화면을 그릴 때마다 이 고정값을 `datetime.fromtimestamp()`로 사람이 읽을 수 있는 시각으로 변환해 보여준다. 진행률(%)도 같은 방식으로 `(현재시각 - started_at) / total_production_time`을 매 갱신마다 다시 계산할 뿐, 별도 시계 상태를 추적할 필요 없다.

## 엣지 케이스

- 화면을 여러 번 들어갔다 나갔다 해도 각 진입마다 새 스레드 하나만 존재해야 한다 (이전 스레드가 확실히 종료된 뒤 새로 시작).
- 경과시간이 이미 완료 시점을 넘었다면(오래 보다가 다시 들어온 경우 등) 목표생산량은 `actual_qty`로 캡되어 한 번에 완료까지 처리된다.

## 완료 조건

- [ ] `job.started_at`이 `assign_idle_lines()` 시점에 설정되는지 테스트
- [ ] `tick()`이 경과시간에 비례해 `produce_unit()`을 반복 호출하고, 완료/확정된 job을 올바르게 반환하는지 테스트 (실제 `time.sleep` 없이, `started_at`을 과거 시각으로 세팅해 결정론적으로 검증)
- [ ] `python main.py`로 "생산라인 조회" 화면 진입 시 실시간으로 진행률이 올라가고, 화면을 나가면 스레드가 정리되는지 수동 확인
