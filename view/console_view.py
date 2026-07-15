MAIN_MENU_TEXT = """
=== 반도체 시료 생산주문관리 시스템 ===
1. 시료관리 (등록/조회/검색)
2. 주문 접수/거절/취소
3. 주문 승인
4. 출고처리/모니터링/생산라인 조회
5. (예약)
0. 종료
선택> """


def show_main_menu() -> str:
    return input(MAIN_MENU_TEXT).strip()


def prompt_sample_register():
    sample_id = input("시료ID: ").strip()
    name = input("이름: ").strip()
    avg_production_time = float(input("평균생산시간: ").strip())
    yield_rate = float(input("수율(0~1): ").strip())
    return sample_id, name, avg_production_time, yield_rate


def prompt_sample_id() -> str:
    return input("조회할 시료ID: ").strip()


def prompt_search_keyword() -> str:
    return input("검색 키워드: ").strip()


def show_sample(sample) -> None:
    if sample is None:
        print("해당 시료를 찾을 수 없습니다.")
        return
    print(f"[{sample.sample_id}] {sample.name} (평균생산시간={sample.avg_production_time}, 수율={sample.yield_rate})")


def show_samples(samples) -> None:
    if not samples:
        print("검색 결과가 없습니다.")
        return
    for sample in samples:
        show_sample(sample)


def show_message(message: str) -> None:
    print(message)
