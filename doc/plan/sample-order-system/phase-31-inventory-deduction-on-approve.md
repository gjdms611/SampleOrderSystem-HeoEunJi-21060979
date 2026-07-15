# Phase 31: 주문 승인 시 재고 차감

계층: controller

## 배경

PRD-코드 대조검증에서 발견된 치명적 버그: `OrderController.approve()`가 재고충분/재고부족 어느 경로든 `inventory.quantity`를 전혀 차감하지 않는다. PRD 2.2("재고는 주문승인 시 차감, 생산완료 시 증가")를 위반한다. 승인 시점에 사용한 재고를 반영하지 않으면, 같은 시료의 다른 주문 승인 시 이미 소모된 재고가 여전히 있는 것처럼 이중 계산된다.

## 목표

`OrderController.approve()`가 승인 결과(재고충분/재고부족)에 따라 실제로 `Inventory`를 차감하고 저장한다.

## 설계

- 재고충분 경로(`order.approve()`가 `None` 반환, 즉 CONFIRMED): 승인에 사용된 재고만큼(`inventory_qty_at_approval` 중 `order.quantity`만큼)을 차감한다 — `inventory.quantity -= order.quantity`. (재고충분이므로 `inventory.quantity >= order.quantity`가 보장되어 음수가 될 수 없다.)
- 재고부족 경로(`order.approve()`가 `ProductionJob` 반환, 즉 PRODUCING): 승인 시점에 있던 재고 전량이 이 주문에 쓰이는 것으로 간주해 `inventory.quantity = 0`으로 만든다 (승인 시점 재고 `inventory_qty_at_approval` 전부를 소진). 이후 생산 진행에 따라 실시간으로 재고가 다시 채워지는 것(Phase9)과 자연스럽게 이어진다.
- 재고 레코드 자체가 없던 경우(`inventory`가 `None`, 즉 재고 미등록 상태로 재고부족 처리된 경우)는 차감할 게 없으므로 아무 것도 하지 않는다.
- 위 갱신 후 `inventory_repo.save(inventory)`를 호출한다 (재고 레코드가 없었다면 저장할 것도 없으므로 호출하지 않는다).
- `Order`/`model/order.py`는 건드리지 않는다 — 재고 차감은 model의 상태전이 로직이 아니라 controller가 repository들을 조율하는 책임이다 (model은 순수 로직, IO/저장은 controller+repository 몫이라는 기존 계층 분리 원칙 유지).

## 엣지 케이스

- 재고충분 시 정확히 `order.quantity`만큼만 차감 (승인 시점 재고가 주문량보다 많았다면 남는 부분은 그대로 유지).
- 재고부족 시 재고 전량 소진(0).
- 재고 레코드 자체가 없던 상태에서 재고부족으로 처리된 경우 저장소에 새 레코드를 만들지 않는다 (있지도 않은 재고를 0으로 "생성"하지 않음 — 필요하면 Phase10의 실시간 반영이 자연스럽게 채운다).

## 완료 조건

- [ ] 재고충분 승인 시 `inventory.quantity`가 `order.quantity`만큼 차감되어 저장되는지 테스트
- [ ] 재고부족 승인 시 `inventory.quantity`가 0으로 저장되는지 테스트
- [ ] 재고 레코드가 아예 없던 상태에서 재고부족 승인 시 새 재고 레코드가 생성되지 않는지 테스트
- [ ] 기존 E2E 시나리오(`tests/test_e2e_order_flow.py`)가 갱신된 재고값 기준으로도 여전히 통과하는지 확인
