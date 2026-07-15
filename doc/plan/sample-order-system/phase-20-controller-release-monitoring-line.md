# Phase 20: 출고처리/모니터링/생산라인 조회 유스케이스 (controller)

계층: controller

## 목표
- 출고처리: `OrderController.release_order(order_id)` (CONFIRMED -> RELEASE)
- 모니터링: 주문량 상태별 카운트 + 재고 판정(Phase 13 재사용)
- 생산라인: 현재 생산중 목록 + 대기큐 조회

## 설계
- 파일: `controller/order_controller.py`에 `release_order(self, order_id) -> Order` 추가
- 파일: `controller/monitoring_controller.py` — `class MonitoringController`, `count_orders_by_status(self) -> dict`, `judge_all_stock(self) -> dict[str, StockStatus]`
- 파일: `controller/production_line_controller.py` — `class ProductionLineController: def __init__(self, queue: ProductionQueue)`, `current_jobs(self) -> list[ProductionJob]`, `waiting_jobs(self) -> list[ProductionJob]`

## 완료 조건
- [ ] 출고처리 유스케이스 테스트 (CONFIRMED -> RELEASE, 부분출고 없음 확인)
- [ ] 모니터링 상태별 카운트 테스트
- [ ] 모니터링 재고 판정 조회 테스트
- [ ] 생산라인 현재/대기 조회 테스트
