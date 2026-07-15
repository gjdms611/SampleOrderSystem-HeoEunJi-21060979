# Phase 1: Sample 엔티티 생성/검증

계층: model

## 목표
`Sample(sample_id, name, avg_production_time, yield_rate)` 생성 시 값을 그대로 보관하고, 잘못된 값이면 즉시 에러.

## 설계
- 파일: `model/sample.py`
- 시그니처: `class Sample: def __init__(self, sample_id: str, name: str, avg_production_time: float, yield_rate: float)`
- 검증 규칙: `avg_production_time > 0`, `0 < yield_rate <= 1`. 위반 시 `ValueError`.

## 엣지 케이스
- `avg_production_time == 0`, 음수
- `yield_rate == 0`, `yield_rate > 1`

## 완료 조건
- [x] 정상 생성 테스트
- [x] avg_production_time 검증 테스트
- [x] yield_rate 검증 테스트
