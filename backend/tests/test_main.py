from fastapi.testclient import TestClient
from app.main import app
import numpy as np
import cv2
from io import BytesIO
from PIL import Image

client = TestClient(app)


def test_upload_invalid_file():
    response = client.post(
        "/upload",
        files={"file": ("test.txt", b"not an image", "text/plain")}
    )
    assert response.status_code == 400
    assert "Unsupported file type" in response.text


def test_image_processing_flow(tmp_path):
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
    test_img = BytesIO()
    Image.new("RGB", (100, 100)).save(test_img, "JPEG")
    test_img.seek(0)

    response = client.post(
        "/upload",
        files={"file": ("test.jpg", test_img, "image/jpeg")}
    )

    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "processed_image" in data
    assert data["status"] == "success"
    assert isinstance(data["processed_image"], str)
    if "filename" in data:
        assert isinstance(data["filename"], str)
