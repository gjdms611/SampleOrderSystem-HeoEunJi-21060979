# Phase 22: 실행 가능한 main.py 스켈레톤 (조기 실행 확인용)

계층: view + main

## 배경

Phase 21(메인 메뉴 5종 콘솔 + 조립 + E2E)은 Phase 17~20 controller가 모두 끝나야 시작할 수 있다. 현재 Phase 17(시료관리)만 끝난 상태에서, 실제로 눈으로 실행해 보며 지금까지의 구현을 확인하고 싶다는 요청에 따라 임시로 실행 가능한 스켈레톤을 먼저 만든다.

이 Phase는 Phase 21을 대체하지 않는다 — Phase 18~20이 끝나면 Phase 21에서 나머지 메뉴를 실제로 연결한다. 이 Phase 22는 그 전까지 수동으로 돌려볼 수 있는 최소 골격이다.

## 목표

메인 메뉴 5종을 콘솔에 띄우고, 그중 실제로 구현이 끝난 유스케이스(시료 등록/조회/검색, Phase 17)만 진짜로 동작시킨다. 아직 구현 안 된 나머지 메뉴는 선택 시 "TBD (Phase 18~20 구현 후 연결 예정)" 안내만 출력하고 메뉴로 돌아간다.

## 설계

- 파일: `view/console_view.py`
  - `show_main_menu() -> str`: 메뉴 5종을 출력하고 사용자 입력(1~5, 0=종료)을 받아 반환. 입력/출력만, 로직 없음.
  - 시료 등록/조회/검색에 필요한 개별 입력 prompt 함수도 이 파일에 둔다 (`prompt_sample_register()`, `prompt_sample_id()`, `prompt_search_keyword()` 등 최소한만).
- 파일: `controller/main_controller.py`
  - `class MainController: def __init__(self, sample_controller: SampleController)`
  - `run(self) -> None`: `show_main_menu()`로 받은 선택지에 따라 분기. 메뉴 1(시료관리)만 `SampleController`(Phase17)의 register/get/search를 실제 호출해 view로 출력. 메뉴 2~5(주문 접수/거절/취소, 주문 승인, 출고처리/모니터링/생산라인 조회)는 Phase 18~20 controller가 없으므로 "TBD (Phase 18~20 구현 후 연결 예정)" 메시지만 출력. 0 입력 시 종료.
- 파일: `main.py`
  - `SampleRepository`(파일 경로: `data/samples.json`), `SampleController`, `MainController`를 조립해 `MainController.run()` 실행.

## 엣지 케이스

- 잘못된 메뉴 번호 입력 시 안내 후 다시 메뉴로

## 완료 조건

- [x] `python main.py` 실행 시 메뉴 5종이 뜬다
- [x] 메뉴 1(시료관리) 선택 시 실제로 시료 등록/조회/검색이 파일(JSON)에 반영된다 (수동 확인)
- [x] 메뉴 2~5 선택 시 TBD 안내 문구가 뜨고 메뉴로 복귀한다 (수동 확인)

## 참고 (Windows 콘솔 실행 시)

한글 출력이 깨지면 `PYTHONUTF8=1 python main.py`로 실행한다 (콘솔 코드페이지가 UTF-8이 아닐 때 발생하는 표시 문제, 로직과 무관).
