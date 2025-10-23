from __future__ import annotations

from pathlib import Path

from typer.testing import CliRunner

from pybr_tutorial_decorator.cli import app

from pytest import MonkeyPatch
from unittest.mock import MagicMock

runner = CliRunner()


def test_cli_black_white_creates_output(
    sample_image: Path, tmp_path: Path, monkeypatch: MonkeyPatch
) -> None:
    output = tmp_path / "bw.jpg"
    mock_transformation_function = MagicMock(return_value=output)
    monkeypatch.setattr(
        "pybr_tutorial_decorator.cli.transformer.apply_transformations",
        mock_transformation_function,
    )
    result = runner.invoke(
        app,
        [str(sample_image), "--black-white", "--output", str(output)],
    )
    assert mock_transformation_function.call_count == 1
    assert mock_transformation_function.call_args[1]["to_black_and_white"]
    assert result.exit_code == 0
    assert "Saved transformed image" in result.stdout
    assert output.stem in result.stdout


def test_cli_watermark(
    sample_image: Path, tmp_path: Path, monkeypatch: MonkeyPatch
) -> None:
    output = tmp_path / "wm.jpg"
    mock_transformation_function = MagicMock(return_value=output)
    monkeypatch.setattr(
        "pybr_tutorial_decorator.cli.transformer.apply_transformations",
        mock_transformation_function,
    )

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
    assert mock_transformation_function.call_count == 1
    assert mock_transformation_function.call_args[1]["watermark_text"] == "PyBR"
    assert output.stem in result.stdout


def test_cli_rotate(sample_image: Path, tmp_path: Path, monkeypatch: MonkeyPatch) -> None:
    output = tmp_path / "rotated.jpg"
    mock_transformation_function = MagicMock(return_value=output)
    monkeypatch.setattr(
        "pybr_tutorial_decorator.cli.transformer.apply_transformations",
        mock_transformation_function,
    )
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
    assert mock_transformation_function.call_count == 1
    assert mock_transformation_function.call_args[1]["rotate_degrees"] == 45
    assert mock_transformation_function.call_args[1]["rotate_direction"] == "left"
    assert "Saved transformed image" in result.stdout
    assert output.stem in result.stdout



def test_cli_multiple_transformations(
    sample_image: Path, tmp_path: Path, monkeypatch: MonkeyPatch
) -> None:
    output = tmp_path / "combo.jpg"
    mock_transformation_function = MagicMock(return_value=output)
    monkeypatch.setattr(
        "pybr_tutorial_decorator.cli.transformer.apply_transformations",
        mock_transformation_function,
    )
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
    assert mock_transformation_function.call_count == 1
    assert mock_transformation_function.call_args[1]["to_black_and_white"]
    assert mock_transformation_function.call_args[1]["watermark_text"] == "PyBR"
    assert mock_transformation_function.call_args[1]["rotate_degrees"] == 90
    assert mock_transformation_function.call_args[1]["rotate_direction"] == "left"
    assert "Saved transformed image" in result.stdout
    assert output.stem in result.stdout
