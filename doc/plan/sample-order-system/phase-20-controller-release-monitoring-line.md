# Phase 20: 출고처리/모니터링/생산라인 조회 유스케이스 (controller)

계층: controller

## 목표
- 출고처리: `OrderController.release_order(order_id)` (CONFIRMED -> RELEASE)
- 모니터링: 주문량 상태별 카운트 + 재고 판정(Phase 13 재사용)
- 생산라인: 현재 생산중 목록 + 대기큐 조회

## 설계
- 파일: `controller/order_controller.py`에 `release_order(self, order_id) -> Order` 추가. Phase18/19와 동일하게 `InvalidOrderTransitionError`는 잡아서 `None`으로 처리(컨트롤러 밖으로 새지 않음).
- 파일: `controller/monitoring_controller.py` — `class MonitoringController: def __init__(self, order_repo, inventory_repo)`
  - `count_orders_by_status(self) -> dict[OrderStatus, int]`: 전체 주문을 상태별로 집계.
  - `judge_all_stock(self) -> dict[str, StockStatus]`: `sample_id`별 수요합계(RESERVED+PRODUCING 수량합, Phase13 규칙)와 `inventory_repo.find_all()`의 각 재고수량을 비교해 판정. `InventoryRepository`에 `find_all()`이 없어서 이번 Phase에서 추가함(Phase15 확장).
- 파일: `controller/production_line_controller.py` — `class ProductionLineController: def __init__(self, queue: ProductionQueue)`, `current_jobs(self) -> list[ProductionJob]` (라인 중 `None`이 아닌 것만), `waiting_jobs(self) -> list[ProductionJob]` (`queue.waiting` 그대로)

## 완료 조건
- [x] 출고처리 유스케이스 테스트 (CONFIRMED -> RELEASE, 부분출고 없음 확인)
- [x] 모니터링 상태별 카운트 테스트
- [x] 모니터링 재고 판정 조회 테스트
- [x] 생산라인 현재/대기 조회 테스트
