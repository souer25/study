# 终极保姆级 Ubuntu 24.04.3 虚拟机运维笔记  
（专为你在 Windows 宿主机上跑的这台 Ubuntu 虚拟机量身定制，照着做一辈子不会忘）

### 一、虚拟机本身操作（宿主机层面）

| 操作               | 软件推荐                     | 快捷键 / 方法                                      | 说明                                  |
|--------------------|------------------------------|----------------------------------------------------|---------------------------------------|
| 启动虚拟机软件       | VMware Workstation Player（免费）<br>或 VirtualBox（免费）<br>或 Proxmox VE（进阶） | 我用的是 VMware Player                      | 你现在用的就是它                      |
| 启动虚拟机         | 双击桌面快捷方式             | 或在 VMware 里右键你的 Ubuntu → Power On         | 开机                                  |
| 进入全屏           | Ctrl + Alt + Enter           | 再次按退出全屏                                     | 最爽操作体验                          |
| 退出全屏           | Ctrl + Alt                   | 鼠标移到屏幕正中上方会弹出工具栏                   | 随时切回 Windows                      |
| 暂停虚拟机         | 顶部菜单 → VM → Power → Suspend | 相当于“休眠”，下次恢复秒开                        | 推荐！比关机快                        |
| 完全关机           | 虚拟机里敲 `sudo poweroff`   | 或顶部菜单 → Power → Shut Down                      | 彻底关闭                              |
| 复制文件到虚拟机   | 1. 共享文件夹（最方便）<br>2. WinSCP（图形化）<br>3. scp 命令 | 我用共享文件夹：VM → Settings → Options → Shared Folders → Add 宿主机文件夹 | 拖拽文件直接进虚拟机                  |
| 从虚拟机复制文件到宿主机 | 同上，直接拖出来             |                                                    |                                       |

### 二、虚拟机第一次登录（你现在已经做完）

```bash
ubuntu login: root
Password: 你设置的密码
```

成功后看到 `root@ubuntu:~#` 就是胜利！

### 三、Ubuntu 24.04.3 核心操作速查表（永久保存）

| 功能                     | 命令（直接复制粘贴）                                                                 | 说明                                                                 |
|--------------------------|--------------------------------------------------------------------------------------|----------------------------------------------------------------------|
| 换国内源 + 系统升级      | `cat > /etc/apt/sources.list.d/ubuntu.sources <<EOF`（前面给你的那段）<br>`apt update -y && apt upgrade -y` | 提速10倍，必做一次                                                   |
| 安装常用工具             | `apt install -y python3-pip python3-venv nginx curl git tmux htop unzip`               | 一次装齐                                                             |
| 创建项目目录             | `mkdir -p /opt/score_system && cd /opt/score_system`                                   | 所有项目放 /opt 最规范                                               |
| 创建虚拟环境             | `python3 -m venv venv`<br>`source venv/bin/activate`                                   | 激活后提示符会变成 `(venv) root@ubuntu`                               |
| 退出虚拟环境             | `deactivate`                                                                         | 回到系统 python                                                      |
| 安装 FastAPI 全家桶      | `pip install --upgrade pip`<br>`pip install fastapi uvicorn[standard] rich`             | 只在虚拟环境里装                                                     |
| 启动 Web 服务（前台）    | `uvicorn web_main:app --host 0.0.0.0 --port 8000`                                        | 用来测试                                                             |
| 启动 Web 服务（后台）    | `nohup uvicorn web_main:app --host 0.0.0.0 --port 8000 > web.log 2>&1 &`              | 永久后台运行                                                         |
| 查看运行状态             | `ps aux | grep uvicorn`                                                               | 看进程                                                               |
| 查看实时日志             | `tail -f web.log`                                                                    | Ctrl+C 退出                                                          |
| 重启 Nginx               | `nginx -t && systemctl restart nginx`                                                     | 配置改完必敲                                                         |
| 开80端口（如果有ufw）    | `ufw allow 80`                                                                       | 不开浏览器打不开                                                     |
| 开机自启服务（以后用）   | `systemctl enable nginx`                                                              | 系统启动自动跑                                                       |

### 四、你现在的完整项目路径（永久记住）

```
/opt/score_system/
├── venv/                     ← 虚拟环境
├── web_main.py               ← FastAPI 主程序
├── data/
│   └── students.json          ← 所有学生数据（关机不丢！）
└── web.log                   ← 运行日志
```

### 五、每天开机后的标准启动流程（复制到记事本永久保存）

```bash
# 1. 登录虚拟机（root）
# 2. 进入项目
cd /opt/score_system

# 3. 激活虚拟环境
source venv/bin/activate

# 4. 启动服务
nohup uvicorn web_main:app --host 0.0.0.0 --port 8000 > web.log 2>&1 &

# 5. 打开浏览器访问 http://虚拟机IP
```

### 六、完全退出虚拟机流程（安全关机）

```bash
# 在虚拟机里敲
sudo poweroff
# 或者直接点 VMware 顶部 Power → Shut Down Guest
```

### 七、以后想直接在 Windows 访问虚拟机里的 Web

只要虚拟机开着，宿主机浏览器直接打开：
```
http://192.168.x.x        ← 你的虚拟机IP（你截图里是 192.168.31.7）
http://192.168.31.7/docs ← 直接玩交互文档
```

这套笔记直接保存成 `Ubuntu虚拟机运维宝典.md`，放桌面，以后一辈子都不会忘！

**Day13 完美收官！**  
你现在拥有了一个：
- 可随时开关
- 永不失联
- 完全可控
- 可复制到任何云服务器
的生产级开发环境！

准备好了就吼：
**“虚拟机运维笔记已刻进DNA！Day14 登录+数据库+HTTPS，冲！”**

明天我们直接把这个系统变成带用户名密码、PostgreSQL、域名、HTTPS 绿锁的正式上线项目！  
30天后你就是能独立搞定全栈 + 运维的狠人！冲！