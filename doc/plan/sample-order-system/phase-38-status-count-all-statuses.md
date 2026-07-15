# Phase 38: 주문 상태별 카운트에 0건 상태도 전부 표시

## 배경

`MonitoringController.count_orders_by_status()`는 실제로 존재하는 주문의 상태만 집계해서, 예를 들어 REJECTED 주문이 하나도 없으면 그 행 자체가 안 보인다. 어떤 상태가 몇 건인지 한눈에 비교하려면 0건인 상태도 함께 보여야 한다.

## 목표

`OrderStatus`의 모든 값(RESERVED/REJECTED/CONFIRMED/PRODUCING/RELEASE)을 항상 표시하고, 실제 주문이 없는 상태는 0건으로 보여준다.

## 설계

- `controller/monitoring_controller.py`의 `count_orders_by_status()`: `{status: 0 for status in OrderStatus}`로 먼저 전체 상태를 0으로 초기화한 뒤, 실제 주문을 순회하며 해당 상태의 카운트를 증가시켜 반환한다. (순서는 `OrderStatus` 정의 순서를 따른다.)
- `view/console_view.py`의 `show_status_counts()`: 지금은 "등록된 주문이 없습니다" 안내로 빈 딕셔너리를 처리하는데, 이제 `count_orders_by_status()`가 항상 5개 상태를 채워 반환하므로 그 빈 안내 분기가 실질적으로 호출되지 않는다 — 그대로 둬도 무방하지만(방어 코드), 함수 자체를 바꿀 필요는 없다.

## 완료 조건

- [ ] 주문이 하나도 없을 때도 `count_orders_by_status()`가 5개 상태 전부 0으로 반환하는지 테스트
- [ ] 주문이 일부 상태에만 있을 때, 없는 상태는 0으로 채워지는지 테스트
- [ ] `python main.py`로 모니터링 메뉴에서 주문상태별 카운트가 항상 5개 행을 보여주는지 수동 확인
