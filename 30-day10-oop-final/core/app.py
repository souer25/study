# core/app.py
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import track
from rich import print as rprint
import time
import shutil
from datetime import datetime

from core.storage import save_data, DATA_FILE
from core.student import Student

class ScoreApp:
    def __init__(self):
        self.console = Console()
        self.students = self._load_students()
    
    def _load_students(self):
        raw = {}
        if DATA_FILE.exists():
            import json
            try:
                raw = json.loads(DATA_FILE.read_text(encoding="utf-8"))
            except:
                pass
        return {name: Student(name, score) for name, score in raw.items()}
    
    def _save(self):
        data = {s.name: s.score for s in self.students.values()}
        save_data(data)
    
    def run(self):
        self._welcome()
        while True:
            self._show_menu()
            choice = self.console.input("\n[bold white]请选择 [1-7]: [/]").strip()
            if choice == "1": self._add()
            elif choice == "2": self._delete()
            elif choice == "3": self._modify()
            elif choice == "4": self._query()
            elif choice == "5": self._ranking()
            elif choice == "6": self._stats()
            elif choice == "7": self._exit(); break
            else: self.console.print("[bold red]输入错误！[/]")
    
    def _welcome(self):
        self.console.clear()
        self.console.print(Panel.fit(
            "[bold magenta]学生成绩管理系统 v10.0[/]\n[cyan]面向对象终极版 • 数据永存 • 准备上云[/]",
            style="bold white on purple", border_style="bright_magenta"
        ))
        for _ in track(range(100), description="[green]正在启动..."):
            time.sleep(0.01)
        rprint("\n[bold green]系统启动成功！[/]\n")
    
    def _show_menu(self):
        self.console.rule("[bold blue]主菜单[/]", style="cyan")
        table = Table(show_header=False)
        table.add_column("选项", style="cyan")
        table.add_column("功能", style="green")
        for i, func in enumerate(["添加学生","删除学生","修改成绩","查询学生","排行榜","统计信息","退出"], 1):
            table.add_row(str(i), func)
        self.console.print(table)
    
    def _add(self):
        name = self.console.input("请输入姓名：").strip()
        if name in self.students:
            self.console.print("[red]该学生已存在！[/]")
            return
        while True:
            try:
                score = int(self.console.input("请输入成绩（0-100）："))
                if 0 <= score <= 100:
                    self.students[name] = Student(name, score)
                    self._save()
                    self.console.print(f"[green]添加成功！[/]")
                    return
            except ValueError:
                self.console.print("[red]请输入数字！[/]")
    
    def _delete(self):
        name = self.console.input("要删除的学生姓名：").strip()
        if self.students.pop(name, None):
            self._save()
            self.console.print("[green]删除成功[/]")
        else:
            self.console.print("[red]查无此人[/]")
    
    def _modify(self):
        name = self.console.input("要修改的学生姓名：").strip()
        if name not in self.students:
            self.console.print("[red]查无此人[/]")
            return
        while True:
            try:
                score = int(self.console.input(f"当前 {self.students[name].score} → 新成绩："))
                if 0 <= score <= 100:
                    self.students[name].score = score
                    self._save()
                    self.console.print("[green]修改成功[/]")
                    return
            except ValueError:
                self.console.print("[red]请输入数字！[/]")
    
    def _query(self):
        name = self.console.input("查询姓名：").strip()
        s = self.students.get(name)
        self.console.print(str(s) if s else "[red]查无此人[/]")
    
    def _ranking(self):
        if not self.students:
            self.console.print("[yellow]暂无数据[/]")
            return
        table = Table(title="[bold magenta]成绩排行榜[/]")
        table.add_column("排名", style="bold yellow")
        table.add_column("学生", style="white")
        for i, s in enumerate(sorted(self.students.values(), key=lambda x: x.score, reverse=True), 1):
            table.add_row(str(i), str(s))
        self.console.print(table)
    
    def _stats(self):
        if not self.students:
            return
        scores = [s.score for s in self.students.values()]
        avg = sum(scores) / len(scores)
        passed = sum(1 for s in scores if s >= 60)
        self.console.print(Panel.fit(
            f"[cyan]平均分：[white]{avg:.1f}[/]\n"
            f"[cyan]最高分：[green]{max(scores)}[/]　最低分：[red]{min(scores)}[/]\n"
            f"[cyan]及格率：[magenta]{passed/len(scores)*100:.1f}%[/]",
            title="成绩统计", border_style="bright_blue"
        ))
    
    def _exit(self):
        if self.students:
            backup_dir = DATA_FILE.parent / "backup"
            backup_dir.mkdir(exist_ok=True)
            shutil.copy2(DATA_FILE, backup_dir / f"backup_{datetime.now():%Y%m%d_%H%M%S}.json")
            self.console.print("[dim]已自动备份[/]")
        self.console.print(Panel("[bold red]感谢使用！再见！[/]", style="white on red"))
