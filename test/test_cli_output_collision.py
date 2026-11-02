"""The CLI must not truncate an input file while opening its output."""

import os
from pathlib import Path
import subprocess
import sys

import pytest


@pytest.mark.parametrize(
    ("fileformat", "data"),
    [
        ("rsv", "alpha 1\nbeta 2\n"),
        ("csv", "alpha,1\nbeta,2\n"),
        ("jsonl", '{"name": "alpha", "value": 1}\n{"name": "beta", "value": 2}\n'),
    ],
)
@pytest.mark.parametrize("output_kind", ["same", "hardlink", "different"])
def test_cli_input_output_files(tmp_path, fileformat, data, output_kind):
    source = tmp_path / "input.txt"
    source.write_text(data, encoding="utf-8")
    output = source if output_kind == "same" else tmp_path / "output.txt"
    if output_kind == "hardlink":
        os.link(source, output)

    result = subprocess.run(
        [
            sys.executable,
            str(Path(__file__).parents[1] / "tabulate" / "cli.py"),
            "--read",
            fileformat,
            "--output",
            str(output),
            str(source),
        ],
        capture_output=True,
        text=True,
    )

    assert source.read_text(encoding="utf-8") == data
    if output_kind == "different":
        assert result.returncode == 0
        assert "alpha" in output.read_text(encoding="utf-8")
        assert "beta" in output.read_text(encoding="utf-8")
    else:
        assert result.returncode != 0
        assert "input" in result.stderr.lower()
        assert "output" in result.stderr.lower()
