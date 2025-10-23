"""Command line interface for basic image transformations."""

from __future__ import annotations

from pathlib import Path
from typing import Optional

import typer

from . import image_transformer as transformer
from .image_transformer import RotationDirection

app = typer.Typer(
    help="Simple CLI for common image transformations.",
    no_args_is_help=True,
)


def _validate_input_path(image: Path) -> None:
    if not image.exists():
        typer.secho(f"Image not found: {image}", fg=typer.colors.RED)
        raise typer.Exit(code=1)


@app.command(no_args_is_help=True)
def transform(
    image: Path = typer.Argument(..., help="Path to the image to transform."),
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="Destination path for the transformed image."),
    black_white: bool = typer.Option(False, "--black-white", help="Convert the image to black and white."),
    watermark_text: Optional[str] = typer.Option(None, "--watermark-text", "-w", help="Text content for the watermark."),
    rotate_degrees: Optional[float] = typer.Option(None, "--rotate-degrees", help="Number of degrees to rotate the image."),
    rotate_direction: RotationDirection = typer.Option(
        "right",
        "--rotate-direction",
        help="Rotate right (clockwise) or left (counter-clockwise) when rotation is used.",
    ),
) -> None:
    """Apply one or more transformations to an image in a single pass."""
    _validate_input_path(image)

    if watermark_text is not None:
        if not watermark_text.strip():
            typer.secho("Watermark text cannot be empty.", fg=typer.colors.RED)
            raise typer.Exit(code=1)

    if rotate_degrees is not None and rotate_degrees < 0:
        typer.secho("Rotation degrees must be zero or positive.", fg=typer.colors.RED)
        raise typer.Exit(code=1)

    if not any([black_white, watermark_text, rotate_degrees is not None]):
        typer.secho("Provide at least one transformation option.", fg=typer.colors.YELLOW)
        raise typer.Exit(code=0)

    try:
        destination = transformer.apply_transformations(
            image,
            output,
            to_black_and_white=black_white,
            watermark_text=watermark_text,
            rotate_degrees=rotate_degrees,
            rotate_direction=rotate_direction,
        )
    except ValueError as exc:
        typer.secho(str(exc), fg=typer.colors.RED)
        raise typer.Exit(code=1) from exc

    typer.secho(f"Saved transformed image to {destination}", fg=typer.colors.GREEN)


def main() -> None:
    """Entry point used by the project scripts."""
    app()


if __name__ == "__main__":
    main()
