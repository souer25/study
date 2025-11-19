# day4.py 优化后的代码片段

for i in range(1, 10):
    for j in range(1, i + 1):
        # 1. 构造单元格内容
        cell_content = f"{j} * {i} = {i * j}"
        
        # 2. 使用 f-string 格式化和填充：
        # {:<10} 表示将 cell_content 字符串填充到 10 个字符的宽度，并左对齐 (<)。
        # 然后再在后面添加一个额外的空格作为列间分隔。
        print(f"{cell_content:<11}", end=' ')
        
    print()