# Plan Index: 반도체 시료 생산주문관리 시스템

`doc/prd/sample-order-system.md` 기반. Python, JSON 파일 저장.

이 파일은 인덱스다. Phase별 상세 설계는 `doc/plan/sample-order-system/phase-NN-*.md`에 각각 분리되어 있다. 이 파일에서는 Phase 목록과 진행 상태(체크박스)만 갱신한다.

## 아키텍처 개요 (PoC 검증 결과 반영)

- `PoC/ConsoleMVC`에서 검증: `model`(데이터+로직, IO 없음) / `view`(콘솔 입출력만) / `controller`(흐름 제어만, 비즈니스 로직·직접 print 금지) 3계층 분리.
- `PoC/DataPersistence`에서 검증: `storage`(JSON 파일 raw load/save) / `repository`(CRUD 로직, storage를 통해서만 파일 접근) 2계층 분리.
- 두 PoC 결론을 합쳐 본 프로젝트 계층을 아래와 같이 구성한다.

```
main.py       - model/view/controller/repository 조립 진입점 (ConsoleMVC main.py 패턴)
view/         - 메인 메뉴 5종 콘솔 입출력(input/print)만. 비즈니스 로직 없음.
controller/   - 흐름 제어: view 입력 -> model/repository 호출 -> view 출력. 직접 print/input, 비즈니스 로직 금지.
model/        - 엔티티(Sample, Inventory, Order, ProductionJob, ProductionQueue) + 상태머신 + 계산식 + 모니터링 판정. 순수 로직, IO 없음.
repository/   - CRUD 로직 (find/save/search). storage를 통해서만 파일 접근, 직접 파일 IO 금지.
storage/      - JSON 파일 raw load/save. CRUD 의미 없음, 순수 파일 IO.
```

의존 방향: `main.py` → `view`/`controller` 조립 → `controller` → `model`, `controller` → `repository` → `storage`. `model`은 다른 계층을 모른다.

## Phase 구성 원칙

각 Phase는 하나의 동작(behavior)만 검증하는 RED-GREEN-REVIEW 사이클 하나다. Phase마다 사람 검토 후 커밋한다. 순서는 의존관계(model → storage → repository → controller → view) 그대로 따른다.

## Phase 목록 (상태)

