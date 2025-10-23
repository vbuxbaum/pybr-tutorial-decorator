from __future__ import annotations

from pathlib import Path

import pytest
from PIL import Image


@pytest.fixture
def sample_image(tmp_path: Path) -> Path:
    """Create a simple RGB image for testing."""
    image_path = tmp_path / "sample.jpg"
    Image.new("RGB", (100, 50), color=(255, 0, 0)).save(image_path)
    return image_path
