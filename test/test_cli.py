"""Command-line interface.

"""

import os
import sys
import subprocess
import tempfile

SAMPLE_SIMPLE_FORMAT = "\n".join(
    [
        "-----  ------  -------------",
        "Sun    696000     1.9891e+09",
        "Earth    6371  5973.6",
        "Moon     1737    73.5",
        "Mars     3390   641.85",
        "-----  ------  -------------",
    ]
)


SAMPLE_SIMPLE_FORMAT_WITH_HEADERS = "\n".join(
    [
        "Planet      Radius           Mass",
        "--------  --------  -------------",
        "Sun         696000     1.9891e+09",
        "Earth         6371  5973.6",
        "Moon          1737    73.5",
        "Mars          3390   641.85",
    ]
)


SAMPLE_GRID_FORMAT_WITH_HEADERS = "\n".join(
    [
        "+----------+----------+---------------+",
        "| Planet   |   Radius |          Mass |",
        "+==========+==========+===============+",
        "| Sun      |   696000 |    1.9891e+09 |",
        "+----------+----------+---------------+",
        "| Earth    |     6371 | 5973.6        |",
        "+----------+----------+---------------+",
        "| Moon     |     1737 |   73.5        |",
        "+----------+----------+---------------+",
        "| Mars     |     3390 |  641.85       |",
        "+----------+----------+---------------+",
    ]
)


SAMPLE_GRID_FORMAT_WITH_DOT1E_FLOATS = "\n".join(
    [
        "+-------+--------+---------+",
        "| Sun   | 696000 | 2.0e+09 |",
        "+-------+--------+---------+",
        "| Earth |   6371 | 6.0e+03 |",
        "+-------+--------+---------+",
        "| Moon  |   1737 | 7.4e+01 |",
        "+-------+--------+---------+",
        "| Mars  |   3390 | 6.4e+02 |",
        "+-------+--------+---------+",
    ]
)


def sample_input(sep=" ", with_headers=False):
    headers = sep.join(["Planet", "Radius", "Mass"])
    rows = [
        sep.join(["Sun", "696000", "1.9891e9"]),
        sep.join(["Earth", "6371", "5973.6"]),
        sep.join(["Moon", "1737", "73.5"]),
        sep.join(["Mars", "3390", "641.85"]),
    ]
    all_rows = ([headers] + rows) if with_headers else rows
    table = "\n".join(all_rows)
    return table


def run_and_capture_stdout(cmd, input=None):
    proc = subprocess.run(
        cmd, input=input, check=True, capture_output=True, encoding="utf-8"
    )
    return proc.stdout


class TemporaryTextFile:
    def __init__(self):
        self.tmpfile = None

    def __enter__(self):
        self.tmpfile = tempfile.NamedTemporaryFile(
            "w+", prefix="tabulate-test-tmp-", delete=False
        )
        return self.tmpfile

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.tmpfile:
            self.tmpfile.close()
            os.unlink(self.tmpfile.name)


def test_script_from_stdin_to_stdout():
    """Command line utility: read from stdin, print to stdout"""
    cmd = [sys.executable, "tabulate/__init__.py"]
    out = run_and_capture_stdout(cmd, input=sample_input())
    expected = SAMPLE_SIMPLE_FORMAT
    assert out.splitlines() == expected.splitlines()


def test_script_from_file_to_stdout():
    """Command line utility: read from file, print to stdout"""
    with TemporaryTextFile() as tmpfile:
        tmpfile.write(sample_input())
        tmpfile.seek(0)
        cmd = [sys.executable, "tabulate/__init__.py", tmpfile.name]
        out = run_and_capture_stdout(cmd)
        expected = SAMPLE_SIMPLE_FORMAT
        assert out.splitlines() == expected.splitlines()


def test_script_from_file_to_file():
    """Command line utility: read from file, write to file"""
    with TemporaryTextFile() as input_file:
        with TemporaryTextFile() as output_file:
            input_file.write(sample_input())
            input_file.seek(0)
            cmd = [
                sys.executable,
                "tabulate/__init__.py",
                "-o",
                output_file.name,
                input_file.name,
            ]
            out = run_and_capture_stdout(cmd)
            # check that nothing is printed to stdout
            expected = ""
            assert out.splitlines() == expected.splitlines()
            # check that the output was written to file
            output_file.seek(0)
            out = output_file.file.read()
            expected = SAMPLE_SIMPLE_FORMAT
            assert out.splitlines() == expected.splitlines()


def test_script_header_option():
    """Command line utility: -1, --header option"""
    for option in ["-1", "--header"]:
        cmd = [sys.executable, "tabulate/__init__.py", option]
        raw_table = sample_input(with_headers=True)
        out = run_and_capture_stdout(cmd, input=raw_table)
        expected = SAMPLE_SIMPLE_FORMAT_WITH_HEADERS
        assert out.splitlines() == expected.splitlines()


def test_script_sep_option():
    """Command line utility: -s, --sep option"""
    for option in ["-s", "--sep"]:
        cmd = [sys.executable, "tabulate/__init__.py", option, ","]
        raw_table = sample_input(sep=",")
        out = run_and_capture_stdout(cmd, input=raw_table)
        expected = SAMPLE_SIMPLE_FORMAT
        assert out.splitlines() == expected.splitlines()


def test_script_floatfmt_option():
    """Command line utility: -F, --float option"""
    for option in ["-F", "--float"]:
        cmd = [
            sys.executable,
            "tabulate/__init__.py",
            option,
            ".1e",
            "--format",
            "grid",
        ]
        raw_table = sample_input()
        out = run_and_capture_stdout(cmd, input=raw_table)
        expected = SAMPLE_GRID_FORMAT_WITH_DOT1E_FLOATS
        assert out.splitlines() == expected.splitlines()


def test_script_format_option():
    """Command line utility: -f, --format option"""
    for option in ["-f", "--format"]:
        cmd = [sys.executable, "tabulate/__init__.py", "-1", option, "grid"]
        raw_table = sample_input(with_headers=True)
        out = run_and_capture_stdout(cmd, input=raw_table)
        expected = SAMPLE_GRID_FORMAT_WITH_HEADERS
        assert out.splitlines() == expected.splitlines()
