# Phase 18: 주문 접수/거절/취소 유스케이스 (controller)

계층: controller

## 목표
주문 접수(RESERVED 생성) / 거절 / 취소 유스케이스가 `OrderRepository`와 model 상태전이를 연결.

## 설계
- 파일: `controller/order_controller.py`
- `class OrderController: def __init__(self, order_repo, inventory_repo, sample_repo)`
- `submit(self, customer_name, sample_id, quantity) -> Order`
- `reject(self, order_id) -> Order`
- `cancel(self, order_id) -> Order`

## 완료 조건
- [ ] 주문 접수(RESERVED 생성 + 저장) 테스트
- [ ] 주문 거절 유스케이스 테스트
- [ ] 주문 취소 유스케이스 테스트 (RESERVED만 가능 재확인)
