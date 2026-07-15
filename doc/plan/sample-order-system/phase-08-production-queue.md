# Phase 8: 생산대기큐 FIFO 등록 + 라인 배정

계층: model

## 목표
`ProductionJob`을 큐에 등록 순서대로 쌓고, 생산라인(N개, 기본 1)이 유휴 상태면 큐 맨 앞 작업을 즉시 배정.

## 설계
- 파일: `model/production_queue.py`
- `class ProductionQueue: def __init__(self, line_count: int = 1)`
- `enqueue(self, job: ProductionJob) -> None`
- `assign_idle_lines(self) -> None` (유휴 라인에 큐 맨 앞부터 배정)
- 속성: `self.lines: list[ProductionJob | None]`, `self.waiting: list[ProductionJob]`

## 엣지 케이스
- 라인이 모두 사용 중이면 큐에 대기
- 라인 유휴 시 여러 대기 작업을 한 번에 채움

## 완료 조건
- [x] FIFO 등록 순서 유지 테스트
- [x] 유휴 라인에 큐 맨 앞 작업 배정 테스트
- [x] 라인 N개(기본 1) 초과 시 대기 테스트
