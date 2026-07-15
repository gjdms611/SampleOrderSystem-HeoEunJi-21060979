# Phase 30: 입력 중 취소(뒤로가기) 지원

계층: view + controller

## 배경

지금 콘솔 구조(input() 순차 흐름)에서는 서브메뉴에 진입해 값을 입력하는 도중에는 취소하고 메인 메뉴로 돌아갈 방법이 없다. 예를 들어 시료 등록 중 잘못된 값을 입력했거나 그냥 등록을 그만두고 싶어도 끝까지 입력을 마쳐야 한다.

완전한 화면 스택/네비게이션(Textual 전환에서 다룰 영역)까지는 아니어도, "입력 도중 취소 가능"은 지금 구조로도 충분히 구현 가능하다.

## 목표

각 입력 프롬프트에서 아무것도 입력하지 않고 그냥 Enter(빈 입력)를 누르면 그 작업을 취소하고 상위 메뉴로 돌아간다. 이미 값을 일부 입력했더라도, 그 뒤 프롬프트에서 빈 입력을 주면 지금까지 입력한 것을 버리고 취소한다.

## 설계

- `view/console_view.py`: 텍스트 입력을 받는 프롬프트 함수들(`prompt_sample_register`, `prompt_search_keyword`, `prompt_order_submit`, `prompt_order_id`)이 빈 입력(공백만 입력해도 취소로 간주)을 받으면, 값 대신 취소를 뜻하는 특별한 값(`None`)을 반환한다.
  - `prompt_sample_register()`: 시료ID를 비워서 Enter → 전체 등록 취소, `(None, None, None, None)` 반환.
  - `prompt_order_submit()`: 고객명을 비워서 Enter → 전체 접수 취소, `(None, None, None)` 반환.
  - `prompt_search_keyword()`, `prompt_order_id()`: 빈 입력이면 `None` 반환.
  - `prompt_float`/`prompt_int`는 이 Phase에서 건드리지 않는다 (등록 흐름의 첫 필드에서만 취소 판단하고, 숫자 필드 자체는 여전히 재시도 루프).
- `controller/main_controller.py`: 각 흐름에서 프롬프트 결과가 `None`(취소)이면 controller를 호출하지 않고 "취소되었습니다" 안내 후 메인 메뉴로 돌아간다.

## 완료 조건

- [x] 시료 등록 중 시료ID를 비우고 Enter 시 등록이 취소되고 메인 메뉴로 돌아가는지 확인
- [x] 주문 접수 중 고객명을 비우고 Enter 시 접수가 취소되는지 확인
- [x] 검색/주문ID 입력에서 빈 입력 시 취소되는지 확인
- [x] `python main.py`로 전체 흐름 수동 확인
