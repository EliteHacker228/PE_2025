import os
from pathlib import Path

# Базовая директория проекта (до backend/)
BASE_DIR = Path(__file__).resolve().parent.parent.parent  # Правильный путь

# Пути к файлам
MODEL_PATH = os.path.join(BASE_DIR, "models", "k_fold_split_0.pt")
RESULTS_DIR = os.path.join(BASE_DIR, "results")
TEMP_DIR = os.path.join(BASE_DIR, "temp")

# Создаём директории один раз
os.makedirs(RESULTS_DIR, exist_ok=True)
os.makedirs(TEMP_DIR, exist_ok=True)
