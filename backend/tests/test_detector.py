import os
from app.services.detector import process_image_file


def test_process_image_file():
    test_image = "tests/test_data/test.jpg"
    assert os.path.exists(test_image)

    output = process_image_file(test_image)
    assert os.path.exists(output)
    assert output.endswith(".jpg")
