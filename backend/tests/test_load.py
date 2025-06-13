import os
from concurrent.futures import ThreadPoolExecutor
import numpy as np
import cv2
import pytest
from app.services.detector import process_image_file


@pytest.mark.load
def test_concurrent_processing(tmp_path_factory):
    temp_dir = tmp_path_factory.mktemp("load_test")

    for i in range(10):
        img_path = temp_dir / f"test_{i}.jpg"
        cv2.imwrite(
            str(img_path),
            np.random.randint(0, 255, (800, 600, 3), dtype=np.uint8),
        )

    with ThreadPoolExecutor(max_workers=5) as executor:
        image_paths = [str(p) for p in temp_dir.glob("*.jpg")]
        results = list(executor.map(process_image_file, image_paths))

    assert len(results) == 10
    assert all(os.path.exists(p) for p in results)
