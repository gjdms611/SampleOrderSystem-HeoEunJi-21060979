# Phase 2: Inventory 엔티티 생성/조회

계층: model

## 목표
`Inventory(sample_id, quantity)` 생성 및 현재 재고수량 조회.

## 설계
- 파일: `model/inventory.py`
- 시그니처: `class Inventory: def __init__(self, sample_id: str, quantity: int)`, `quantity` 속성 직접 조회.
- 검증: `quantity < 0`이면 `ValueError`.

## 엣지 케이스
- `quantity == 0` (고갈 상태로 생성 가능)
- 음수 재고수량 거부

## 완료 조건
- [x] 정상 생성 + 조회 테스트
- [x] 음수 재고수량 거부 테스트
