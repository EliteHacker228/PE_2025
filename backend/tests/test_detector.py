import numpy as np
import cv2
import tempfile
import os
import pytest
from unittest.mock import MagicMock, patch
from app.services.detector import (
    get_angle_to_rotate,
    rotate_image,
    process_image_file,
)


def test_get_angle_to_rotate():
    mock_obb = MagicMock()
    mock_obb.xywhr = [np.array([0, 0, 0, 0, np.pi / 4])]
    angle = get_angle_to_rotate(mock_obb)
    assert round(angle, 2) == 45.0


def test_rotate_image():
    img = np.ones((100, 100, 3), dtype=np.uint8) * 255
    rotated = rotate_image(img, 45)
    assert rotated.shape == (141, 141, 3)


def test_no_tables_detected(tmp_path):
    mock_yolo = MagicMock()
    mock_result = MagicMock()
    mock_result.obb = []
    mock_yolo.return_value.return_value = [mock_result]

    img_path = tmp_path / "test.jpg"
    cv2.imwrite(str(img_path), np.ones((100, 100, 3), dtype=np.uint8))

    with patch("app.services.detector.YOLO", mock_yolo):
        result_path = process_image_file(str(img_path))
        assert os.path.exists(result_path)
        result_img = cv2.imread(result_path)
        assert result_img.shape == (100, 100, 3)


def test_invalid_image_file():
    with pytest.raises(FileNotFoundError):
        process_image_file("nonexistent_file.jpg")


def test_with_real_image(tmp_path):
    img_path = tmp_path / "test_table.jpg"
    img = np.zeros((500, 500, 3), dtype=np.uint8)
    cv2.rectangle(img, (100, 100), (400, 400), (255, 255, 255), -1)
    cv2.imwrite(str(img_path), img)

    result_path = process_image_file(str(img_path))
    assert os.path.exists(result_path)


@patch("app.services.detector.YOLO")
@patch("app.services.detector.cv2.imwrite")
@patch("app.services.detector.cv2.imread")
def test_process_image_file(mock_imread, mock_imwrite, mock_yolo):
    test_img = np.ones((100, 100, 3), dtype=np.uint8)
    mock_imread.return_value = test_img

    mock_result = MagicMock()
    mock_obb = MagicMock()
    mock_obb.xywhr = [np.array([0, 0, 0, 0, np.pi / 4])]
    mock_result.obb = [mock_obb]
    mock_yolo.return_value.return_value = [mock_result]

    with tempfile.NamedTemporaryFile(suffix=".jpg") as tmp:
        result_path = process_image_file(tmp.name)
        assert "rotated" in result_path
