# 반도체 시료 생산주문관리 시스템 (S-Semi)

가상회사 **S-Semi**의 반도체 시료 생산주문관리 시스템이다. 고객 요청(이메일 등 시스템 외부)을 주문담당자가 시스템에 접수하면, 생산담당자가 승인/거절하고, 재고가 부족하면 생산라인에 자동 등록되어 생산 완료 후 출고까지 이어지는 흐름을 관리한다.

## 무엇을 관리하는 시스템인가

```mermaid
flowchart TD
    START([시작]) --> RESERVED[RESERVED\n주문 등록]
    RESERVED --> 승인여부확인{승인 여부}
    승인여부확인 -->|거절| REJECTED[REJECTED\n거절]
    승인여부확인 -->|승인| 재고확인{재고 확인}
    재고확인 -->|재고충분| CONFIRMED[CONFIRMED\n출고 준비]
    재고확인 -->|재고부족\n생산라인 자동등록| PRODUCING[PRODUCING\n생산 요청]
    PRODUCING -->|생산완료| CONFIRMED
    CONFIRMED -->|출고처리| RELEASE[RELEASE\n출고 처리]
    REJECTED --> END1([종료])
    RELEASE --> END2([종료: 고객 도달])
```

주문 하나는 시료(Sample) 1종 + 수량으로 구성되고, 위 상태머신을 따라 이동한다. 재고가 부족하면 부족분만큼 자동으로 생산 작업이 잡히고(수율/생산시간 계산 포함), 생산이 끝나면 잉여분까지 재고에 반영된 뒤 주문이 CONFIRMED로 넘어간다.

## 아키텍처

MVC(model/view/controller)아키텍쳐를 사용하며, 데이터 영속성 보장을 위해  storage/repository 두 계층을 추가해 총 5계층으로 구성한다.

```
main.py       - model/view/controller/repository 조립 진입점
view/         - 메인 메뉴 5종 콘솔 입출력(input/print)만. 비즈니스 로직 없음.
controller/   - 흐름 제어: view 입력 -> model/repository 호출 -> view 출력.
model/        - 엔티티(Sample, Inventory, Order, ...) + 상태머신 + 계산식. 순수 로직, IO 없음.
repository/   - CRUD 로직 (find/save/search). storage를 통해서만 파일 접근.
storage/      - JSON 파일 raw load/save. 순수 파일 IO.
```

의존 방향: `main.py → view/controller 조립 → controller → model`, `controller → repository → storage`. `model`은 다른 계층을 모른다.

## 실행 방법

표준 라이브러리만 사용하므로 별도 설치 없이 실행 가능하다. 레포 루트(`SampleOrderSystem/`)에서 실행한다.

```bash
python main.py
```

메뉴에서 `1`을 선택하면 시료 등록/조회/검색을 실제로 해볼 수 있다 (`data/samples.json`에 저장됨). `2`~`5`는 아직 `TBD` 안내만 나온다. `0`으로 종료.

> Windows 콘솔에서 한글이 깨져 보이면 `PYTHONUTF8=1 python main.py`로 실행한다 (콘솔 코드페이지 표시 문제일 뿐, 로직과는 무관).
