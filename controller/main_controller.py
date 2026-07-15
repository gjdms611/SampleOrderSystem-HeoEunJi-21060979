from view import console_view


class MainController:
    def __init__(self, sample_controller, order_controller, monitoring_controller, line_controller):
        self.sample_controller = sample_controller
        self.order_controller = order_controller
        self.monitoring_controller = monitoring_controller
        self.line_controller = line_controller

    def run(self) -> None:
        while True:
            choice = console_view.show_main_menu()
            if choice == "0":
                return
            elif choice == "1":
                self._handle_sample_menu()
            elif choice == "2":
                self._handle_order_menu()
            elif choice == "3":
                self._handle_monitoring_menu()
            elif choice == "4":
                self._handle_release_menu()
            elif choice == "5":
                self._handle_production_line_menu()
            else:
                console_view.show_message("잘못된 선택입니다.")

    def _handle_sample_menu(self) -> None:
        action = input("1. 등록 2. 조회 3. 검색\n선택> ").strip()
        if action == "1":
            sample_id, name, avg_production_time, yield_rate = console_view.prompt_sample_register()
            if sample_id is None:
                console_view.show_message("취소되었습니다.")
                return
            sample, is_new = self.sample_controller.register(sample_id, name, avg_production_time, yield_rate)
            if not is_new:
                console_view.show_message("이미 등록된 시료ID입니다. 기존 정보:")
            console_view.show_sample(sample)
        elif action == "2":
            samples = self.sample_controller.list_all()
            console_view.show_samples(samples)
        elif action == "3":
            keyword = console_view.prompt_search_keyword()
            if keyword is None:
                console_view.show_message("취소되었습니다.")
                return
            samples = self.sample_controller.search(keyword)
            console_view.show_samples(samples)
        else:
            console_view.show_message("잘못된 선택입니다.")

    def _handle_order_menu(self) -> None:
        action = input("1. 접수 2. 승인 3. 거절 4. 취소\n선택> ").strip()
        if action == "1":
            customer_name, sample_id, quantity = console_view.prompt_order_submit()
            if customer_name is None:
                console_view.show_message("취소되었습니다.")
                return
            order = self.order_controller.submit(customer_name, sample_id, quantity)
            console_view.show_order(order)
        elif action == "2":
            order_id = console_view.prompt_order_id()
            if order_id is None:
                console_view.show_message("취소되었습니다.")
                return
            order = self.order_controller.approve(order_id)
            console_view.show_order(order)
        elif action == "3":
            order_id = console_view.prompt_order_id()
            if order_id is None:
                console_view.show_message("취소되었습니다.")
                return
            order = self.order_controller.reject(order_id)
            console_view.show_order(order)
        elif action == "4":
            order_id = console_view.prompt_order_id()
            if order_id is None:
                console_view.show_message("취소되었습니다.")
                return
            order = self.order_controller.cancel(order_id)
            console_view.show_order(order)
        else:
            console_view.show_message("잘못된 선택입니다.")

    def _handle_monitoring_menu(self) -> None:
        action = input("1. 주문상태별 카운트 2. 재고 판정\n선택> ").strip()
        if action == "1":
            counts = self.monitoring_controller.count_orders_by_status()
            console_view.show_status_counts(counts)
        elif action == "2":
            judgements = self.monitoring_controller.judge_all_stock()
            console_view.show_stock_judgement(judgements)
        else:
            console_view.show_message("잘못된 선택입니다.")

    def _handle_release_menu(self) -> None:
        order_id = console_view.prompt_order_id()
        if order_id is None:
            console_view.show_message("취소되었습니다.")
            return
        order = self.order_controller.release_order(order_id)
        console_view.show_order(order)

    def _handle_production_line_menu(self) -> None:
        current_jobs = self.line_controller.current_jobs()
        waiting_jobs = self.line_controller.waiting_jobs()
        console_view.show_production_lines(current_jobs, waiting_jobs)
