# core/storage.py
import json
import os
import sys
from pathlib import Path

def get_exe_dir():
    """完美适配开发和打包后的路径"""
    if getattr(sys, 'frozen', False):  # 被 PyInstaller 打包后为 True
        return Path(sys.executable).parent
    else:
        return Path(__file__).parent.parent

BASE_DIR = get_exe_dir()
DATA_FILE = BASE_DIR / "data" / "students_data.json"

def load_data() -> dict:
    if DATA_FILE.exists():
        try:
            return json.loads(DATA_FILE.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"数据文件损坏，已重建：{e}")
    return {}

def save_data(data: dict):
    DATA_FILE.parent.mkdir(exist_ok=True)
    DATA_FILE.write_text(
        json.dumps(data, ensure_ascii=False, indent=4),
        encoding="utf-8"
    )
    print(f"数据已成功保存到：{DATA_FILE}")