# Phase 21: 메인 메뉴 5종 콘솔 + 조립 + E2E

계층: view + main

## 배경

Phase 22(임시 실행 골격)는 메뉴 구조를 PRD와 다르게 임시로 나눴었다(1.시료관리 2.주문접수/거절/취소 3.주문승인 4.출고+모니터링+생산라인(TBD) 5.예약). 이 Phase는 PRD 5절이 정의한 **실제 5개 메뉴**로 교체하고, Phase 17~20의 controller를 전부 실제로 연결한다.

## 목표

콘솔 메뉴(시료관리/주문/모니터링/출고처리/생산라인) 입출력 구현. view는 input/print만 담당하고, 실제 흐름 제어는 controller(Phase 17~20)를 호출한다. `main.py`가 model/repository/controller/view를 조립한다.

## 설계

- 메인 메뉴 (PRD 5절 그대로):
  1. 시료관리: 등록/조회/검색 (Phase17 `SampleController`, 이미 연결됨)
  2. 주문: 접수/승인/거절/취소 (Phase18/19 `OrderController.submit/approve/reject/cancel`)
  3. 모니터링: 주문량 상태별 카운트 + 재고 판정 (Phase20 `MonitoringController`)
  4. 출고처리: CONFIRMED -> RELEASE (Phase20 `OrderController.release_order`)
  5. 생산라인: 현재 생산중/대기큐 조회 (Phase20 `ProductionLineController.current_jobs/waiting_jobs`) — 이 Phase에서는 **정적 조회**만 구현한다. "보는 동안 실시간으로 진행률이 올라가는 것"은 Phase 25에서 별도로 추가한다(경과시간 추산 + 조회 화면 전용 스레드). Phase21 시점엔 `current_jobs()`/`waiting_jobs()`가 반환하는 시점의 스냅샷만 보여주면 된다.
  0. 종료
- `main.py`: `SampleRepository`/`InventoryRepository`/`OrderRepository`/`ProductionQueue` 생성 -> `SampleController`/`OrderController`(production_queue 주입)/`MonitoringController`/`ProductionLineController` 생성 -> `MainController`에 전부 주입 -> `MainController.run()`.
- `controller/main_controller.py`: Phase22의 TBD 분기(메뉴 2~5)를 실제 controller 호출로 교체. 각 하위 메뉴는 Phase22의 시료관리 서브메뉴 패턴(선택 -> 입력 prompt -> controller 호출 -> view 출력)을 그대로 따른다.
- `view/console_view.py`: 주문/모니터링/출고/생산라인 관련 prompt/출력 함수 추가 (예: `prompt_order_submit()`, `show_order()`, `show_status_counts(counts)`, `show_stock_judgement(judgements)`, `show_production_lines(jobs, waiting)` 등). 여전히 입출력만, 로직 없음.

## 완료 조건 (E2E, 권장)

- [ ] 시료관리 메뉴 콘솔 흐름 테스트 (Phase17/22에서 이미 검증됨 — 회귀만 확인)
- [ ] 주문 메뉴 콘솔 흐름 테스트 (접수/승인/거절/취소)
- [ ] 모니터링 메뉴 콘솔 흐름 테스트
- [ ] 출고처리 메뉴 콘솔 흐름 테스트
- [ ] 생산라인 메뉴 콘솔 흐름 테스트 (정적 조회만, 실시간 갱신은 Phase25)
- [ ] E2E: 접수 -> 승인(재고부족) -> 생산 진행(`produce_unit` 직접 반복 호출로 진행 시뮬레이션, 스레드/시간 없이) -> 완료 -> 출고 전체 시나리오, controller 계층 통해 검증
