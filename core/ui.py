# core/ui.py
from core.operations import students

def show_ranking():
    if not students:
        print("暂无数据")
        return
    print(f"\n{'排名':<4}{'姓名':<10}{'成绩':<6}")
    print("-" * 30)
    for rank, (name, score) in enumerate(sorted(students.items(), key=lambda x: x[1], reverse=True), 1):
        print(f"{rank:<4}{name:<10}{score:<6}")

def show_statistics():
    if not students:
        return
    scores = list(students.values())
    avg = sum(scores) / len(scores)
    passed = sum(1 for s in scores if s >= 60)
    print(f"\n平均分：{avg:.1f}  最高：{max(scores)}  最低：{min(scores)}  及格率：{passed/len(scores)*100:.1f}%")