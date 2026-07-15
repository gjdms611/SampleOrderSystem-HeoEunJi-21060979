# Phase 13: 모니터링 판정 (재고 여유/부족/고갈)

계층: model

## 목표
시료별 수요합계(RESERVED 수량합 + PRODUCING 수량합)와 재고수량을 비교해 판정.

## 설계
- 파일: `model/monitoring.py`
- `class StockStatus(Enum): SUFFICIENT, SHORTAGE, DEPLETED`
- `judge_stock_status(inventory_qty: int, demand_total: int) -> StockStatus`
- 규칙: `inventory_qty == 0` → DEPLETED, `0 < inventory_qty < demand_total` → SHORTAGE, `inventory_qty >= demand_total` → SUFFICIENT

## 완료 조건
- [ ] DEPLETED 판정 테스트
- [ ] SHORTAGE 판정 테스트
- [ ] SUFFICIENT 판정 테스트
