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
    assert response.status_code in (400, 422)


def test_image_processing_flow(tmp_path):
    test_img = tmp_path / "test.jpg"
    cv2.imwrite(str(test_img), np.zeros((100, 100, 3), dtype=np.uint8))

    with open(test_img, "rb") as f:
        response = client.post(
            "/detect-rotate/",
            files={"file": ("test.jpg", f, "image/jpeg")},
        )

    assert response.status_code == 200
    assert response.headers["content-type"] == "image/jpeg"


def test_response_format():
    test_img = BytesIO()
    Image.new("RGB", (100, 100)).save(test_img, "JPEG")
    test_img.seek(0)

    response = client.post(
        "/detect-rotate/",
        files={"file": ("test.jpg", test_img, "image/jpeg")},
    )

    assert response.status_code == 200
    assert response.headers["content-type"] == "image/jpeg"
