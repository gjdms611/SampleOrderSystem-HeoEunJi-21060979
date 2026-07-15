MAIN_MENU_TEXT = """
=== 반도체 시료 생산주문관리 시스템 ===
1. 시료관리 (등록/조회/검색)
2. 주문 (접수/승인/거절/취소)
3. 모니터링 (주문상태/재고판정)
4. 출고처리
5. 생산라인 조회
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


def prompt_order_submit():
    customer_name = input("고객명: ").strip()
    sample_id = input("시료ID: ").strip()
    quantity = int(input("수량: ").strip())
    return customer_name, sample_id, quantity


def prompt_order_id() -> str:
    return input("주문ID: ").strip()


def show_order(order) -> None:
    if order is None:
        print("처리할 수 없습니다 (주문을 찾을 수 없거나 현재 상태에서 허용되지 않는 처리입니다).")
        return
    print(
        f"[{order.order_id}] {order.customer_name} / 시료={order.sample_id} "
        f"/ 수량={order.quantity} / 상태={order.status.value}"
    )


def show_status_counts(counts) -> None:
    if not counts:
        print("등록된 주문이 없습니다.")
        return
    for status, count in counts.items():
        print(f"{status.value}: {count}건")


def show_stock_judgement(judgements) -> None:
    if not judgements:
        print("등록된 재고가 없습니다.")
        return
    for sample_id, status in judgements.items():
        print(f"{sample_id}: {status.value}")


def show_production_lines(current_jobs, waiting_jobs) -> None:
    print("--- 생산중 ---")
    if not current_jobs:
        print("생산중인 작업이 없습니다.")
    for job in current_jobs:
        print(f"주문={job.order_id} 시료={job.sample_id} 진행={job.produced_qty}/{job.actual_qty}")

    print("--- 대기중 ---")
    if not waiting_jobs:
        print("대기중인 작업이 없습니다.")
    for job in waiting_jobs:
        print(f"주문={job.order_id} 시료={job.sample_id} 부족분={job.shortage}")


def show_message(message: str) -> None:
    print(message)
