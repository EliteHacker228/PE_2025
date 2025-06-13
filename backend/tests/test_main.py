from fastapi.testclient import TestClient
from app.main import app
import pytest
import cv2
import numpy as np
from io import BytesIO
from PIL import Image  # Добавлен импорт PIL
import os

client = TestClient(app)


def test_upload_invalid_file():
    """Тест загрузки некорректного файла"""
    response = client.post(
        "/upload",
        files={"file": ("test.txt", b"not an image", "text/plain")}
    )
    assert response.status_code == 400
    assert "Unsupported file type" in response.text


def test_image_processing_flow(tmp_path):
    """Тест с валидным изображением"""
    test_img = tmp_path / "test.jpg"
    cv2.imwrite(str(test_img), np.zeros((100, 100, 3), dtype=np.uint8))

    with open(test_img, "rb") as f:
        response = client.post(
            "/upload",
            files={"file": ("test.jpg", f, "image/jpeg")}
        )

    assert response.status_code == 200
    assert "processed_image" in response.json()


def test_response_format():
    """Проверяем структуру JSON-ответа"""
    test_img = BytesIO()
    Image.new('RGB', (100, 100)).save(test_img, 'JPEG')
    test_img.seek(0)

    response = client.post(
        "/upload",
        files={"file": ("test.jpg", test_img, "image/jpeg")}
    )

    assert response.status_code == 200
    data = response.json()

    # Проверяем минимально необходимые поля
    assert "status" in data
    assert "processed_image" in data
    assert data["status"] == "success"

    # Дополнительно можно проверить тип полей
    assert isinstance(data["processed_image"], str)
    if "filename" in data:  # Если поле опциональное
        assert isinstance(data["filename"], str)