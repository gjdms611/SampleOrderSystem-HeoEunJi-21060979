# Phase 6: Order 상태전이 RESERVED -> CONFIRMED (재고충분)

계층: model

## 목표
승인 시점 재고수량 >= 주문수량이면 바로 CONFIRMED 전이. (CLAUDE.md 필수 상태전이 케이스 2/4)

## 설계
- 시그니처: `Order.approve(self, inventory_qty_at_approval: int) -> ProductionJob | None`
- 재고충분이면 `status = CONFIRMED`, 반환값 `None`.
- 재고부족 분기는 Phase 7에서 시그니처 확장.

## 완료 조건
- [x] 재고충분 시 RESERVED -> CONFIRMED 전이 테스트
