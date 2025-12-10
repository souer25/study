# main.py  ← Day9 炫彩终极版（只依赖 rich，永不翻车）
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import track
from rich import print as rprint
import time
import shutil
from datetime import datetime

from core.operations import add, delete, modify, query
from core.ui import show_ranking, show_statistics
from core.storage import save_data, DATA_FILE
from core.operations import students   # ← 正确位置！students 在 operations 里

console = Console()

def welcome_animation():
    console.clear()
    title = Panel.fit(
        "[bold magenta]学生成绩管理系统 v9.0[/]\n[cyan]炫彩富文本 • 极致美观 • 数据永存[/]",
        style="bold white on #4a148c",
        border_style="bright_magenta"
    )
    console.print(title)
    for _ in track(range(100), description="[green]正在启动系统..."):
        time.sleep(0.015)
    rprint("\n[bold green]系统启动成功！欢迎使用！[/bold green]\n")

def auto_backup():
    if students and DATA_FILE.exists():
        backup_dir = DATA_FILE.parent / "backup"
        backup_dir.mkdir(exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = backup_dir / f"backup_{timestamp}.json"
        shutil.copy2(DATA_FILE, backup_file)
        console.print(f"[dim]自动备份完成 → {backup_file.name}[/]")

def main():
    welcome_animation()
    
    while True:
        console.rule("[bold blue]主菜单[/bold blue]", style="cyan")
        
        table = Table(show_header=True, header_style="bold yellow")
        table.add_column("选项", style="cyan", justify="center")
        table.add_column("功能", style="green")
        
        menu_items = ["添加学生", "删除学生", "修改成绩", "查询学生", "排行榜", "统计信息", "退出"]
        for i, item in enumerate(menu_items, 1):
            table.add_row(str(i), item)
        
        console.print(table)
        
        choice = console.input("\n[bold white]请选择功能 [1-7]: [/]").strip()
        
        match choice:
            case "1": add()
            case "2": delete()
            case "3": modify()
            case "4": query()
            case "5": show_ranking()
            case "6": show_statistics()
            case "7": 
                auto_backup()
                console.print(Panel(
                    "[bold red]感谢使用！所有数据已永久保存[/bold red]\n[bold cyan]明天见！[/bold cyan]",
                    style="white on #8B0000",
                    expand=False
                ))
                time.sleep(1.5)
                break
            case _: 
                console.print("[bold red]输入有误，请重新选择！[/bold red]")

if __name__ == "__main__":
    main()