import cv2
import numpy as np
import os
from ultralytics import YOLO
from app.core.config import MODEL_PATH, RESULTS_DIR, BASE_DIR

print("MODEL_PATH value:")
print(MODEL_PATH)

print("Полный список файлов от BASE_DIR:")
for root, dirs, files in os.walk(BASE_DIR):
    dirs[:] = [d for d in dirs if d != ".venv"]

    for f in files:
        full_path = os.path.join(root, f)
        print(full_path)

model = YOLO(MODEL_PATH)


def get_angle_to_rotate(obb) -> float:
    xywhr = obb.xywhr[0]
    rotation_rad = xywhr[-1]
    return round(rotation_rad.item() * (180 / np.pi), 2)


def rotate_image(image, angle):
    h, w = image.shape[:2]
    center = (w // 2, h // 2)
    matrix = cv2.getRotationMatrix2D(center, angle, 1.0)

    cos = abs(matrix[0, 0])
    sin = abs(matrix[0, 1])
    new_w = int(h * sin + w * cos)
    new_h = int(h * cos + w * sin)

    matrix[0, 2] += new_w / 2 - center[0]
    matrix[1, 2] += new_h / 2 - center[1]

    return cv2.warpAffine(image, matrix, (new_w, new_h))


def process_image_file(image_path: str) -> str:
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"File not found or cannot be read: {filepath}")

    results = model(image)

    angle = 0
    for result in results:
        if result.obb and len(result.obb) > 0:
            angles = [get_angle_to_rotate(obb) for obb in result.obb]
            angle = sum(angles) / len(angles)

    rotated = rotate_image(image, angle)
    filename = os.path.basename(image_path)
    output_path = os.path.join(RESULTS_DIR, f"rotated_{filename}")
    cv2.imwrite(output_path, rotated)
    return output_path
