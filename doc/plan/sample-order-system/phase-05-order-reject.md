# Phase 5: Order 상태전이 RESERVED -> REJECTED

계층: model

## 목표
`order.reject()` 호출 시 RESERVED인 주문을 REJECTED로 전이. (CLAUDE.md 필수 상태전이 케이스 1/4)

## 설계
- 시그니처: `Order.reject(self) -> None`
- 이 Phase는 정상 경로만 다룸. 잘못된 시작 상태에서의 호출 차단은 Phase 11에서 공통 가드로 처리.

## 완료 조건
- [x] RESERVED -> REJECTED 전이 테스트
