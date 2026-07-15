# Phase 4: Order 생성 (초기 상태 RESERVED)

계층: model

## 목표
`Order(order_id, customer_name, sample_id, quantity)` 생성 시 `status = RESERVED`.

## 설계
- 파일: `model/order.py`
- `class OrderStatus(Enum): RESERVED, REJECTED, CONFIRMED, PRODUCING, RELEASE`
- `class Order: def __init__(self, order_id, customer_name, sample_id, quantity)` → `self.status = OrderStatus.RESERVED`

## 완료 조건
- [x] Order 생성 시 상태가 RESERVED인지 확인하는 테스트
