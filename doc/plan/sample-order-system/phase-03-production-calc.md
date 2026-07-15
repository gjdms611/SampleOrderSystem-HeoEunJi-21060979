# Phase 3: 생산라인 계산식

계층: model

## 목표
PRD 6절 계산식을 순수 함수로 구현 (아직 큐/상태전이와 연결하지 않음).

## 설계
- 파일: `model/production_calc.py`
- `calc_shortage(order_qty: int, inventory_qty: int) -> int` — `order_qty - inventory_qty`
- `calc_actual_production_qty(shortage: int, yield_rate: float) -> int` — `ceil(shortage / yield_rate)`
- `calc_total_production_time(avg_production_time: float, actual_qty: int) -> float` — `avg_production_time * actual_qty`
- `calc_surplus(actual_qty: int, shortage: int) -> int` — `actual_qty - shortage`

## 엣지 케이스
- `yield_rate == 1` → 잉여 0
- 나누어떨어지는 경우 → 잉여 0
- 나누어떨어지지 않는 경우 → 잉여 > 0 (ceil 올림분)

## 완료 조건
- [x] calc_shortage 테스트
- [x] calc_actual_production_qty 테스트 (ceil 확인)
- [x] calc_total_production_time 테스트
- [x] calc_surplus 테스트
