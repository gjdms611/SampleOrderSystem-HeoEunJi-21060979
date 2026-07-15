# Phase 37: 시료 조회/검색 결과에 재고수량 포함

## 배경

시료관리의 조회(전체목록)/검색 결과에 재고수량이 안 보여서, 재고를 확인하려면 별도로 모니터링 메뉴(재고판정)로 가야 하는 불편함이 있다.

## 목표

시료 조회(전체목록)/검색/단건조회 결과에 각 시료의 현재 재고수량을 함께 보여준다.

## 설계

- `controller/sample_controller.py`: 생성자에 `inventory_repo`를 추가로 주입받는다 (`__init__(self, repo, inventory_repo)`).
- `list_all()`, `search(keyword)`, `get(sample_id)`가 반환하는 각 `Sample`에 대해 `inventory_repo.find_by_sample_id(sample.sample_id)`로 재고를 조회하고, `(sample, quantity)` 튜플(재고 미등록이면 `quantity=0`)로 묶어 반환한다. `list_all()`/`search()`는 `(sample, quantity)` 튜플 리스트를, `get()`은 단일 `(sample, quantity)` 튜플(또는 시료 자체가 없으면 `None`)을 반환한다.
- `register()`는 이 Phase 범위 밖 — 반환 타입(`(Sample, is_new)`) 그대로 둔다.
- `view/console_view.py`의 `show_sample()`/`show_samples()`를 `(sample, quantity)` 튜플(또는 그 리스트)을 받도록 바꾸고, 표에 "재고" 컬럼을 추가한다.
- `controller/main_controller.py`의 시료관리 조회(2)/검색(3) 호출부를 새 반환 타입에 맞게 갱신한다. `main.py`에서 `SampleController` 생성 시 `inventory_repo`를 함께 넘기도록 조립부도 갱신한다.
- `register()`가 호출하는 `show_sample(sample)`(등록 결과 표시, `Sample` 단일 객체)은 이 Phase에서 시그니처가 바뀌는 `show_sample`과 충돌하므로, 등록 흐름도 `(sample, 0)` 튜플로 감싸서 넘기도록 함께 맞춘다 (신규 등록 시 재고는 항상 0이므로 값 조작 없이 고정 0으로 감싸면 된다).

## 완료 조건

- [ ] `SampleController.list_all()`/`search()`/`get()`이 각 시료의 재고수량을 포함한 `(sample, quantity)` 형태로 반환하는지 테스트 (재고 미등록 시 0)
- [ ] `python main.py`로 시료 조회/검색/등록 결과에 재고 컬럼이 보이는지 수동 확인
