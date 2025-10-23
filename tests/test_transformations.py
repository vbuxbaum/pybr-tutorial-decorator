from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageChops

from pybr_tutorial_decorator.image_transformer import (
    WatermarkTransformer,
    BlackAndWhiteTransformer,
    RotationTransformer,
    apply_transformations,
)


def test_black_and_white_transformer(
    sample_image: Path, tmp_path: Path
) -> None:
    with Image.open(sample_image) as img_file:
        img = img_file.convert("RGB")

    transformed = BlackAndWhiteTransformer().apply(img)
    assert transformed.mode == "L"

    destination = tmp_path / "bw.jpg"
    transformed.save(destination)
    assert destination.exists()


def test_watermark_transformer_changes_image(sample_image: Path) -> None:
    with Image.open(sample_image) as img_file:
        img = img_file.convert("RGB")
    watermarked = WatermarkTransformer().apply(img, "PyBR")

    difference = ImageChops.difference(img, watermarked)
    assert difference.getbbox() is not None


def test_rotation_transformer_expands_canvas(
    sample_image: Path, tmp_path: Path
) -> None:
    destination = tmp_path / "rotated.jpg"
    with Image.open(sample_image) as img_file:
        img = img_file.convert("RGB")

    rotated = RotationTransformer().apply(img, degrees=90, direction="left")
    assert rotated.size == (50, 100)

    rotated.save(destination)
    assert destination.exists()

def test_combine_transformations(
    sample_image: Path, tmp_path: Path
) -> None:
    with Image.open(sample_image) as img_file:
        img = img_file.convert("RGB")

    transformed = RotationTransformer().apply(img, degrees=90, direction="left")
    transformed = BlackAndWhiteTransformer().apply(transformed)

    assert transformed.mode == "L"
    assert transformed.size == (50, 100)

    destination = tmp_path / "combo.jpg"
    transformed.save(destination)
    assert destination.exists()

def test_apply_transformations_pipeline(
    sample_image: Path, tmp_path: Path
) -> None:
    destination = tmp_path / "combo.jpg"
    result = apply_transformations(
        sample_image,
        destination_path=destination,
        to_black_and_white=True,
        watermark_text="PyBR",
        rotate_degrees=90,
        rotate_direction="left",
    )

    assert result.exists()
    with Image.open(result) as img:
        assert img.mode == "L"
        assert img.size == (50, 100)
