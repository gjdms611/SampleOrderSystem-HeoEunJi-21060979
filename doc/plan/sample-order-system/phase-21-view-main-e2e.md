# Phase 21: 메인 메뉴 5종 콘솔 + 조립 + E2E

계층: view + main

## 목표
콘솔 메뉴(시료관리/주문/모니터링/출고처리/생산라인) 입출력 구현. view는 input/print만 담당하고, 실제 흐름 제어는 controller(Phase 17~20)를 호출한다. `main.py`가 model/repository/controller/view를 조립한다 (`PoC/ConsoleMVC/main.py` 패턴).

## 설계
- 파일: `view/console_view.py` — 각 메뉴의 입력/출력 함수 (예: `show_main_menu()`, `read_choice()`, `show_sample_list(samples)` 등). 비즈니스 로직 없음.
- 파일: `main.py` — repository 생성 → controller 생성(repository 주입) → view 생성 → 메뉴 루프에서 view 입력을 controller로 전달, controller 결과를 view로 출력.

## 완료 조건 (E2E, 권장)
- [ ] 시료관리 메뉴 콘솔 흐름 테스트
- [ ] 주문 메뉴 콘솔 흐름 테스트
- [ ] 모니터링 메뉴 콘솔 흐름 테스트
- [ ] 출고처리 메뉴 콘솔 흐름 테스트
- [ ] 생산라인 메뉴 콘솔 흐름 테스트
- [ ] E2E: 접수 -> 승인(재고부족) -> 생산 진행 -> 완료 -> 출고 전체 시나리오, service(controller) 계층 통해 검증
