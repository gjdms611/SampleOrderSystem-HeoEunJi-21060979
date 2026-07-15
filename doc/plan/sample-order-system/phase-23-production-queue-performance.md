# Phase 23: 생산대기큐 확정 스캔 성능 최적화

계층: model

## 배경

Phase 9의 `produce_unit()`은 잉여가 발생할 때마다 `self.waiting` 전체를 순회해 확정 가능한 주문을 찾는다. 대기 주문 수가 커지면 매 생산 단위(unit)마다 O(대기건수) 비용이 든다.

단순히 `self.waiting`을 `shortage` 오름차순으로 정렬해 앞에서부터 확인 후 조기 종료하는 방식은 안 된다 — `self.waiting`은 `assign_idle_lines()`가 `pop(0)`로 사용하는 **도착순(FIFO) 큐**이기도 하기 때문에, 정렬해버리면 "라인이 비면 먼저 접수된 주문부터 배정"이라는 Phase 8의 이미 검증된 보장이 깨진다.

## 목표

`assign_idle_lines()`의 FIFO 라인배정 순서를 그대로 유지하면서, `produce_unit()`의 확정 스캔만 평균적으로 더 빠르게 만든다.

## 설계

- `self.waiting`은 지금처럼 도착순 리스트로 그대로 둔다 (`assign_idle_lines`가 계속 이 순서로 `pop(0)`).
- 확정 스캔 전용 보조 구조를 추가한다: `sample_id`별로 `shortage` 오름차순을 유지하는 최소 구조(예: `heapq` 기반 min-heap, `self._waiting_by_shortage: dict[str, list]`).
- `enqueue()`, `assign_idle_lines()`(라인 배정으로 waiting에서 빠질 때), `produce_unit()`의 확정 처리(waiting에서 빠질 때) 시점에 이 보조 구조도 함께 갱신해 `self.waiting`과 항상 동기화한다.
- `produce_unit()`은 보조 구조에서 해당 `sample_id`의 최소 `shortage` 항목을 확인해, 현재 잉여로 충족 가능한 동안만 반복해서 꺼내 확정하고, 충족 불가능한 항목을 만나면 즉시 스캔을 중단한다.

## 필수 테스트 (회귀 방지 포함)

- [x] 최적화 적용 후에도 `assign_idle_lines()`가 여전히 도착순(FIFO)으로 배정하는지 테스트 — `shortage`가 서로 다른 여러 대기 작업을 도착 순서와 다른 `shortage` 순서로 채운 뒤 라인이 비었을 때 **도착순으로** 배정되는지 확인 (Phase 8 보장이 깨지지 않았음을 명시적으로 검증)
- [x] 최적화 적용 후에도 Phase 9의 PRD 6.2 시나리오(100ea/20ea, 누적 120에서 20ea 먼저 CONFIRMED)가 그대로 통과하는지 회귀 테스트
- [x] `shortage`가 서로 다른 여러 대기 주문이 섞여 있을 때, 잉여가 가장 작은 `shortage`부터 순서대로(도착순이 아니라 `shortage` 오름차순으로) 확정되는지 테스트
- [x] 스캔이 불필요하게 전체를 순회하지 않고 첫 미충족 항목에서 멈추는지 확인할 수 있는 테스트 (예: 매우 큰 `shortage`를 가진 항목들을 다수 넣어도, 그보다 작은 `shortage` 항목이 없으면 확정 시도 자체가 곧바로 끝나는지 — 호출 횟수/조기 종료를 관찰 가능한 형태로 검증)

## 구현 시 발견한 이슈

- 기존 Phase9/10/20 테스트들이 `queue.waiting.append(job)`으로 직접 리스트에 넣고 있었는데, 이는 애초에 캡슐화를 깨는 방식이었다. 이번 최적화로 `enqueue()`를 거쳐야만 보조 힙 구조와 동기화되므로, 그 테스트들을 전부 `queue.enqueue(job)` 호출로 수정했다 (동작 의도는 동일, 호출 경로만 정상화).
- 조기종료를 관찰 가능하게 검증하려면 확정 판정 시점에 `job.shortage`를 실시간으로 읽어야 해서 (힙 push 시점에 저장해둔 값이 아니라), `_drain_confirmable`에서 힙 튜플의 저장값 대신 `candidate.shortage`를 그때그때 읽도록 구현했다.
