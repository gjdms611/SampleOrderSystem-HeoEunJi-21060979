# Phase 19: 주문 승인 유스케이스 (controller)

계층: controller

## 목표
승인 시점 재고 조회 → model `Order.approve` 호출 → 재고충분이면 그대로 저장, 재고부족이면 `ProductionJob`을 `ProductionQueue`에 등록.

## 설계
- 시그니처: `OrderController.approve(self, order_id) -> Order`
- Phase 8~10의 `ProductionQueue`를 controller 계층에서 보유(주입)하여 승인 시 `enqueue` + `assign_idle_lines` 호출.

## 완료 조건
- [ ] 재고충분 승인 유스케이스 테스트 (CONFIRMED로 저장)
- [ ] 재고부족 승인 유스케이스 테스트 (PRODUCING으로 저장 + 큐 등록 확인)
