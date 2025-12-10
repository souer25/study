# Day8 学习笔记 —— Python 打包成 exe 终极防丢全总结（Windows 专属）

**日期**：2025-11-XX  
**系统**：Windows 11 + VS Code + PyInstaller  
**最终成果**：双击即用、数据永不丢失、随便发给任何人、exe 旁边自动出现 data 文件夹

### 一、为什么之前所有数据都丢了？（四大天坑）

| 天坑 | 现象 | 根本原因 | 终极解决方案 |
|------|------|----------|--------------|
| 1. 数据写到临时目录 | 关掉 exe 数据就没了 | PyInstaller 单文件模式运行时会在 `%TEMP%\_MEIxxxx` 解压，关掉就删 | 用 `sys.frozen` + `sys.executable` 判断 exe 真实路径 |
| 2. `-w` 参数 | 双击闪退、报 `lost sys.stdin` | `-w` 禁用了控制台，`input()` 直接崩溃 | 去掉 `-w`，保留小黑窗（最稳） |
| 3. `__file__` 失效 | 打包后路径乱飞 | 冻结后 `__file__` 指向临时目录或不存在 | 永远不用 `__file__`，改用 `sys.executable` |
| 4. 相对路径依赖 cwd | 换地方运行就乱 | 双击 exe 的当前目录是 exe 位置，从别的盘运行就错 | 所有路径必须基于 exe 位置计算 |

### 二、终极防丢神器函数（背下来一辈子吃香）

```python
def get_exe_dir():
    if getattr(sys, 'frozen', False):        # 打包后为 True
        return Path(sys.executable).parent   # exe 所在目录
    else:
        return Path(__file__).parent.parent  # 开发时项目根目录

BASE_DIR = get_exe_dir()
DATA_FILE = BASE_DIR / "data" / "students_data.json"
```

所有要保存的文件（json、log、数据库、配置）都基于 `BASE_DIR`，永不丢失！

### 三、最稳打包命令（我现在永远只用这一个）

```powershell
pyinstaller -F -i icon.ico main.py
# -F：单文件
# -i：自定义图标
# 不加 -w：保留小黑窗，保证 input() 正常
```

### 四、完整项目结构（专业工程化标准）

```
项目根目录/
│
├── main.py                  ← 入口
├── icon.ico                 ← 可选图标
├── data/                    ← 程序运行时自动创建
│   └── students_data.json
└── core/
    ├── __init__.py
    ├── storage.py           ← 防丢核心
    ├── operations.py        ← 增删改查
    └── ui.py                ← 界面显示
```

### 五、每日打包 + 提交终极流程（10 秒）

1. 改完代码 → Ctrl+S
2. 左侧 Source Control → 点 + 全暂存
3. 写消息：`feat: day8 终极防丢版`
4. Ctrl+Enter 提交
5. ↓ Pull → ↑ Push
6. 终端敲：`pyinstaller -F -i icon.ico main.py`
7. 把 `dist/main.exe` 复制出来随便发

### 六、今日最大收获

- 彻底搞懂了 Python 打包的所有天坑
- 拥有了真正能发给任何人的 Windows 软件
- 掌握了 `sys.frozen` + `sys.executable` 这把“打包界屠龙刀”
- 以后再也不怕数据丢失、路径错误、双击闪退

**Day8 彻底征服！所有天坑已封印！**  
**下一个目标**：Day9 用 rich + colorama 做出炫彩终端界面 + 开场动画 + 音效 + 自动备份

准备好了就吼：
**“Day8 笔记已刻进DNA！Day9 启动！”**

我们明天把这个程序美到你妈都想学编程！冲！