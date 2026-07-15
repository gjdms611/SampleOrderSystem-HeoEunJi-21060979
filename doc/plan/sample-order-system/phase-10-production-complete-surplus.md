# Phase 10: 생산작업 완료 + 잉여 반영

계층: model

## 목표
자기 작업의 `produced_qty == actual_qty`가 되면 해당 주문 CONFIRMED 전환 (CLAUDE.md 필수 상태전이 케이스 3/4 후반부). Phase 9의 실시간 반영으로 이미 재고에는 전량 반영되어 있으므로, 이 Phase는 "자기 자신의 CONFIRMED 전환 시점" 판정과 라인을 유휴로 되돌려 다음 대기 작업을 배정하는 것만 다룬다.

## 설계
- `produce_unit` 내부에서 처리하거나 `ProductionQueue._complete_job(self, line_index) -> None`으로 분리.
- 완료 즉시 그 라인에 큐의 다음 대기 작업을 배정 (Phase 8의 `assign_idle_lines` 재사용).

## 완료 조건
- [x] 자기 작업 실생산량 전량 완료 시 CONFIRMED 전환 테스트
- [x] 완료 후 라인 유휴 -> 다음 대기 작업 배정 테스트
- [x] 잉여(실생산량 - 부족분)가 재고에 남아있는지 확인 테스트
