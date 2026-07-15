# Phase 33: 승인 대기중(RESERVED) 주문만 조회

계층: controller + view

## 배경

Phase32의 "전체조회"는 모든 상태의 주문을 다 보여준다. 실제로 승인/거절 작업을 하려는 사용자는 RESERVED(아직 처리 안 된) 주문만 빠르게 보고 싶은 경우가 많다. 전체조회와 별도로 "승인 대기중만 조회"를 추가한다.

## 목표

주문 메뉴에 "승인대기 조회" 옵션을 추가해 RESERVED 상태인 주문만 필터링해서 보여준다.

## 설계

- `controller/order_controller.py`에 `list_pending(self) -> list[Order]` 추가: `self.order_repo.find_all()` 중 `status == OrderStatus.RESERVED`인 것만 필터링해 반환.
- `controller/main_controller.py`의 주문 서브메뉴에 "6. 승인대기 조회" 추가 (`1.접수 2.승인 3.거절 4.취소 5.전체조회 6.승인대기 조회`).
- view는 기존 `show_orders()`를 그대로 재사용한다(목록이 RESERVED만으로 필터링된 채로 넘어올 뿐, 출력 형식은 동일).

## 완료 조건

- [x] `OrderController.list_pending()`이 RESERVED 상태 주문만 반환하는지(다른 상태는 제외) 테스트
- [x] `python main.py`로 승인대기 조회 시 RESERVED 주문만 보이는지 수동 확인
