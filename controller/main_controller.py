from view import console_view

TBD_MESSAGE = "TBD (Phase 18~20 구현 후 연결 예정)"


class MainController:
    def __init__(self, sample_controller):
        self.sample_controller = sample_controller

    def run(self) -> None:
        while True:
            choice = console_view.show_main_menu()
            if choice == "0":
                return
            elif choice == "1":
                self._handle_sample_menu()
            elif choice in ("2", "3", "4", "5"):
                console_view.show_message(TBD_MESSAGE)
            else:
                console_view.show_message("잘못된 선택입니다.")

    def _handle_sample_menu(self) -> None:
        action = input("1. 등록 2. 조회 3. 검색\n선택> ").strip()
        if action == "1":
            sample_id, name, avg_production_time, yield_rate = console_view.prompt_sample_register()
            sample = self.sample_controller.register(sample_id, name, avg_production_time, yield_rate)
            console_view.show_sample(sample)
        elif action == "2":
            sample_id = console_view.prompt_sample_id()
            sample = self.sample_controller.get(sample_id)
            console_view.show_sample(sample)
        elif action == "3":
            keyword = console_view.prompt_search_keyword()
            samples = self.sample_controller.search(keyword)
            console_view.show_samples(samples)
        else:
            console_view.show_message("잘못된 선택입니다.")
