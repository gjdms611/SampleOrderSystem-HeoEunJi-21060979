MAIN_MENU_TEXT = """
==================================================
 반도체 시료 생산주문관리 시스템
==================================================
 1. 시료관리   (등록/조회/검색)
 2. 주문       (접수/승인/거절/취소)
 3. 모니터링   (주문상태/재고판정)
 4. 출고처리
 5. 생산라인 조회
 0. 종료
--------------------------------------------------
선택> """

STOCK_STATUS_LABELS = {
    "SUFFICIENT": "여유",
    "SHORTAGE": "부족",
    "DEPLETED": "고갈",
}


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
        print("[안내] 해당 시료를 찾을 수 없습니다.")
        return
    show_samples([sample])


def show_samples(samples) -> None:
    if not samples:
        print("[안내] 검색 결과가 없습니다.")
        return
    print(f"{'시료ID':<10}{'이름':<15}{'평균생산시간':<12}{'수율':<8}")
    print("-" * 45)
    for sample in samples:
        print(
            f"{sample.sample_id:<10}{sample.name:<15}"
            f"{sample.avg_production_time:<12}{sample.yield_rate:<8}"
        )


def prompt_order_submit():
    customer_name = input("고객명: ").strip()
    sample_id = input("시료ID: ").strip()
    quantity = int(input("수량: ").strip())
    return customer_name, sample_id, quantity


def prompt_order_id() -> str:
    return input("주문ID: ").strip()


def show_order(order) -> None:
    if order is None:
        print("[오류] 처리할 수 없습니다 (주문을 찾을 수 없거나 현재 상태에서 허용되지 않는 처리입니다).")
        return
    print("-" * 45)
    print(f"주문ID   : {order.order_id}")
    print(f"고객명   : {order.customer_name}")
    print(f"시료ID   : {order.sample_id}")
    print(f"수량     : {order.quantity}")
    print(f"상태     : {order.status.value}")
    print("-" * 45)


def show_status_counts(counts) -> None:
    if not counts:
        print("[안내] 등록된 주문이 없습니다.")
        return
    print(f"{'상태':<12}{'건수':<6}")
    print("-" * 20)
    for status, count in counts.items():
        print(f"{status.value:<12}{count:<6}")


def show_stock_judgement(judgements) -> None:
    if not judgements:
        print("[안내] 등록된 재고가 없습니다.")
        return
    print(f"{'시료ID':<10}{'재고판정':<8}")
    print("-" * 20)
    for sample_id, status in judgements.items():
        label = STOCK_STATUS_LABELS.get(status.value, status.value)
        print(f"{sample_id:<10}{label:<8}")


def show_production_lines(current_jobs, waiting_jobs) -> None:
    print("=" * 20 + " 생산중 " + "=" * 20)
    if not current_jobs:
        print("[안내] 생산중인 작업이 없습니다.")
    for job in current_jobs:
        progress = int(job.produced_qty / job.actual_qty * 100) if job.actual_qty else 0
        print(f"주문={job.order_id} 시료={job.sample_id} 진행={job.produced_qty}/{job.actual_qty} ({progress}%)")

    print("=" * 20 + " 대기중 " + "=" * 20)
    if not waiting_jobs:
        print("[안내] 대기중인 작업이 없습니다.")
    for job in waiting_jobs:
        print(f"주문={job.order_id} 시료={job.sample_id} 부족분={job.shortage}")


def show_message(message: str) -> None:
    print(f"[안내] {message}")
