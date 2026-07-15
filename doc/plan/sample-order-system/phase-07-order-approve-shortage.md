# Phase 7: Order 상태전이 RESERVED -> PRODUCING (재고부족)

계층: model

## 목표
재고수량 < 주문수량이면 Phase 3 계산식으로 부족분/실생산량/총생산시간을 계산해 `ProductionJob`을 생성하고 `status = PRODUCING`. (CLAUDE.md 필수 상태전이 케이스 3/4 중 전반부)

## 설계
- 파일: `model/production_job.py`
- `class ProductionJob: def __init__(self, order_id, sample_id, shortage, actual_qty, total_production_time)`, `produced_qty: int = 0` (누적 생산량)
- `Order.approve(self, inventory_qty_at_approval, sample: Sample = None)`가 재고부족 분기에서 `ProductionJob`을 만들어 반환하도록 Phase 6 시그니처를 확장.
  - `sample`은 기본값 `None`인 선택 인자다. 재고충분(Phase6) 분기는 생산을 하지 않으므로 시료의 평균생산시간/수율 값을 전혀 참조하지 않는다 — "이 주문이 무슨 시료냐"는 이미 `Order.sample_id`로 알고 있고, `sample` 인자는 오직 재고부족 분기의 생산량/생산시간 계산에만 쓰인다. 그래서 Phase6에서 이미 커밋된 `order.approve(inventory_qty_at_approval=10)` 호출부는 수정하지 않고, 재고부족 분기에서만 `sample`을 요구한다(내부적으로 None이면 계산 불가하므로 에러 처리는 하지 않음 — 재고부족 시엔 항상 sample을 넘겨야 한다는 호출측 책임).

## 엣지 케이스
- 재고수량 == 0 (전량 부족분)

## 완료 조건
- [x] 재고부족 시 RESERVED -> PRODUCING 전이 + ProductionJob 생성 테스트
