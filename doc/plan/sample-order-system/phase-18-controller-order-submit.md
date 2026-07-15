# Phase 18: 주문 접수/거절/취소 유스케이스 (controller)

계층: controller

## 목표
주문 접수(RESERVED 생성) / 거절 / 취소 유스케이스가 `OrderRepository`와 model 상태전이를 연결.

## 설계
- 파일: `controller/order_controller.py`
- `class OrderController: def __init__(self, order_repo, inventory_repo, sample_repo)`
- `submit(self, customer_name, sample_id, quantity) -> Order`
  - `order_id`는 호출자가 넘기지 않는다 — 컨트롤러가 순차 번호로 생성한다: `order_repo.find_all()` 개수를 기준으로 `f"O{len(existing)+1}"` (예: 기존 3건이면 다음은 `"O4"`).
- `reject(self, order_id) -> Order`
- `cancel(self, order_id) -> Order`
- 잘못된 상태에서 `reject`/`cancel` 호출 시 `model.order.InvalidOrderTransitionError`가 발생하는데, 이 컨트롤러는 그 예외를 **잡아서 그대로 올리지 않는다** — 콘솔 프로그램이 처리 안 된 예외로 죽는 것처럼 보이면 안 되기 때문이다. `try/except InvalidOrderTransitionError`로 감싸고, 실패를 나타내는 값(예: `None` 반환)으로 정리해 view가 "취소/거절할 수 없는 상태입니다" 같은 안내를 띄울 수 있게 한다. (Phase19의 `approve`도 같은 예외를 낼 수 있으므로 동일 패턴을 따른다.)

## 완료 조건
- [x] 주문 접수(RESERVED 생성 + 저장, order_id 순차 생성 포함) 테스트
- [x] 주문 거절 유스케이스 테스트
- [x] 주문 취소 유스케이스 테스트 (RESERVED만 가능 재확인)
- [x] 잘못된 상태에서 reject/cancel 호출 시 예외가 컨트롤러 밖으로 새지 않고 처리되는지 테스트
