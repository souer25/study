# core/storage.py
import json
import sys
from pathlib import Path

def get_base_dir():
    """完美兼容开发和打包后的路径"""
    if getattr(sys, 'frozen', False):
        return Path(sys.executable).parent
    else:
        return Path(__file__).parent.parent

BASE_DIR = get_base_dir()
DATA_FILE = BASE_DIR / "data-day10" / "students_day10.json"

def load_data() -> dict:
    if DATA_FILE.exists():
        try:
            return json.loads(DATA_FILE.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"数据损坏，已重建：{e}")
    return {}

def save_data(data: dict):
    DATA_FILE.parent.mkdir(exist_ok=True)
    DATA_FILE.write_text(
        json.dumps(data, ensure_ascii=False, indent=4),
        encoding="utf-8"
    )