# core/student.py
class Student:
    def __init__(self, name: str, score: int):
        self.name = name.strip()
        self.score = score
    
    def __str__(self):
        if self.score >= 90:
            color = "bold green"
        elif self.score >= 60:
            color = "bold yellow"
        else:
            color = "bold red"
        return f"[{color}]{self.name}[/]：{self.score} 分"