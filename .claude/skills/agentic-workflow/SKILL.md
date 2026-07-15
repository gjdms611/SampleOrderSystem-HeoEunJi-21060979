---
name: agentic-workflow
description: 이 레포(SampleOrderSystem)에서 진행하는 모든 작업의 진입점. Agentic Engineering(Explore-Plan-Action) 전체 흐름을 prd-skill과 tdd-skill로 라우팅하며 단계 순서를 강제한다. "이 프로젝트 작업 시작해줘", "다음 기능 진행해줘", "워크플로우대로 해줘", "PRD/Plan 상태 확인해줘" 같은 요청뿐 아니라, 지금이 Explore/Plan/Action 중 어느 단계인지 애매한 모든 순간에 먼저 트리거되어야 함. prd-skill이나 tdd-skill을 단독으로 어느 것을 먼저 부를지 판단이 안 설 때도 이 스킬부터 사용한다.
---

# Agentic Workflow (Explore-Plan-Action 진입점)

## 개요

이 스킬은 새로운 스킬이 아니라 **라우터**다. `prd-skill`과 `tdd-skill`을 대체하지 않는다 — 지금이 Explore/Plan/Action 중 어디인지 판단해서 맞는 스킬로 넘겨주고, 단계를 건너뛰지 못하게 순서를 강제하는 역할만 한다.

```
Explore (PRD.md)  --[승인+커밋]-->  Plan (Plan.md, tdd-skill RED)  --[승인+커밋]-->  Action (구현, tdd-skill GREEN/REVIEW)  --[승인+커밋]--> 다음 사이클
```

**핵심 원칙:** 앞 단계가 사람 승인 + 커밋으로 끝나지 않았다면 다음 단계로 넘어가지 않는다. 이 게이트가 없으면 잘못된 요구사항 위에 계획을 쌓고, 잘못된 계획 위에 코드를 쌓게 된다 — 되돌리는 비용이 각 단계마다 기하급수적으로 커진다.

## 1단계: 지금 어디에 있는지 판단하라

작업을 시작하기 전에 레포 상태를 확인한다:

1. `PRD.md`가 레포 루트에 있는가? 있다면 이번에 다루려는 기능/요구사항이 이미 반영돼 있는가?
2. 진행하려는 기능 단위의 `Plan.md`가 있고, 사람 승인을 받아 커밋됐는가?
3. `Plan.md`에 따른 구현이 아직 GREEN/REVIEW 사이클 중인가, 이미 끝나서 커밋됐는가?

이 판단 결과에 따라 아래 표로 다음 행동을 정한다. 여러 조건이 동시에 해당하면 표의 위에서부터(Explore 우선) 적용한다.

| 상태 | 다음 행동 |
|---|---|
| PRD.md 없음, 또는 다루려는 요구사항이 PRD.md에 없음/최신이 아님 | `prd-skill` 트리거 (Explore) |
| PRD.md는 승인+커밋됐지만, 이번 기능의 Plan.md가 없음 | `tdd-skill` 트리거, RED 단계부터 (Plan) |
| Plan.md는 승인+커밋됐지만, 구현이 아직 없거나 REVIEW 전 | `tdd-skill` 트리거, GREEN/REVIEW 단계부터 (Action) |
| 이번 기능의 구현까지 승인+커밋 완료 | 다음 기능으로 이동 — 다시 표 맨 위부터 판단 |

불확실하면 사람 파트너에게 "지금 Explore/Plan/Action 중 어디부터 시작할지" 짧게 확인하고 시작하라. 잘못 짚고 진행하는 것보다 한 줄 질문이 싸다.

## 2단계: 해당 스킬을 그대로 따른다

이 스킬은 각 단계의 세부 절차(요구사항 수집, PRD 작성, Plan.md 작성, RED-GREEN-REVIEW, 인간 검토 지점, 커밋 시점)를 다시 정의하지 않는다 — `prd-skill`과 `tdd-skill`이 이미 정의한 절차와 인간 검토 체크포인트를 그대로 따른다. 이 스킬의 역할은 순서를 정하고 건너뛰지 못하게 막는 것으로 끝난다.

## 위험 신호 (Red Flags) - 멈추고 표로 돌아가라

- "PRD.md 검토는 아직인데 Plan.md부터 써둘게요, 어차피 크게 안 바뀔 거예요" - Explore 승인 전에 Plan을 시작하면 게이트가 무의미해진다
- "Plan.md 커밋 전에 일단 코드부터 짜볼게요" - Action은 Plan 승인+커밋 이후에만 시작한다
- "이번엔 사이클이 작으니 Explore/Plan 단계는 생략할게요" - 사이클 크기와 무관하게 세 단계와 두 번의 인간 승인은 유지한다 (아주 사소한 오탈자/서식 수정 등 도메인 규칙 변경이 없는 예외는 prd-skill/tdd-skill 각각의 예외 규정을 따른다)
- 어느 스킬을 불러야 할지 몰라서 아무 스킬도 안 부르고 바로 구현/문서 작성 - 판단이 안 서면 이 스킬로 다시 돌아와 표를 다시 짚어라

## 완료 체크리스트

한 기능 사이클을 완료로 표시하기 전에:

- [ ] PRD.md가 이번 기능의 요구사항을 반영하고, 승인+커밋됐다
- [ ] Plan.md가 이번 기능 범위로 작성되고, 승인+커밋됐다 (tdd-skill RED)
- [ ] 구현이 Plan.md 범위 내에서 끝났고, 승인+커밋됐다 (tdd-skill GREEN/REVIEW)
- [ ] 세 산출물(PRD/Plan/구현)이 각각 별도 커밋으로 남아있다

## 참고 문서

- `CLAUDE.md`: Explore-Plan-Action 워크플로우와 커밋 규칙의 원본 정의
- `prd-skill`, `tdd-skill`: 각 단계의 실제 절차
