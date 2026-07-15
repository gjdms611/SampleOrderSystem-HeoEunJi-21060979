# Phase 9: 동시생산 실시간 반영 (PRD 6.2, 핵심)

계층: model

## 목표
라인이 시료 1단위를 생산할 때마다(`produce_unit`) 즉시 `Inventory.quantity += 1`, 그리고 대기 중인 다른 주문(현재 생산 진행 중인 자기 자신 제외)을 큐 앞에서부터 확인해 재고가 그 주문의 부족분을 채우면 즉시 CONFIRMED 전환 + 그만큼 재고 차감. 생산 진행 중인 작업 자신은 `produced_qty == actual_qty`가 될 때까지 CONFIRMED 전환 안 함 (자기 예외).

## 설계
- 시그니처: `ProductionQueue.produce_unit(self, line_index: int, inventory: Inventory) -> list[ProductionJob]` — 1단위 생산 처리 한 번의 호출 단위. 반환값은 이번 호출로 새로 CONFIRMED된(대기열에서 제거된) `ProductionJob` 목록(보통 빈 리스트).
- 핵심 메커니즘(자기 예외 구현 방법): 라인의 job은 `produced_qty`가 자신의 `shortage`를 **초과한 만큼만** `inventory.quantity`에 반영한다 — 처음 `shortage`개는 그 job 자신의 부족분을 채우는 몫이라 다른 대기 주문에 흘러가지 않는다. `shortage`를 넘어선 생산분(잉여)만 실시간으로 `inventory.quantity`에 더해지고, `waiting`의 각 주문을 순서대로 확인해 (같은 `sample_id`이고) 이 잉여가 그 주문의 `shortage`에 도달하면 즉시 그 주문을 `waiting`에서 제거 + 확정 목록에 추가 + 그만큼 `inventory.quantity`에서 차감한다.
  - 이 규칙 덕분에 PRD 6.2 예시(100ea 부족분100/실생산량150 생산 중, 20ea 부족분20 대기)에서: 1~100번째 생산분은 100ea 자신의 몫(잉여 0), 101~120번째(20개)가 잉여로 누적돼 정확히 누적 생산 120 시점에 20ea가 충족되어 CONFIRMED된다.
  - 라인의 job 자신은 `waiting`에 없으므로 이 스캔 로직에서 자연히 제외된다("자기 예외"). 자신의 완료 처리(잉여 재고 반영 포함)는 Phase 10에서 다룬다.

## 엣지 케이스 (PRD 6.2 예시로 검증, CLAUDE.md 필수 상태전이 케이스 3/4 핵심)
- 같은 시료에 100ea 주문(부족분100, 실생산량150)이 먼저 PRODUCING, 20ea 주문(부족분20)이 큐 대기 중일 때
- 누적 생산량 120 시점에 20ea가 먼저 CONFIRMED
- 100ea는 150 전량 완료 시점에 CONFIRMED (자기 예외로 인해 20ea보다 늦게 CONFIRMED될 수 있음)

## 완료 조건
- [ ] 생산 1단위마다 재고 실시간 반영 테스트
- [ ] 대기 중인 다른 주문 부족분 충족 시 즉시 CONFIRMED 전환 테스트
- [ ] PRD 6.2 100ea/20ea 시나리오 테스트 (누적 120에서 20ea 먼저 CONFIRMED, 100ea는 150 전량 완료 시 CONFIRMED)