| Phase | 계층 | 내용 | 상세 설계 | 상태 |
|---|---|---|---|---|
| 1 | model | Sample 엔티티 생성/검증 | [phase-01](sample-order-system/phase-01-sample-entity.md) | [x] |
| 2 | model | Inventory 엔티티 생성/조회 | [phase-02](sample-order-system/phase-02-inventory-entity.md) | [x] |
| 3 | model | 생산라인 계산식 (부족분/실생산량/총생산시간/잉여) | [phase-03](sample-order-system/phase-03-production-calc.md) | [x] |
| 4 | model | Order 생성 (초기 상태 RESERVED) | [phase-04](sample-order-system/phase-04-order-create.md) | [x] |
| 5 | model | Order 상태전이: RESERVED -> REJECTED | [phase-05](sample-order-system/phase-05-order-reject.md) | [x] |
| 6 | model | Order 상태전이: RESERVED -> CONFIRMED (재고충분) | [phase-06](sample-order-system/phase-06-order-approve-sufficient.md) | [x] |
| 7 | model | Order 상태전이: RESERVED -> PRODUCING (재고부족, ProductionJob 생성) | [phase-07](sample-order-system/phase-07-order-approve-shortage.md) | [x] |
| 8 | model | 생산대기큐: FIFO 등록 + 라인(N개) 유휴 시 배정 | [phase-08](sample-order-system/phase-08-production-queue.md) | [x] |
| 9 | model | 동시생산 실시간 반영 (PRD 6.2, 핵심) | [phase-09](sample-order-system/phase-09-concurrent-production.md) | [x] |
| 10 | model | 생산작업 완료 + 잉여 재고 반영 | [phase-10](sample-order-system/phase-10-production-complete-surplus.md) | [x] |
| 11 | model | Order 취소 규칙 + 허용 안 된 전이 차단 | [phase-11](sample-order-system/phase-11-order-cancel-guard.md) | [x] |
| 12 | model | Order 상태전이: CONFIRMED -> RELEASE | [phase-12](sample-order-system/phase-12-order-release.md) | [x] |
| 13 | model | 모니터링 판정: 재고 여유/부족/고갈 | [phase-13](sample-order-system/phase-13-monitoring-judge.md) | [x] |
| 14 | storage | JSON 파일 raw load/save 공통 유틸 | [phase-14](sample-order-system/phase-14-storage.md) | [x] |
| 15 | repository | Sample/Inventory CRUD (storage 사용) | [phase-15](sample-order-system/phase-15-repository-sample-inventory.md) | [x] |
| 16 | repository | Order CRUD (storage 사용) | [phase-16](sample-order-system/phase-16-repository-order.md) | [x] |
| 17 | controller | 시료관리 유스케이스 (등록/조회/검색) | [phase-17](sample-order-system/phase-17-controller-sample.md) | [x] |
| 18 | controller | 주문 접수/거절/취소 유스케이스 | [phase-18](sample-order-system/phase-18-controller-order-submit.md) | [x] |
| 19 | controller | 주문 승인 유스케이스 (재고확인 -> model 전이 + repository 반영) | [phase-19](sample-order-system/phase-19-controller-order-approve.md) | [x] |
| 20 | controller | 출고처리/모니터링/생산라인 조회 유스케이스 | [phase-20](sample-order-system/phase-20-controller-release-monitoring-line.md) | [x] |
| 21 | view+main | 메인 메뉴 5종 콘솔 + 조립 + E2E (PRD 기준 재설계) | [phase-21](sample-order-system/phase-21-view-main-e2e.md) | [x] |
| 22 | view+main | 실행 가능한 main.py 스켈레톤 (조기 실행 확인용, Phase18~20 미완료 메뉴는 TBD) | [phase-22](sample-order-system/phase-22-main-skeleton.md) | [x] |
| 23 | model | 생산대기큐 확정 스캔 성능 최적화 (FIFO 라인배정 보장 유지) | [phase-23](sample-order-system/phase-23-production-queue-performance.md) | [x] |
| 24 | view | 콘솔 UI/UX 개선 (출력 포맷만, 로직 변경 없음) | [phase-24](sample-order-system/phase-24-console-ux-polish.md) | [x] |
| 25 | model+controller+view | 생산라인 실시간 진행 (경과시간 추산 + 조회 화면 전용 스레드 + 예상완료시각) | [phase-25](sample-order-system/phase-25-production-line-live-tick.md) | 보류(Textual 전환에 흡수) |
| 26 | main+repository | 기본 제공 시료/재고 초기 데이터 시딩 | [phase-26](sample-order-system/phase-26-default-sample-seed.md) | [ ] |

Phase 22는 Phase 21을 대체하지 않는다 — Phase 17만 끝난 지금 시점에 수동으로 돌려볼 수 있는 임시 실행 골격이며, Phase 18~20이 끝나면 Phase 21에서 나머지 메뉴를 실제로 연결한다.

Phase 25는 콘솔(input/print) 구조를 전제로 스레드 기반 실시간 갱신을 설계했으나, view 계층을 Textual로 전면 재작성하기로 결정되어 이 Phase는 지금 구조로 구현하지 않는다 — Textual 전환 PRD/Plan에서 이 기능(생산라인 실시간 진행)을 Textual의 반응형 위젯/타이머로 자연스럽게 흡수한다.

## 테스트 전략

- Unit: model 계층 전부 (상태전이, 재고계산, 수율계산) — mock 없이 순수 함수/객체로 테스트.
- CLAUDE.md 필수 상태전이 케이스 4종 (각각 별도 테스트):
  1. RESERVED -> REJECTED (Phase 5)
  2. RESERVED -> CONFIRMED, 재고충분 (Phase 6)
  3. RESERVED -> PRODUCING -> CONFIRMED, 재고부족 후 생산완료 (Phase 7, 9, 10)
  4. CONFIRMED -> RELEASE (Phase 12)
