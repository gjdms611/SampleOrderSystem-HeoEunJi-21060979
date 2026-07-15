# Phase 34: 도메인 값 검증 예외처리 + 주문 수량 검증

계층: model + controller + view

## 배경

PRD-코드 대조검증에서 발견된 버그 2건:
1. `main_controller._handle_sample_menu`가 `Sample.__init__`의 도메인 검증(`avg_production_time<=0`, `yield_rate` 범위 초과 등)에서 나는 `ValueError`를 안 잡아서, 잘못된 값을 입력하면 콘솔이 죽는다.
2. `Order`/`OrderController.submit`에 수량(quantity) 검증이 전혀 없어, 음수나 0인 수량으로도 주문이 그대로 생성된다.

## 목표

- 시료 등록 시 도메인 검증 실패(`ValueError`)가 콘솔을 죽이지 않고 안내 후 메뉴로 복귀한다.
- 주문 수량이 양수가 아니면 주문 생성 자체를 거부한다.

## 설계

- `model/order.py`의 `Order.__init__`에 `quantity > 0` 검증 추가 (위반 시 `ValueError`, `model/sample.py`의 기존 검증 패턴과 동일).
- `controller/order_controller.py`의 `submit()`: `Order(...)` 생성을 `try/except ValueError`로 감싸, 실패하면 `None`을 반환한다 (기존 `sample_id` 미등록 시 `None` 반환 패턴과 일관).
- `controller/main_controller.py`의 `_handle_sample_menu` action=="1"(등록) 분기: `sample_controller.register(...)` 호출을 `try/except ValueError`로 감싸, 실패하면 `console_view.show_message(str(e), error=True)`로 안내 후 메뉴로 복귀한다 (콘솔이 죽지 않음).

## 완료 조건

- [ ] `Order(quantity=0)` / `Order(quantity=-1)`이 `ValueError`를 내는지 테스트
- [ ] `OrderController.submit()`이 수량이 0 이하일 때 `None`을 반환하는지(예외 전파 없음) 테스트
- [ ] `python main.py`로 시료 등록 시 잘못된 숫자값(예: 평균생산시간에 0)을 넣어도 콘솔이 죽지 않고 안내 후 메뉴로 복귀하는지 수동 확인
