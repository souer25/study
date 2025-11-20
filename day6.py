# day6_complete.py
# Python 字典 + JSON 永久存储版 学生成绩管理系统
# 作者：Lang   日期：2025-11-22

import json
import os
from typing import List, Dict

# 1. 常量与文件路径
DATA_FILE = "students_data.json"   # 数据保存的文件名

# 2. 加载数据函数（程序启动时自动执行）
def load_data() -> Dict[str, int]:
    """从 JSON 文件加载数据，如果文件不存在返回空字典"""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)    # {"张三": 88, "李四": 92}
        except:
            print("⚠️  数据文件损坏，已重新初始化")
    return {}   # 第一次运行或文件损坏时返回空

# 3. 保存数据函数（每次修改后自动调用）
def save_data(data: Dict[str, int]):
    """把字典保存到 JSON 文件"""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print("💾 数据已自动保存！")

# 4. 主程序开始
students = load_data()    # ←←← 关键！启动时自动读取历史数据

def add_student():
    name = input("请输入姓名：").strip().strip("\n\r")
    if name in students:
        print("❌ 该学生已存在！")
        return
    while True:
        try:
            score = int(input("请输入成绩（0-100）："))
            if 0 <= score <= 100:
                students[name] = score
                save_data(students)
                print(f"✅ 添加成功：{name} {score}分")
                break
            else:
                print("⚠️  成绩必须在0-100之间！")
        except ValueError:
            print("⚠️  请输入纯数字！")

def delete_student():
    name = input("请输入要删除的学生姓名：").strip()
    if students.pop(name, None) is not None:   # pop 如果不存在返回 None
        save_data(students)
        print(f"✅ 已删除 {name}")
    else:
        print("❌ 查无此人")

def modify_score():
    name = input("请输入要修改的学生姓名：").strip()
    if name not in students:
        print("❌ 查无此人")
        return
    while True:
        try:
            score = int(input(f"当前成绩 {students[name]} → 新成绩："))
            if 0 <= score <= 100:
                students[name] = score
                save_data(students)
                print("✅ 修改成功！")
                break
            else:
                print("⚠️  必须0-100")
        except ValueError:
            print("⚠️  请输入数字")

def query_student():
    name = input("请输入要查询的学生姓名：").strip()
    score = students.get(name)
    if score is not None:
        print(f"🎯 {name} 的成绩是：{score} 分")
    else:
        print("❌ 查无此人")

def show_ranking():
    if not students:
        print("⚠️  暂无数据")
        return
    # 按成绩降序排序
    sorted_items = sorted(students.items(), key=lambda x: x[1], reverse=True)
    print(f"\n{'排名':<4}{'姓名':<10}{'成绩':<5}")
    print("-" * 25)
    for rank, (name, score) in enumerate(sorted_items, 1):
        print(f"{rank:<4}{name:<10}{score:<5}")

def show_statistics():
    if not students:
        print("⚠️  暂无数据")
        return
    scores = list(students.values())
    avg = sum(scores) / len(scores)
    pass_count = len([s for s in scores if s >= 60])
    print(f"\n📊 平均分：{avg:.2f}")
    print(f"📈 最高分：{max(scores)}")
    print(f"📉 最低分：{min(scores)}")
    print(f"✔️  及格人数：{pass_count}（及格率 {pass_count/len(scores)*100:5.1f}%）")

# 主菜单循环
while True:
    print("\n" + "="*30)
    print("   学生成绩管理系统 v6.0 (永久存储版)")
    print("="*30)
    print("1. 添加学生")
    print("2. 删除学生")
    print("3. 修改成绩")
    print("4. 查询学生")
    print("5. 排行榜")
    print("6. 统计信息")
    print("7. 退出")
    
    choice = input("\n请选择功能 (1-7): ").strip()
    
    if choice == "1":
        add_student()
    elif choice == "2":
        delete_student()
    elif choice == "3":
        modify_score()
    elif choice == "4":
        query_student()
    elif choice == "5":
        show_ranking()
    elif choice == "6":
        show_statistics()
    elif choice == "7":
        print("👋 再见！所有数据已自动保存")
        break
    else:
        print("❌ 输入有误，请重新选择")