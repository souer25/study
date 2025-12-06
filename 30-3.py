# 写入操作 ('w' 模式)
file = open("my_log.txt", "w") # w 表示写入模式，会覆盖原有内容
file.write("这是第一行日志。\n")
file.write("这是第二行日志。\n")
file.close() # 必须关闭！


# 读取操作 ('r' 模式)
file = open("my_log.txt", "r") # r 表示读取模式
content = file.read()
print(content)
file.close() # 必须关闭！

# 使用 with 语句，文件会在代码块结束时自动关闭
with open("my_data.txt", "w") as f: # f 是文件对象
    f.write("使用上下文管理器更安全！")

# 此时文件 f 已经被自动关闭了
with open("my_data.txt", "r") as f1:
    data = f1.read()
    print(data)


with open("example.txt", "a") as f2:
    f2.write("追加一行内容。\n")

try:
    with open("settings.json", "r") as f3:
except FileNotFoundError :
    print("文件未找到，请检查路径是否正确。")
    settings = f3.read()
    print("找到的结果是 {settings})