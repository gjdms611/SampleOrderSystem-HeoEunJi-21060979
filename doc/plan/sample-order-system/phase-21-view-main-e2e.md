# Phase 21: 메인 메뉴 5종 콘솔 + 조립 + E2E

계층: view + main

## 배경

Phase 22(임시 실행 골격)는 메뉴 구조를 PRD와 다르게 임시로 나눴었다(1.시료관리 2.주문접수/거절/취소 3.주문승인 4.출고+모니터링+생산라인(TBD) 5.예약). 이 Phase는 PRD 5절이 정의한 **실제 5개 메뉴**로 교체하고, Phase 17~20의 controller를 전부 실제로 연결한다.

## 목표

콘솔 메뉴(시료관리/주문/모니터링/출고처리/생산라인) 입출력 구현. view는 input/print만 담당하고, 실제 흐름 제어는 controller(Phase 17~20)를 호출한다. `main.py`가 model/repository/controller/view를 조립한다.

## 설계

- 메인 메뉴 (PRD 5절 그대로):
  1. 시료관리: 등록/조회/검색 (Phase17 `SampleController`, 이미 연결됨)
  2. 주문: 접수/승인/거절/취소 (Phase18/19 `OrderController.submit/approve/reject/cancel`)
  3. 모니터링: 주문량 상태별 카운트 + 재고 판정 (Phase20 `MonitoringController`)
  4. 출고처리: CONFIRMED -> RELEASE (Phase20 `OrderController.release_order`)
  5. 생산라인: 현재 생산중/대기큐 조회 (Phase20 `ProductionLineController.current_jobs/waiting_jobs`) — 이 Phase에서는 **정적 조회**만 구현한다. "보는 동안 실시간으로 진행률이 올라가는 것"은 Phase 25에서 별도로 추가한다(경과시간 추산 + 조회 화면 전용 스레드). Phase21 시점엔 `current_jobs()`/`waiting_jobs()`가 반환하는 시점의 스냅샷만 보여주면 된다.
  0. 종료
- `main.py`: `SampleRepository`/`InventoryRepository`/`OrderRepository`/`ProductionQueue` 생성 -> `SampleController`/`OrderController`(production_queue 주입)/`MonitoringController`/`ProductionLineController` 생성 -> `MainController`에 전부 주입 -> `MainController.run()`.
- `controller/main_controller.py`: Phase22의 TBD 분기(메뉴 2~5)를 실제 controller 호출로 교체. 각 하위 메뉴는 Phase22의 시료관리 서브메뉴 패턴(선택 -> 입력 prompt -> controller 호출 -> view 출력)을 그대로 따른다.
- `view/console_view.py`: 주문/모니터링/출고/생산라인 관련 prompt/출력 함수 추가 (예: `prompt_order_submit()`, `show_order()`, `show_status_counts(counts)`, `show_stock_judgement(judgements)`, `show_production_lines(jobs, waiting)` 등). 여전히 입출력만, 로직 없음.

### 설계 공백 발견 및 해결: 생산완료 -> Order CONFIRMED 반영

E2E를 짜다가 발견: `ProductionQueue.produce_unit()`(Phase9/10)이 반환하는 "확정된 `ProductionJob` 목록"을 받아서, 그 `job.order_id`에 해당하는 실제 `Order`의 상태를 CONFIRMED로 바꾸고 저장하는 역할이 어느 Phase 설계에도 없었다. Phase9/10은 순수 model(큐) 레벨에서 "이 job은 확정됐다"는 목록만 반환하면 끝났고, 그 결과를 Order 엔티티에 반영하는 연결고리(controller 몫)가 빠져 있었다.

해결:
- `model/order.py`에 `Order.complete_production(self) -> None` 추가: Phase11의 가드 패턴과 동일하게, `PRODUCING` 상태에서만 허용하고 `CONFIRMED`로 전이. 그 외 상태면 `InvalidOrderTransitionError`.
- `controller/order_controller.py`에 `complete_production(self, confirmed_jobs: list) -> list[Order]` 추가: 각 job의 `order_id`로 `order_repo.find_by_id` -> `order.complete_production()` 호출(모델 가드 재사용) -> `order_repo.save(order)`. 갱신된 `Order` 목록을 반환.
- 이 메서드는 `produce_unit()`(수동 시뮬레이션)이든 Phase25의 `tick()`(경과시간 기반)이든, "확정된 job 목록"을 반환하는 모든 지점에서 동일하게 호출해 쓸 수 있다.

## 완료 조건 (E2E, 권장)

- [x] E2E: 접수 -> 승인(재고부족) -> 생산 진행(`produce_unit` 직접 반복 호출로 진행 시뮬레이션, 스레드/시간 없이) -> 완료(`complete_production`) -> 출고 전체 시나리오, controller 계층 통해 검증
- [ ] 시료관리 메뉴 콘솔 흐름 테스트 (Phase17/22에서 이미 검증됨 — 회귀만 확인)
- [ ] 주문 메뉴 콘솔 흐름 테스트 (접수/승인/거절/취소)
- [ ] 모니터링 메뉴 콘솔 흐름 테스트
- [ ] 출고처리 메뉴 콘솔 흐름 테스트
- [ ] 생산라인 메뉴 콘솔 흐름 테스트 (정적 조회만, 실시간 갱신은 Phase25)
