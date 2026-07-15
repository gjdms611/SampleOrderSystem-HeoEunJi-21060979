# CLAUDE.md

이 프로젝트는 . Agentic Engineering(Explore-Plan-Action) 절차를 순서대로 지킨다. 채점 기준 충족 여부와 무관하게 아래 순서를 항상 지킨다.

## Explore-Plan-Action 워크플로우 (필수, 순서 고정)

```
Explore (PRD.md)  ->  Plan (Plan.md)  ->  Action (구현)
```

1. **Explore**: `PRD.md` 작성/갱신. 도메인 모델, 주문 상태머신, 역할별 권한, 메인 메뉴 5종, 생산라인 계산식 정의 (`domain-and-prd.md` 참고). PRD.md 없이 Plan/Action 단계로 넘어가지 않는다.
2. **Plan**: `Plan.md` 작성. 모듈/기능 단위 TODO로 분해. 이 단계부터는 로컬 skill `tdd-skill`(`.claude/skills/tdd-skill/SKILL.md`)을 그대로 사용한다 — tdd-skill의 RED 단계(Plan.md 작성 + 실패하는 테스트 + 인간 검토 + 커밋)가 이 Plan 단계에 해당한다.
3. **Action**: Plan.md에 따라 구현. tdd-skill의 GREEN(최소 구현) → REVIEW(Plan 대비 검토 + 인간 검토 + 커밋) 사이클을 그대로 따른다. Plan.md 범위를 벗어난 구현 금지.

## 커밋 규칙

- PRD.md, Plan.md, 구현 코드는 모두 파일로 저장 후 커밋한다.
- 최소한 RED(Plan.md+테스트)와 REVIEW(구현) 커밋은 분리한다 (tdd-skill 체크리스트 기준).
- Explore 단계 산출물(PRD.md)도 별도 커밋으로 남긴다.

## Skill 사용 규칙

- 새 기능/버그수정/구현 작업 전에는 반드시 `tdd-skill`을 트리거한다. 별도의 Explore-Plan-Action 전용 skill을 새로 만들지 않는다 — tdd-skill의 Plan.md/RED-GREEN-REVIEW 루프가 Plan+Action 단계를 이미 강제한다.
- Explore 단계(PRD.md 작성/도메인 정의)만 tdd-skill 범위 밖이므로, 이 문서(CLAUDE.md)가 그 부분을 명시적으로 보완한다.

## 참고 문서

- `domain-and-prd.md`: Explore 단계 상세 요구사항 (PRD.md 내용)
- `agentic-engineering-process.md`: 본 워크플로우 요구사항 원문
- `implementation-and-cleancode.md`, `testing-unit-e2e.md`, `claude-md-governance.md`: 후속 요구사항
