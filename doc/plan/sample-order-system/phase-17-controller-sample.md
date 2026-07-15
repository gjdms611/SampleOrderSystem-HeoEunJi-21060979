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
- `list_all(self) -> list[Sample]` (사용성 피드백으로 추가: "조회" 메뉴가 시료ID를 입력해야만 하나만 보여주는 게 불편하다는 지적에 따라, 콘솔 메뉴의 "조회"는 이제 이 메서드로 전체 목록을 보여준다. `get()`은 API/테스트로는 남겨두되 메인 메뉴 흐름에서는 더 이상 호출하지 않는다.)

## 완료 조건
- [x] 시료 등록 유스케이스 테스트
- [x] 시료 조회 유스케이스 테스트
- [x] 시료 검색 유스케이스 테스트
- [x] 시료 전체 목록 조회(`list_all`) 테스트
