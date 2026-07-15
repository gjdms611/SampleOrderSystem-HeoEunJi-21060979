# Phase 28: 시료 중복 등록 방지

계층: controller

## 배경

지금은 이미 존재하는 `sample_id`로 다시 등록하면 `SampleRepository.save()`가 조용히 덮어쓴다(Phase15에서 검증된 "동일 ID 덮어쓰기" 동작). 그런데 사용자 입장에서는 실수로 같은 ID를 다시 등록했을 때, 아무 말 없이 정보가 바뀌는 것보다 "이미 있는 ID"라고 알려주고 기존 정보를 보여주는 게 안전하다.

## 목표

`SampleController.register()`가 이미 존재하는 `sample_id`로 호출되면 등록/덮어쓰기를 하지 않고, 이미 등록된 기존 시료 정보를 그대로 반환한다. 호출자(view)는 이 경우 "이미 등록된 시료ID입니다" 안내와 함께 기존 정보를 보여준다.

## 설계

- `controller/sample_controller.py`의 `register(self, sample_id, name, avg_production_time, yield_rate)`:
  - `self.repo.find_by_id(sample_id)`로 기존 시료를 먼저 조회한다.
  - 이미 있으면 새로 저장하지 않고, 기존 시료 객체와 "중복이었다"는 신호를 함께 반환한다 — 반환 타입을 `(Sample, bool)` 튜플로 바꾼다: `(sample, is_new)`. `is_new=False`면 기존 정보, `True`면 이번에 새로 등록된 정보.
  - 없으면 지금처럼 새로 생성해 저장하고 `(sample, True)`를 반환한다.
- `controller/main_controller.py`: 등록 흐름에서 `sample, is_new = self.sample_controller.register(...)`로 받아, `is_new`가 `False`면 `view`에 "이미 등록된 시료ID입니다" 안내를 먼저 띄우고 그 다음 기존 정보를 보여준다. `True`면 지금처럼 등록 결과만 보여준다.
- `view/console_view.py`: 새 안내 문구 추가 (`show_message("이미 등록된 시료ID입니다. 기존 정보:")` 같은 형태), `show_sample()` 자체는 바꾸지 않는다.

## 완료 조건

- [ ] 존재하지 않는 sample_id로 register 시 새로 생성되고 `(sample, True)` 반환 테스트
- [ ] 이미 존재하는 sample_id로 register 시 저장소가 바뀌지 않고(덮어쓰기 안 됨) 기존 정보 + `(sample, False)` 반환 테스트
- [ ] `python main.py`로 같은 ID를 두 번 등록해봤을 때 "이미 등록된 시료ID입니다" 안내와 기존 정보가 뜨는지 수동 확인
