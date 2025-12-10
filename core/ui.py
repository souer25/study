# core/ui.py
from rich.panel import Panel        # ← 必须加上这行
from rich.table import Table
from rich.console import Console
from core.operations import students

console = Console()

console = Console()

def show_ranking():
    if not students:
        console.print("[yellow]暂无学生数据[/yellow]")
        return
    
    table = Table(title="[bold magenta]成绩排行榜 TOP[/]", show_header=True, header_style="bold cyan")
    table.add_column("排名", style="bold yellow", justify="center")
    table.add_column("姓名", style="green")
    table.add_column("成绩", style="bold white")
    
    for rank, (name, score) in enumerate(sorted(students.items(), key=lambda x: x[1], reverse=True), 1):
        if score >= 90:
            score_str = f"[bold green]{score}[/]"
        elif score >= 60:
            score_str = f"[bold yellow]{score}[/]"
        else:
            score_str = f"[bold red]{score}[/]"
        table.add_row(f"#{rank}", name, score_str)
    
    console.print(table)

def show_statistics():
    if not students:
        console.print("[yellow]暂无数据可统计[/yellow]")
        return
    
    scores = list(students.values())
    avg = sum(scores) / len(scores)
    passed = sum(1 for s in scores if s >= 60)
    
    console.print(Panel.fit(
        f"[bold cyan]平均分：[bold white]{avg:.1f}[/]\n"
        f"[bold cyan]最高分：[bold green]{max(scores)}[/]\n"
        f"[bold cyan]最低分：[bold red]{min(scores)}[/]\n"
        f"[bold cyan]及格人数：[yellow]{passed}[/] 人\n"
        f"[bold cyan]及格率：[bold magenta]{passed/len(scores)*100:.1f}%[/]",
        title="[bold blue]成绩统计总览[/]",
        border_style="bright_blue"
    ))