import os
from pathlib import Path

# Базовая директория проекта
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Пути к директориям и файлам
MODEL_PATH = os.path.join(BASE_DIR, "models", "k_fold_split_0.pt")

TEMP_DIR = os.path.join(BASE_DIR, "temp")
RESULTS_DIR = os.path.join(BASE_DIR, "results")

# Убедимся, что директории существуют
os.makedirs(TEMP_DIR, exist_ok=True)
os.makedirs(RESULTS_DIR, exist_ok=True)
