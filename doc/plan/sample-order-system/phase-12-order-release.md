# Phase 12: Order 상태전이 CONFIRMED -> RELEASE

계층: model

## 목표
`order.release()` 호출 시 CONFIRMED인 주문만 RELEASE로 전이. 부분출고 없음(수량 분할 인자 자체가 없음). (CLAUDE.md 필수 상태전이 케이스 4/4)

## 설계
- 시그니처: `Order.release(self) -> None`

## 완료 조건
- [x] CONFIRMED -> RELEASE 전이 테스트 (그 외 상태에서 거부하는 가드 포함)