- PRD 6.2 동시생산 시나리오 (Phase 9 필수 테스트):
  100ea 주문(부족분100, 실생산량150) 생산 중 + 20ea 주문(부족분20) 대기 중일 때, 누적 120 시점 20ea 먼저 CONFIRMED, 100ea는 150 전량 완료 시 CONFIRMED.
- E2E: 메인 메뉴 콘솔 흐름 (Phase 21, 권장).

## 진행 순서

Phase 1부터 21까지 순서대로 진행. Phase 하나 끝나면 사람 검토 후 커밋하고, 이 인덱스 파일에서 그 Phase의 상태 칸만 `[x]`로 갱신한다. 다른 Phase의 상세 파일은 손대지 않는다.

## 병렬 실행 정책 (Subagent RED-GREEN 병렬, REVIEW는 순차)

**원칙: 서로 데이터/코드 의존이 없는 Phase는 subagent로 병렬 RED-GREEN(테스트+구현) 진행 가능하다. 단, 사람 검토(REVIEW)와 커밋은 반드시 Phase 번호 순서대로 하나씩 순차 진행한다.** 병렬로 구현이 먼저 끝나도, 사람 검토는 새치기 없이 번호 순서를 지킨다 — 뒤 Phase가 앞 Phase 승인보다 먼저 커밋되면 "이번 기능이 무엇을 만들기로 합의했는가"의 순서 기록이 깨진다.

### 배치(batch) 구성

같은 배치 안의 Phase들은 서로 의존이 없어 병렬 진행 가능하다. 배치는 이전 배치가 만든 클래스/함수 시그니처에 의존하므로, 다음 배치의 subagent를 실행하기 전에 이전 배치 Phase들이 전부 GREEN까지(REVIEW/커밋은 아직 몰아둬도 됨) 끝나 있어야 한다.

| 배치 | Phase | 비고 |
|---|---|---|
| 1 | 1, 2, 3, 4, 13, 14 | 서로 의존 없음 (Sample/Inventory/계산식/Order생성/모니터링판정/storage) |
| 2 | 5, 6, 15, 16 | 5·6은 Phase4(Order) 필요, 15는 Phase14+1+2, 16은 Phase14+4 필요 |
| 3 | 7, 17 | 7은 Phase3+6, 17은 Phase15 필요 |
| 4 | 8 | Phase7(ProductionJob) 필요 |
| 5 | 9 | Phase8 필요 |
| 6 | 10 | Phase9 필요 |
| 7 | 11 | Phase4/5/6/7 전이 메서드 전부 존재해야 가드 추가 가능 |
| 8 | 12, 18 | 12는 Phase6, 18은 Phase16+4+5+11 필요 |
| 9 | 19 | Phase16+6+7+8+9+10 필요 |
| 10 | 20 | Phase16+13+8~10+12 필요 |
| 11 | 21 | Phase17~20 전부 필요 (마지막, 병렬 대상 없음) |

### 진행 방식

1. Master는 현재 배치의 Phase 개수만큼 subagent를 병렬로 fan-out한다. 각 subagent는 배정된 Phase 설계 파일(`phase-NN-*.md`)만 보고 그 Phase의 실패하는 테스트 + 최소 구현(RED+GREEN)까지 진행한다. 다른 Phase 파일이나 다른 subagent의 작업에 손대지 않는다.
2. 배치 내 모든 subagent가 GREEN까지 끝나면, Master는 Phase 번호가 가장 낮은 것부터 순서대로 사람에게 REVIEW를 요청한다. 하나가 승인+커밋될 때까지 다음 Phase의 REVIEW를 시작하지 않는다.
3. 사람이 특정 Phase를 반려하면, 그 Phase만 담당 subagent(또는 Master)가 GREEN/REVIEW로 돌아가 수정한다 — 이미 승인된 앞 Phase, 아직 검토 전인 뒤 Phase의 결과물은 건드리지 않는다.
4. 현재 배치의 모든 Phase가 REVIEW+커밋까지 끝나야 다음 배치의 subagent를 fan-out한다.
5. 이 정책은 RED-GREEN의 실행 방식(병렬 가능)에만 적용된다 — "실패하는 테스트를 먼저 본다", "Phase 설계 범위를 벗어나지 않는다" 같은 tdd-skill의 다른 규칙은 그대로 유지된다.
