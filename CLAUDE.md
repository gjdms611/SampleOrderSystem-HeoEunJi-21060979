# CLAUDE.md

이 프로젝트는 반도체 시료 생산주문관리 시스템이다. Agentic Engineering(Explore-Plan-Action) 절차를 순서대로 지킨다.

## Explore-Plan-Action 워크플로우 (필수, 순서 고정)

```
Explore (PRD.md)  ->  Plan (Plan.md)  ->  Action (구현)
```

1. **Explore**: `PRD.md` 작성/갱신. 도메인 모델, 주문 상태머신, 역할별 권한, 메인 메뉴 5종, 생산라인 계산식 정의 (`요구사항.md` 참고). PRD.md 없이 Plan/Action 단계로 넘어가지 않는다.
2. **Plan**: `Plan.md` 작성. 모듈/기능 단위 TODO로 분해. 이 단계부터는 로컬 skill `tdd-skill`(`.claude/skills/tdd-skill/SKILL.md`)을 그대로 사용한다 — tdd-skill의 RED 단계(Plan.md 작성 + 실패하는 테스트 + 인간 검토 + 커밋)가 이 Plan 단계에 해당한다.
3. **Action**: Plan.md에 따라 구현. tdd-skill의 GREEN(최소 구현) → REVIEW(Plan 대비 검토 + 인간 검토 + 커밋) 사이클을 그대로 따른다. Plan.md 범위를 벗어난 구현 금지.

## 기술 스택

- 언어: Python
- 데이터 저장: 파일 기반(JSON)

## 커밋 규칙

- PRD.md, Plan.md, 구현 코드는 모두 파일로 저장 후 커밋한다.
- 최소한 RED(Plan.md+테스트)와 REVIEW(구현) 커밋은 분리한다 (tdd-skill 체크리스트 기준).
- Explore 단계 산출물(PRD.md)도 별도 커밋으로 남긴다.
- 기능/작업 단위로 커밋을 분리해 의미 단위 커밋 이력을 유지한다.

## CleanCode 원칙

- 중복 코드 제거
- 명확한 네이밍
- 계층 분리 유지(예: MVC 등 역할 분리)

## 테스트 요구사항

- Unit Test(필수): 상태전이 로직, 재고계산, 수율계산 등 핵심 로직 검증
- E2E Test(권장): 메인 메뉴 콘솔 흐름 전체 시나리오 검증
- 상태머신 전이 케이스별 테스트를 각각 필수로 작성:
  - RESERVED -> REJECTED
  - RESERVED -> CONFIRMED (재고 충분 경로)
  - RESERVED -> PRODUCING -> CONFIRMED (재고 부족 후 생산 완료 경로)
  - CONFIRMED -> RELEASE

## 문서 관리

- CLAUDE.md에 프로젝트 컨벤션, 아키텍처(계층 구조/주요 모듈 구성), 작업 규칙을 기록한다.
- PRD.md/Plan.md와 상호 참조를 유지한다.
- 주요 설계 변경 발생 시 CLAUDE.md를 갱신한다.

## Skill 사용 규칙

- 작업 시작 시 진입점은 로컬 skill `agentic-workflow`(`.claude/skills/agentic-workflow/SKILL.md`)다. 지금이 Explore/Plan/Action 중 어디인지 판단해 아래 두 스킬로 라우팅한다.
- Explore 단계(PRD.md 작성/갱신)에서는 로컬 skill `prd-skill`(`.claude/skills/prd-skill/SKILL.md`)을 사용한다.
- Plan/Action 단계, 즉 새 기능/버그수정/구현 작업에는 `tdd-skill`을 사용한다.

## 참고 문서

- `요구사항.md`: Explore 단계 상세 요구사항 (PRD.md 내용)
