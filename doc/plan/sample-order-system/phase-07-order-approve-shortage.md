# Phase 7: Order 상태전이 RESERVED -> PRODUCING (재고부족)

계층: model

## 목표
재고수량 < 주문수량이면 Phase 3 계산식으로 부족분/실생산량/총생산시간을 계산해 `ProductionJob`을 생성하고 `status = PRODUCING`. (CLAUDE.md 필수 상태전이 케이스 3/4 중 전반부)

## 설계
- 파일: `model/production_job.py`
- `class ProductionJob: def __init__(self, order_id, sample_id, shortage, actual_qty, total_production_time)`, `produced_qty: int = 0` (누적 생산량)
- `Order.approve(self, inventory_qty_at_approval, sample: Sample)`가 재고부족 분기에서 `ProductionJob`을 만들어 반환하도록 Phase 6 시그니처를 확장.

## 엣지 케이스
- 재고수량 == 0 (전량 부족분)

## 완료 조건
- [ ] 재고부족 시 RESERVED -> PRODUCING 전이 + ProductionJob 생성 테스트
