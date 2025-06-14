from fastapi.testclient import TestClient
from app.main import app
import numpy as np
import cv2
from io import BytesIO
from PIL import Image

client = TestClient(app)


def test_upload_invalid_file():
    response = client.post(
        "/detect-rotate/",
        files={"file": ("test.txt", b"not an image", "text/plain")},
    )
    assert response.status_code == 500
    assert "Image processing failed" in response.text


def test_image_processing_flow(tmp_path):
    test_img = tmp_path / "test.jpg"
    arr = np.zeros((100, 100, 3), dtype=np.uint8)
    cv2.imwrite(str(test_img), arr)

    with open(test_img, "rb") as f:
        response = client.post(
            "/detect-rotate/",
            files={"file": ("test.jpg", f, "image/jpeg")},
        )

    assert response.status_code == 200
    # Проверяем, что ответ содержит бинарные данные изображения
    assert response.content.startswith(b"\xff\xd8")
    assert "content-disposition" in response.headers


def test_response_format():
    test_img = BytesIO()
    Image.new("RGB", (100, 100)).save(test_img, "JPEG")
    test_img.seek(0)

    response = client.post(
        "/detect-rotate/",
        files={"file": ("test.jpg", test_img, "image/jpeg")},
    )

    assert response.status_code == 200
    # Проверяем бинарный ответ
    assert response.content.startswith(b"\xff\xd8")
    assert "content-disposition" in response.headers
