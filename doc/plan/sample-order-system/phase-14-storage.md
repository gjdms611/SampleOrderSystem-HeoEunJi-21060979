# Phase 14: JSON 파일 raw load/save 공통 유틸

계층: storage

## 목표
JSON 파일에서 데이터를 읽고 쓰는 raw IO만 담당. CRUD 의미(찾기/검색 등)는 갖지 않는다. (`PoC/DataPersistence/storage.py` 패턴)

## 설계
- 파일: `storage/json_storage.py`
- `load(path: str) -> list` — 파일 없으면 빈 리스트 반환
- `save(data: list, path: str) -> None` — 디렉터리 없으면 생성 후 저장

## 엣지 케이스
- 파일이 없는 경로에서 load 시 빈 리스트
- 저장 경로의 디렉터리가 없을 때 자동 생성

## 완료 조건
- [ ] 파일 없을 때 load 빈 리스트 반환 테스트
- [ ] save 후 load로 동일 데이터 확인 테스트 (재시작 후 유지 검증)
