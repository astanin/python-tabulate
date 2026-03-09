"""Command-line interface."""

import os
import subprocess
import sys
import tempfile

from common import assert_equal

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
    x = subprocess.Popen(
        cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    input_buf = input.encode() if input else None
    out, err = x.communicate(input=input_buf)
    out = out.decode("utf-8")
    if x.returncode != 0:
        raise OSError(err)
    return out


class TemporaryTextFile:
    def __init__(self):
        self.tmpfile = None

    def __enter__(self):
        self.tmpfile = tempfile.NamedTemporaryFile("w+", prefix="tabulate-test-tmp-", delete=False)
        return self.tmpfile

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.tmpfile:
            self.tmpfile.close()
            os.unlink(self.tmpfile.name)


def test_script_from_stdin_to_stdout():
    """Command line utility: read from stdin, print to stdout"""
    cmd = [sys.executable, "tabulate/cli.py"]
    out = run_and_capture_stdout(cmd, input=sample_input())
    expected = SAMPLE_SIMPLE_FORMAT
    print("got:     ", repr(out))
    print("expected:", repr(expected))
    assert_equal(out.splitlines(), expected.splitlines())


def test_script_from_file_to_stdout():
    """Command line utility: read from file, print to stdout"""
    with TemporaryTextFile() as tmpfile:
        tmpfile.write(sample_input())
        tmpfile.seek(0)
        cmd = [sys.executable, "tabulate/cli.py", tmpfile.name]
        out = run_and_capture_stdout(cmd)
        expected = SAMPLE_SIMPLE_FORMAT
        print("got:     ", repr(out))
        print("expected:", repr(expected))
        assert_equal(out.splitlines(), expected.splitlines())


def test_script_from_file_to_file():
    """Command line utility: read from file, write to file"""
    with TemporaryTextFile() as input_file:
        with TemporaryTextFile() as output_file:
            input_file.write(sample_input())
            input_file.seek(0)
            cmd = [
                sys.executable,
                "tabulate/cli.py",
                "-o",
                output_file.name,
                input_file.name,
            ]
            out = run_and_capture_stdout(cmd)
            # check that nothing is printed to stdout
            expected = ""
            print("got:     ", repr(out))
            print("expected:", repr(expected))
            assert_equal(out.splitlines(), expected.splitlines())
            # check that the output was written to file
            output_file.seek(0)
            out = output_file.file.read()
            expected = SAMPLE_SIMPLE_FORMAT
            print("got:     ", repr(out))
            print("expected:", repr(expected))
            assert_equal(out.splitlines(), expected.splitlines())


def test_script_header_option():
    """Command line utility: -1, --header option"""
    for option in ["-1", "--header"]:
        cmd = [sys.executable, "tabulate/cli.py", option]
        raw_table = sample_input(with_headers=True)
        out = run_and_capture_stdout(cmd, input=raw_table)
        expected = SAMPLE_SIMPLE_FORMAT_WITH_HEADERS
        print(out)
        print("got:     ", repr(out))
        print("expected:", repr(expected))
        assert_equal(out.splitlines(), expected.splitlines())


def test_script_sep_option():
    """Command line utility: -s, --sep option"""
    for option in ["-s", "--sep"]:
        cmd = [sys.executable, "tabulate/cli.py", option, ","]
        raw_table = sample_input(sep=",")
        out = run_and_capture_stdout(cmd, input=raw_table)
        expected = SAMPLE_SIMPLE_FORMAT
        print("got:     ", repr(out))
        print("expected:", repr(expected))
        assert_equal(out.splitlines(), expected.splitlines())


def test_script_floatfmt_option():
    """Command line utility: -F, --float option"""
    for option in ["-F", "--float"]:
        cmd = [
            sys.executable,
            "tabulate/cli.py",
            option,
            ".1e",
            "--format",
            "grid",
        ]
        raw_table = sample_input()
        out = run_and_capture_stdout(cmd, input=raw_table)
        expected = SAMPLE_GRID_FORMAT_WITH_DOT1E_FLOATS
        print("got:     ", repr(out))
        print("expected:", repr(expected))
        assert_equal(out.splitlines(), expected.splitlines())


def test_script_format_option():
    """Command line utility: -f, --format option"""
    for option in ["-f", "--format"]:
        cmd = [sys.executable, "tabulate/cli.py", "-1", option, "grid"]
        raw_table = sample_input(with_headers=True)
        out = run_and_capture_stdout(cmd, input=raw_table)
        expected = SAMPLE_GRID_FORMAT_WITH_HEADERS
        print(out)
        print("got:     ", repr(out))
        print("expected:", repr(expected))
        assert_equal(out.splitlines(), expected.splitlines())


SAMPLE_INPUT_JSONL = "\n".join(
    [
        '{"id": 1, "name": "Alice", "email": "alice@example.com"}',
        '{"id": 2, "name": "Bob", "email": "bob@example.com"}',
    ]
)

SAMPLE_GRID_FORMAT = "\n".join(
    [
        "+------+--------+-------------------+",
        "|   id | name   | email             |",
        "+======+========+===================+",
        "|    1 | Alice  | alice@example.com |",
        "+------+--------+-------------------+",
        "|    2 | Bob    | bob@example.com   |",
        "+------+--------+-------------------+",
    ]
)


def test_module_jsonl_from_stdin():
    """Command line utility: python -m tabulate with JSONL input from stdin"""
    cmd = [sys.executable, "-m", "tabulate", "-r", "jsonl", "-f", "grid"]
    out = run_and_capture_stdout(cmd, input=SAMPLE_INPUT_JSONL)
    expected = SAMPLE_GRID_FORMAT
    print("got:     ", repr(out))
    print("expected:", repr(expected))
    assert_equal(out.splitlines(), expected.splitlines())


SAMPLE_REMAPPED_HEADERS = "\n".join(
    [
        "  ID  First Name    Email",
        "----  ------------  -----------------",
        "   1  Alice         alice@example.com",
        "   2  Bob           bob@example.com",
    ]
)


SAMPLE_INPUT_CSV = (
    'id,name,email,"""favorite"" fruit"\n'
    '1,Alice,alice@example.com,"apple, kiwi"\n'
    '2,Bob,bob@example.com,"banana,\norange,\nlychee"\n'
    "3,Carol,,pear\n"
)

SAMPLE_CSV_FORMAT = "\n".join(
    [
        "--  -----  -----------------  ----------------",
        "id  name   email              \"favorite\" fruit",
        "1   Alice  alice@example.com  apple, kiwi",
        "2   Bob    bob@example.com    banana,",
        "                              orange,",
        "                              lychee",
        "3   Carol                     pear",
        "--  -----  -----------------  ----------------",
    ]
)

def test_module_csv_from_stdin():
    """Command line utility: python -m tabulate with CSV input from stdin"""
    cmd = [sys.executable, "-m", "tabulate", "-r", "csv"]
    out = run_and_capture_stdout(cmd, input=SAMPLE_INPUT_CSV)
    expected = SAMPLE_CSV_FORMAT
    print("got:     ", repr(out))
    print("expected:", repr(expected))
    assert_equal(out.splitlines(), expected.splitlines())


def test_module_jsonl_remapped_headers():
    """Command line utility: --headers with key:header remapping for JSONL input"""
    cmd = [
        sys.executable, "-m", "tabulate",
        "-r", "jsonl",
        "--headers", "id:ID,name:First Name,email:Email",
    ]
    out = run_and_capture_stdout(cmd, input=SAMPLE_INPUT_JSONL)
    expected = SAMPLE_REMAPPED_HEADERS
    print("got:     ", repr(out))
    print("expected:", repr(expected))
    assert_equal(out.splitlines(), expected.splitlines())
