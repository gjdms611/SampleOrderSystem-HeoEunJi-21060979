# Phase 17: 시료관리 유스케이스 (controller)

계층: controller

## 목표
시료 등록/조회/검색 유스케이스가 `SampleRepository`를 통해 동작. 직접 print/input 없음 (view가 담당).

## 설계
- 파일: `controller/sample_controller.py`
- `class SampleController: def __init__(self, repo: SampleRepository)`
- `register(self, sample_id, name, avg_production_time, yield_rate) -> Sample`
- `get(self, sample_id) -> Sample | None`
- `search(self, keyword) -> list[Sample]`

## 완료 조건
- [ ] 시료 등록 유스케이스 테스트
- [ ] 시료 조회 유스케이스 테스트
- [ ] 시료 검색 유스케이스 테스트
