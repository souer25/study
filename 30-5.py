import logging
import os

LOG_FILE = 'system_activity.log'

# 1. 基本配置：设置日志记录的格式、级别和输出文件
logging.basicConfig(
    filename=LOG_FILE,             # 记录到哪个文件
    level=logging.INFO,            # 记录的最低级别（只记录 INFO, WARNING, ERROR, CRITICAL）
    format='%(asctime)s - %(levelname)s - %(message)s'  # 日志格式
)

# 2. 记录一条信息
logging.info("智能学习系统启动成功。")

# 3. 记录一条警告
logging.warning("数据库连接可能不稳定。")

# 4. 记录一条错误
try:
    result = 10 / 0
except ZeroDivisionError as e:
    # 使用 exception() 方法来记录完整的错误追踪信息
    logging.exception(f"致命错误：尝试除以零！")