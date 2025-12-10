# core/operations.py
from core.storage import load_data, save_data

students = load_data()

def add():
    name = input("请输入姓名：").strip()
    if not name:
        return
    if name in students:
        print("该学生已存在！")
        return
    while True:
        try:
            score = int(input("请输入成绩（0-100）："))
            if 0 <= score <= 100:
                students[name] = score
                save_data(students)
                print(f"添加成功：{name} {score}分")
                return
        except ValueError:
            print("请输入数字！")

def delete():
    name = input("请输入要删除的学生姓名：").strip()
    if students.pop(name, None) is not None:
        save_data(students)
        print(f"已删除：{name}")
    else:
        print("查无此人")

def modify():
    name = input("请输入要修改的学生姓名：").strip()
    if name not in students:
        print("查无此人")
        return
    while True:
        try:
            score = int(input(f"当前成绩 {students[name]} → 新成绩："))
            if 0 <= score <= 100:
                students[name] = score
                save_data(students)
                print("修改成功！")
                return
        except ValueError:
            print("请输入数字")

def query():
    name = input("请输入要查询的学生姓名：").strip()
    score = students.get(name)
    print(f"{name} 的成绩：{score} 分" if score is not None else "查无此人")