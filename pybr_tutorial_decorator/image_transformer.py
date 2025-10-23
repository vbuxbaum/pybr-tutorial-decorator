"""Image transformation helpers used by the CLI."""

from __future__ import annotations


from abc import ABC
from pathlib import Path
from typing import Literal, Optional

from PIL import Image, ImageDraw, ImageFont, ImageOps

RotationDirection = Literal["left", "right"]


class TransformerInterface(ABC):
    def apply(self, image: Image.Image) -> Image.Image:
        raise NotImplementedError


class TransformerDecorator(TransformerInterface):
    _transformer: TransformerInterface

    def __init__(self, transformer: TransformerInterface) -> None:
        self._transformer = transformer


class RGBTransformer(TransformerInterface):
    def apply(self, image: Image.Image) -> Image.Image:
        return image.convert("RGB")


class BlackAndWhiteTransformer(TransformerDecorator):
    def apply(self, image: Image.Image) -> Image.Image:
        """Return a black and white copy of the provided image."""
        image = self._transformer.apply(image)

        grayscale = ImageOps.grayscale(image)
        return ImageOps.autocontrast(grayscale)


class WatermarkTransformer(TransformerDecorator):
    def __init__(self, transformer: TransformerInterface, text: str) -> None:
        super().__init__(transformer)
        self._text = text

    def apply(self, image: Image.Image) -> Image.Image:
        """Return a copy of the image with a large semi-transparent watermark."""
        if not self._text:
            raise ValueError("Watermark text cannot be empty.")

        image = self._transformer.apply(image)

        base = image.convert("RGBA")
        watermark_layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(watermark_layer)
        font = self._load_watermark_font(base.size)
        text_bbox = draw.textbbox((0, 0), self._text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]

        x = (base.width - text_width) // 2
        y = (base.height - text_height) // 2
        draw.text((x, y), self._text, font=font, fill=(255, 255, 255, 120))

        combined = Image.alpha_composite(base, watermark_layer)
        return combined.convert("RGB")

    def _load_watermark_font(
        self, image_size: tuple[int, int]
    ) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
        """Return a large font sized to roughly half of the longest image dimension."""
        width, height = image_size
        base_size = max(int(max(width, height) * 0.5), 10)

        candidates = [
            "DejaVuSans.ttf",
            "Arial.ttf",
            "Helvetica.ttf",
        ]

        last_error: OSError | None = None
        for font_name in candidates:
            try:
                font = ImageFont.truetype(font_name, size=base_size)
                bbox = font.getbbox(self._text)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]

                max_width = width * 0.95
                max_height = height * 0.5
                width_scale = max_width / text_width if text_width else 1
                height_scale = max_height / text_height if text_height else 1
                scale = min(width_scale, height_scale)

                if scale < 1:
                    adjusted_size = max(int(base_size * scale), 10)
                    font = ImageFont.truetype(font_name, size=adjusted_size)

                return font
            except OSError as exc:
                last_error = exc

        if last_error:
            # Final fallback keeps the default font even though it cannot scale as desired.
            return ImageFont.load_default()
        return ImageFont.load_default()


class RotationTransformer(TransformerDecorator):
    def __init__(
        self,
        transformer: TransformerInterface,
        degrees: float,
        direction: RotationDirection,
    ) -> None:
        super().__init__(transformer)
        self._degrees = degrees
        self._direction = direction

    def apply(self, image: Image.Image) -> Image.Image:
        """Rotate the provided image by the given amount."""
        if self._degrees < 0:
            raise ValueError("Degrees must be positive.")

        image = self._transformer.apply(image)

        angle = self._degrees if self._direction == "left" else -self._degrees
        return image.rotate(angle, expand=True)


def _default_output_path(source: Path) -> Path:
    """Default destination path using the original name with a transformed suffix."""
    return source.with_name(f"{source.stem}-transformed{source.suffix}")


def apply_transformations(
    source_path: Path,
    destination_path: Path | None = None,
    *,
    to_black_and_white: bool = False,
    watermark_text: Optional[str] = None,
    rotate_degrees: Optional[float] = None,
    rotate_direction: RotationDirection = "right",
) -> Path:
    """Apply one or more transformations to the image and persist the result."""

    transformer = RGBTransformer()

    if watermark_text:
        transformer = WatermarkTransformer(transformer, watermark_text)

    if rotate_degrees:
        transformer = RotationTransformer(
            transformer, rotate_degrees, rotate_direction
        )
    if to_black_and_white:
        transformer = BlackAndWhiteTransformer(transformer)

    with Image.open(source_path) as img_file:
        image = transformer.apply(img_file)

    destination_path = destination_path or _default_output_path(source_path)
    destination_path.parent.mkdir(parents=True, exist_ok=True)
    image.save(destination_path)

    return destination_path
