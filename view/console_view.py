from datetime import datetime

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
    sample_id = console.input("시료ID (취소하려면 빈 값으로 Enter): ").strip()
    if not sample_id:
        return None, None, None, None
    name = console.input("이름: ").strip()
    avg_production_time = prompt_float("평균생산시간: ")
    yield_rate = prompt_float("수율(0~1): ")
    return sample_id, name, avg_production_time, yield_rate


def prompt_search_keyword():
    keyword = console.input(
        "검색 키워드 (시료 이름의 일부를 입력하세요. 예: Wafer-A, Wafer, Chip. 취소하려면 빈 값으로 Enter): "
    ).strip()
    return keyword if keyword else None


def show_sample(sample_with_quantity) -> None:
    if sample_with_quantity is None:
        show_message("해당 시료를 찾을 수 없습니다.", error=True)
        return
    show_samples([sample_with_quantity])


def show_samples(samples) -> None:
    if not samples:
        show_message("검색 결과가 없습니다.")
        return
    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("시료ID")
    table.add_column("이름")
    table.add_column("평균생산시간")
    table.add_column("수율")
    table.add_column("재고")
    for sample, quantity in samples:
        table.add_row(
            sample.sample_id, sample.name, str(sample.avg_production_time), str(sample.yield_rate), str(quantity)
        )
    console.print(table)


def prompt_order_submit():
    customer_name = console.input("고객명 (취소하려면 빈 값으로 Enter): ").strip()
    if not customer_name:
        return None, None, None
    sample_id = console.input("시료ID: ").strip()
    quantity = prompt_int("수량: ")
    return customer_name, sample_id, quantity


def prompt_order_id():
    order_id = console.input("주문ID (취소하려면 빈 값으로 Enter): ").strip()
    return order_id if order_id else None


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


def show_orders(orders) -> None:
    if not orders:
        show_message("등록된 주문이 없습니다.")
        return
    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("주문ID")
    table.add_column("고객명")
    table.add_column("시료ID")
    table.add_column("수량")
    table.add_column("상태")
    for order in orders:
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


def show_production_line_screen(line_count, running_count, current_rows, waiting_rows) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    console.print(f"[bold]생산라인 {line_count}개 (가동중 {running_count} / 유휴 {line_count - running_count})[/bold]  현재시각 {now}")

    if not current_rows:
        show_message("생산중인 작업이 없습니다.")
    else:
        current_table = Table(title="처리중", show_header=True, header_style="bold green")
        for column in ("주문번호", "시료", "주문량", "재고", "부족분", "실생산량", "수율", "진행률", "예상완료시각"):
            current_table.add_column(column)
        for row in current_rows:
            progress_pct = int(row["progress_ratio"] * 100)
            current_table.add_row(
                row["order_id"],
                row["sample_name"],
                str(row["quantity"]),
                str(row["inventory"]),
                str(row["shortage"]),
                f"{row['produced_qty']}/{row['actual_qty']}",
                f"{row['yield_rate'] * 100:.0f}%",
                f"{progress_pct}%",
                row["expected_completion_at"].strftime("%Y-%m-%d %H:%M:%S"),
            )
        console.print(current_table)

    if not waiting_rows:
        show_message("대기중인 작업이 없습니다.")
    else:
        waiting_table = Table(title="대기중 (FIFO)", show_header=True, header_style="bold yellow")
        for column in ("순서", "주문번호", "시료", "주문량", "부족분", "실생산량"):
            waiting_table.add_column(column)
        for row in waiting_rows:
            waiting_table.add_row(
                str(row["position"]),
                row["order_id"],
                row["sample_name"],
                str(row["quantity"]),
                str(row["shortage"]),
                str(row["actual_qty"]),
            )
        console.print(waiting_table)


def show_message(message: str, error: bool = False) -> None:
    style = "red" if error else "yellow"
    prefix = "오류" if error else "안내"
    console.print(f"[{style}][{prefix}] {message}[/{style}]")
