# Phase 15: Sample/Inventory CRUD (repository)

계층: repository

## 목표
`Sample`, `Inventory`를 storage를 통해 저장/조회/검색. repository는 직접 파일 IO를 하지 않고 Phase 14의 storage 모듈만 호출한다.

## 설계
- 파일: `repository/sample_repository.py`
  - `class SampleRepository: def __init__(self, file_path: str)`
  - `save(self, sample: Sample)`
  - `find_by_id(self, sample_id) -> Sample | None`
  - `search(self, keyword: str) -> list[Sample]`
- 파일: `repository/inventory_repository.py`
  - `class InventoryRepository: def __init__(self, file_path: str)`
  - `save(self, inventory: Inventory)`
  - `find_by_sample_id(self, sample_id) -> Inventory | None`

## 엣지 케이스
- 동일 ID 저장 시 덮어쓰기
- 존재하지 않는 ID 조회 시 `None`

## 완료 조건
- [x] Sample 저장/조회 테스트
- [x] Sample 검색 테스트
- [x] Inventory 저장/조회 테스트
- [x] 동일 ID 덮어쓰기 테스트
