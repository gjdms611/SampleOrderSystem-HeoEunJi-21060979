# Phase 27: 컨트롤러/입력 예외 안전성 강화

계층: controller + view

## 배경

수동 콘솔 테스트 중 발견된 버그 5건 — 잘못된 입력(존재하지 않는 ID, 숫자 아닌 값)으로 콘솔이 처리 안 된 예외로 죽는다.

## 목표

`OrderController`의 `reject`/`cancel`/`release_order`/`approve`가 존재하지 않는 `order_id`에 안전하게 반응하고(`None` 반환, 예외 전파 금지), `submit`이 존재하지 않는 `sample_id`를 거부하며, 콘솔 숫자 입력이 검증 없이 죽지 않게 한다.

## 설계

### A) `OrderController.reject`/`cancel`/`release_order`: order_id 없음 가드
- `order_repo.find_by_id(order_id)`가 `None`이면, `.reject()`/`.cancel()`/`.release()`를 호출하지 않고 즉시 `None`을 반환한다 (Phase18/20에서 이미 하던 "잘못된 상태 -> None" 패턴과 동일선상).

### B) `OrderController.approve`: order_id 없음 가드 + 존재하지 않는 sample_id로 접수된 주문 방어
- `order_repo.find_by_id(order_id)`가 `None`이면 즉시 `None` 반환.
- `sample_repo.find_by_id(order.sample_id)`가 `None`이면(등록 안 된 시료를 가리키는 주문) 재고부족 계산 자체가 불가능하므로 `None`을 반환하고 승인 처리를 하지 않는다 — `sample=None`인 채로 `Order.approve()`에 들어가 `_start_production()`에서 죽는 현재 버그의 근본 원인 제거.

### C) `OrderController.submit`: sample_id 존재 검증
- `sample_repo.find_by_id(sample_id)`가 `None`이면 주문을 생성하지 않고 `None`을 반환한다 (B의 문제를 애초에 발생 못 하게 접수 시점에서 막는다).
- `main_controller.py`의 접수 흐름은 `submit()`이 `None`을 반환하면 `show_order(None)`으로 기존 "처리할 수 없습니다" 안내를 그대로 재사용한다.

### D) 콘솔 숫자 입력 검증 (`view/console_view.py`)
- `prompt_sample_register()`(평균생산시간, 수율)과 `prompt_order_submit()`(수량)의 `float()`/`int()` 변환을 검증한다 — 잘못된 입력이면 재입력을 요구하거나(간단히) 사용자에게 안내 후 `None`류 값으로 처리해 호출자가 처리 실패로 인식하게 한다. 구체적으로: 변환 실패 시 안내 메시지를 띄우고 다시 입력받는 루프로 처리한다 (입력 형식 오류는 재시도가 자연스러운 UX).

## 완료 조건

- [ ] 존재하지 않는 order_id로 reject/cancel/release_order 호출 시 None 반환(예외 전파 없음) 테스트 3건
- [ ] 존재하지 않는 order_id로 approve 호출 시 None 반환 테스트
- [ ] 등록 안 된 sample_id를 가리키는 주문의 approve 호출 시 None 반환(예외 없음) 테스트
- [ ] 존재하지 않는 sample_id로 submit 호출 시 None 반환 테스트
- [ ] 숫자 입력란에 비숫자 값을 넣었을 때 콘솔이 죽지 않고 재입력을 요구하는지 수동 확인
