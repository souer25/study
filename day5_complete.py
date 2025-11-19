# day5_complete.py
# 学生成绩管理系统（纯列表版） - Day5 完整作业

names = []
scores = []

while True:
    print("\n" + "="*25)
    print("   学生成绩管理系统")
    print("="*25)
    print("1. 添加学生成绩")
    print("2. 删除学生")
    print("3. 修改成绩")
    print("4. 查询学生成绩")
    print("5. 显示所有学生（按成绩降序）")
    print("6. 统计信息")
    print("7. 退出")
    print("-"*25)
    
    choice = input("请选择功能 (1-7): ").strip()
    
    if choice == "1":
        name = input("请输入学生姓名: ").strip()
        while True:
            try:
                score = int(input("请输入学生成绩 (0-100): "))
                if 0 <= score <= 100:
                    break
                else:
                    print("成绩必须在0-100之间！")
            except ValueError:
                print("请输入有效的数字！")
        
        names.append(name)
        scores.append(score)
        print(f"成功添加 {name} 的成绩 {score} 分！")
    
    elif choice == "2":
        name = input("请输入要删除的学生姓名: ")
        if name in names:
            idx = names.index(name)
            names.pop(idx)
            scores.pop(idx)
            print(f"已删除学生 {name}")
        else:
            print("查无此人！")
    
    elif choice == "3":
        name = input("请输入要修改的学生姓名: ")
        if name in names:
            idx = names.index(name)
            while True:
                try:
                    new_score = int(input(f"原成绩 {scores[idx]} 分，输入新成绩: "))
                    if 0 <= new_score <= 100:
                        scores[idx] = new_score
                        print("修改成功！")
                        break
                    else:
                        print("成绩必须在0-100之间！")
                except ValueError:
                    print("请输入有效数字！")
        else:
            print("查无此人！")
    
    elif choice == "4":
        name = input("请输入要查询的学生姓名: ")
        if name in names:
            idx = names.index(name)
            print(f"{name} 的成绩是：{scores[idx]} 分")
        else:
            print("查无此人！")
    
    elif choice == "5":
        if not names:
            print("暂无学生数据！")
            continue
        
        # 组合成 (score, name) 的列表，按 score 降序排序
        combined = list(zip(scores, names))
        combined.sort(reverse=True)  # 按成绩降序
        
        print(f"\n{'排名':<3} {'姓名':<10} {'成绩':<5}")
        print("-" * 25)
        for rank, (score, name) in enumerate(combined, 1):
            print(f"{rank:<3} {name:<10} {score:<5}")
    
    elif choice == "6":
        if not scores:
            print("暂无学生数据！")
            continue
        
        avg = sum(scores) / len(scores)
        max_score = max(scores)
        min_score = min(scores)
        pass_count = len([s for s in scores if s >= 60])
        
        print(f"平均分: {avg:.2f}")
        print(f"最高分: {max_score}")
        print(f"最低分: {min_score}")
        print(f"及格人数: {pass_count} 人（≥60分）")
        print(f"及格率: {pass_count/len(scores)*100:.1f}%")
    
    elif choice == "7":
        print("感谢使用，再见！")
        break
    
    else:
        print("输入有误，请重新选择！")
    
    # 任意键继续
    input("\n按回车键继续...")