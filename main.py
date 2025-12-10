# main.py
from core.operations import add, delete, modify, query
from core.ui import show_ranking, show_statistics

def main():
    while True:
        print("\n" + "="*40)
        print("    学生成绩管理系统 v8.0（终极防丢版）")
        print("="*40)
        menu = ["添加学生", "删除学生", "修改成绩", "查询学生", "排行榜", "统计信息", "退出"]
        for i, item in enumerate(menu, 1):
            print(f"{i}. {item}")
        
        choice = input("\n请选择 (1-7): ").strip()
        match choice:
            case "1": add()
            case "2": delete()
            case "3": modify()
            case "4": query()
            case "5": show_ranking()
            case "6": show_statistics()
            case "7": print("再见！数据已永久保存"); break
            case _: print("输入错误！")

if __name__ == "__main__":
    main()