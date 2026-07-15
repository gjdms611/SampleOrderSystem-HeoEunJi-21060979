from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

MAIN_MENU_TEXT = (
    "[bold]1.[/bold] 시료관리   (등록/조회/검색)\n"
    "[bold]2.[/bold] 주문       (접수/승인/거절/취소)\n"
    "[bold]3.[/bold] 모니터링   (주문상태/재고판정)\n"
    "[bold]4.[/bold] 출고처리\n"
    "[bold]5.[/bold] 생산라인 조회\n"
    "[bold]0.[/bold] 종료"
)

STOCK_STATUS_STYLE = {
    "SUFFICIENT": ("여유", "green"),
    "SHORTAGE": ("부족", "yellow"),
    "DEPLETED": ("고갈", "red"),
}


def show_main_menu() -> str:
    console.print(Panel(MAIN_MENU_TEXT, title="반도체 시료 생산주문관리 시스템", style="cyan"))
    return console.input("[bold]선택> [/bold]").strip()


def prompt_float(message: str) -> float:
    while True:
        try:
            return float(console.input(message).strip())
        except ValueError:
            show_message("숫자를 입력해주세요.", error=True)


def prompt_int(message: str) -> int:
    while True:
        try:
            return int(console.input(message).strip())
        except ValueError:
            show_message("숫자를 입력해주세요.", error=True)


def prompt_sample_register():
    sample_id = console.input("시료ID: ").strip()
    name = console.input("이름: ").strip()
    avg_production_time = prompt_float("평균생산시간: ")
    yield_rate = prompt_float("수율(0~1): ")
    return sample_id, name, avg_production_time, yield_rate


def prompt_search_keyword() -> str:
    return console.input(
        "검색 키워드 (시료 이름의 일부를 입력하세요. 예: Wafer-A, Wafer, Chip): "
    ).strip()


def show_sample(sample) -> None:
    if sample is None:
        show_message("해당 시료를 찾을 수 없습니다.", error=True)
        return
    show_samples([sample])


def show_samples(samples) -> None:
    if not samples:
        show_message("검색 결과가 없습니다.")
        return
    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("시료ID")
    table.add_column("이름")
    table.add_column("평균생산시간")
    table.add_column("수율")
    for sample in samples:
        table.add_row(sample.sample_id, sample.name, str(sample.avg_production_time), str(sample.yield_rate))
    console.print(table)


def prompt_order_submit():
    customer_name = console.input("고객명: ").strip()
    sample_id = console.input("시료ID: ").strip()
    quantity = prompt_int("수량: ")
    return customer_name, sample_id, quantity


def prompt_order_id() -> str:
    return console.input("주문ID: ").strip()


def show_order(order) -> None:
    if order is None:
        show_message("처리할 수 없습니다 (주문을 찾을 수 없거나 현재 상태에서 허용되지 않는 처리입니다).", error=True)
        return
    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("주문ID")
    table.add_column("고객명")
    table.add_column("시료ID")
    table.add_column("수량")
    table.add_column("상태")
    table.add_row(order.order_id, order.customer_name, order.sample_id, str(order.quantity), order.status.value)
    console.print(table)


def show_status_counts(counts) -> None:
    if not counts:
        show_message("등록된 주문이 없습니다.")
        return
    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("상태")
    table.add_column("건수")
    for status, count in counts.items():
        table.add_row(status.value, str(count))
    console.print(table)


def show_stock_judgement(judgements) -> None:
    if not judgements:
        show_message("등록된 재고가 없습니다.")
        return
    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("시료ID")
    table.add_column("재고판정")
    for sample_id, status in judgements.items():
        label, style = STOCK_STATUS_STYLE.get(status.value, (status.value, "white"))
        table.add_row(sample_id, f"[{style}]{label}[/{style}]")
    console.print(table)


def show_production_lines(current_jobs, waiting_jobs) -> None:
    if not current_jobs:
        show_message("생산중인 작업이 없습니다.")
    else:
        current_table = Table(title="생산중", show_header=True, header_style="bold green")
        current_table.add_column("주문ID")
        current_table.add_column("시료ID")
        current_table.add_column("진행률")
        for job in current_jobs:
            progress = int(job.produced_qty / job.actual_qty * 100) if job.actual_qty else 0
            current_table.add_row(job.order_id, job.sample_id, f"{job.produced_qty}/{job.actual_qty} ({progress}%)")
        console.print(current_table)

    if not waiting_jobs:
        show_message("대기중인 작업이 없습니다.")
    else:
        waiting_table = Table(title="대기중", show_header=True, header_style="bold yellow")
        waiting_table.add_column("주문ID")
        waiting_table.add_column("시료ID")
        waiting_table.add_column("부족분")
        for job in waiting_jobs:
            waiting_table.add_row(job.order_id, job.sample_id, str(job.shortage))
        console.print(waiting_table)


def show_message(message: str, error: bool = False) -> None:
    style = "red" if error else "yellow"
    prefix = "오류" if error else "안내"
    console.print(f"[{style}][{prefix}] {message}[/{style}]")
