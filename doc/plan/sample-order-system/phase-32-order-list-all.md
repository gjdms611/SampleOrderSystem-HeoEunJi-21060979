# Phase 32: 주문 전체 목록 조회

계층: controller + view

## 배경

주문을 승인/거절/취소하려면 order_id를 알아야 하는데, 지금 주문 메뉴에는 현재 어떤 주문이 있는지 보는 방법이 없다 (시료관리의 "조회"에 대응하는 기능이 주문 메뉴엔 없음).

## 목표

주문 메뉴에 "전체조회" 옵션을 추가해 등록된 모든 주문(order_id/고객명/시료ID/수량/상태)을 목록으로 보여준다.

## 설계

- `controller/order_controller.py`에 `list_all(self) -> list[Order]` 추가: `self.order_repo.find_all()` 위임.
- `view/console_view.py`에 `show_orders(orders) -> None` 추가: 목록이 없으면 안내, 있으면 `show_order`와 같은 컬럼(주문ID/고객명/시료ID/수량/상태) 표로 출력.
- `controller/main_controller.py`의 주문 서브메뉴에 "5. 전체조회" 추가 (`1.접수 2.승인 3.거절 4.취소 5.전체조회`).

## 완료 조건

- [ ] `OrderController.list_all()`이 저장된 모든 주문을 반환하는지 테스트
- [ ] `python main.py`로 주문 메뉴에서 전체조회 시 등록된 주문 목록이 보이는지 수동 확인
