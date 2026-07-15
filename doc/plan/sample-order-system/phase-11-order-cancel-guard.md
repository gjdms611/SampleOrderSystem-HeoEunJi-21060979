# Phase 11: Order 취소 규칙 + 허용 안 된 전이 차단

계층: model

## 목표
`order.cancel()`은 RESERVED 상태에서만 허용, 그 외 상태는 에러. `reject`/`approve`/`release`도 잘못된 시작 상태에서 호출되면 에러.

## 설계
- 시그니처: `Order.cancel(self) -> None`
- 모든 전이 메서드 진입부에 상태 가드 추가 → 위반 시 `InvalidOrderTransitionError` (신규 예외 클래스, `model/order.py`)

## 엣지 케이스
- REJECTED/CONFIRMED/PRODUCING/RELEASE 상태에서 `cancel()` 시도
- REJECTED에서 `approve()` 시도

## 완료 조건
- [ ] RESERVED 외 상태에서 cancel() 거부 테스트
- [ ] 잘못된 시작 상태에서 reject/approve/release 거부 테스트
