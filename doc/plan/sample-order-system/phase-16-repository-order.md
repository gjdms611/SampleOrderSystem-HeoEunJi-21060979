# Phase 16: Order CRUD (repository)

계층: repository

## 목표
`Order`(상태 포함)를 storage를 통해 저장/조회.

## 설계
- 파일: `repository/order_repository.py`
  - `class OrderRepository: def __init__(self, file_path: str)`
  - `save(self, order: Order)`
  - `find_by_id(self, order_id) -> Order | None`
  - `find_all(self) -> list[Order]`

## 완료 조건
- [x] Order 저장/조회 테스트 (상태 포함 직렬화/역직렬화 확인)
- [x] find_all 테스트
