from __future__ import annotations

from pathlib import Path

from typer.testing import CliRunner

from pybr_tutorial_decorator.cli import app


runner = CliRunner()


def test_cli_black_white_creates_output(sample_image: Path, tmp_path: Path) -> None:
    output = tmp_path / "bw.jpg"
    result = runner.invoke(
        app,
        [str(sample_image), "--black-white", "--output", str(output)],
    )

    assert result.exit_code == 0
    assert "Saved transformed image" in result.stdout
    assert output.exists()


def test_cli_watermark(sample_image: Path, tmp_path: Path) -> None:
    output = tmp_path / "wm.jpg"
    result = runner.invoke(
        app,
        [
            str(sample_image),
            "--watermark-text",
            "PyBR",
            "--output",
            str(output),
        ],
    )

    assert result.exit_code == 0
    assert "Saved transformed image" in result.stdout
    assert output.exists()


def test_cli_rotate(sample_image: Path, tmp_path: Path) -> None:
    output = tmp_path / "rotated.jpg"
    result = runner.invoke(
        app,
        [
            str(sample_image),
            "--rotate-degrees",
            "45",
            "--rotate-direction",
            "left",
            "--output",
            str(output),
        ],
    )

    assert result.exit_code == 0
    assert "Saved transformed image" in result.stdout
    assert output.exists()


def test_cli_multiple_transformations(sample_image: Path, tmp_path: Path) -> None:
    output = tmp_path / "combo.jpg"
    result = runner.invoke(
        app,
        [
            str(sample_image),
            "--black-white",
            "--watermark-text",
            "PyBR",
            "--rotate-degrees",
            "90",
            "--rotate-direction",
            "left",
            "--output",
            str(output),
        ],
    )

    assert result.exit_code == 0
    assert "Saved transformed image" in result.stdout
    assert output.exists()
