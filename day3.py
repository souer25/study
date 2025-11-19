score_str = input("请输入您的分数: ")
score = int(score_str)
if score >= 90:
    print("等级：A")
# 如果 score 不是 >= 90，程序才会执行到这里
elif score >= 80:
    # 此时，我们隐含地知道 score < 90
    print("等级：B")
# ... 依此类推
elif score >= 70:
    print("等级：C")
else:
    print("等级：D")    # ...