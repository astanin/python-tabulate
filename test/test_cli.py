"""Command-line interface."""

import contextlib
import io
import os
import subprocess
import sys
import tempfile
from unittest.mock import patch

from common import assert_equal
from tabulate.cli import _main


class _UnclosableStringIO(io.StringIO):
    """StringIO that ignores close() so getvalue() works after a 'with' block."""
    def close(self):
        pass  # _main does `with sys.stdout as out:`, which would close a plain StringIO


def run_main_in_process(args, input_text=None):
    """Call _main() in-process, capturing stdout. Returns the captured output."""
    stdin = io.StringIO(input_text) if input_text is not None else sys.stdin
    stdout = _UnclosableStringIO()
    with patch("sys.argv", ["tabulate"] + args), \
         patch("sys.stdin", stdin), \
         contextlib.redirect_stdout(stdout):
        _main()
    return stdout.getvalue()

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


# ---------------------------------------------------------------------------
# In-process tests: same scenarios as above but calling _main() directly so
# that coverage.py can instrument the code in tabulate/cli.py.
# ---------------------------------------------------------------------------

def test_inprocess_stdin_to_stdout():
    """In-process: read RSV from stdin, print to stdout"""
    out = run_main_in_process([], input_text=sample_input())
    assert_equal(out.splitlines(), SAMPLE_SIMPLE_FORMAT.splitlines())


def test_inprocess_header_option():
    """In-process: -1 / --header / --headers firstrow"""
    for args in [["-1"], ["--header"], ["--headers", "firstrow"]]:
        out = run_main_in_process(args, input_text=sample_input(with_headers=True))
        assert_equal(out.splitlines(), SAMPLE_SIMPLE_FORMAT_WITH_HEADERS.splitlines())


def test_inprocess_sep_option():
    """In-process: -s / --sep"""
    for opt in ["-s", "--sep"]:
        out = run_main_in_process([opt, ","], input_text=sample_input(sep=","))
        assert_equal(out.splitlines(), SAMPLE_SIMPLE_FORMAT.splitlines())


def test_inprocess_floatfmt_option():
    """In-process: -F / --float"""
    for opt in ["-F", "--float"]:
        out = run_main_in_process([opt, ".1e", "--format", "grid"], input_text=sample_input())
        assert_equal(out.splitlines(), SAMPLE_GRID_FORMAT_WITH_DOT1E_FLOATS.splitlines())


def test_inprocess_format_option():
    """In-process: -f / --format"""
    for opt in ["-f", "--format"]:
        out = run_main_in_process(["-1", opt, "grid"], input_text=sample_input(with_headers=True))
        assert_equal(out.splitlines(), SAMPLE_GRID_FORMAT_WITH_HEADERS.splitlines())


def test_inprocess_file_to_file():
    """In-process: read from file, write to file (-o)"""
    with TemporaryTextFile() as input_file:
        with TemporaryTextFile() as output_file:
            input_file.write(sample_input())
            input_file.flush()
            run_main_in_process(["-o", output_file.name, input_file.name])
            output_file.seek(0)
            out = output_file.file.read()
            assert_equal(out.splitlines(), SAMPLE_SIMPLE_FORMAT.splitlines())


def test_inprocess_jsonl_from_stdin():
    """In-process: JSONL input from stdin, grid format"""
    out = run_main_in_process(["-r", "jsonl", "-f", "grid"], input_text=SAMPLE_INPUT_JSONL)
    assert_equal(out.splitlines(), SAMPLE_GRID_FORMAT.splitlines())


def test_inprocess_jsonl_remapped_headers():
    """In-process: JSONL input with key:header remapping"""
    out = run_main_in_process(
        ["-r", "jsonl", "--headers", "id:ID,name:First Name,email:Email"],
        input_text=SAMPLE_INPUT_JSONL,
    )
    assert_equal(out.splitlines(), SAMPLE_REMAPPED_HEADERS.splitlines())


def test_inprocess_csv_from_stdin():
    """In-process: CSV input from stdin"""
    out = run_main_in_process(["-r", "csv"], input_text=SAMPLE_INPUT_CSV)
    assert_equal(out.splitlines(), SAMPLE_CSV_FORMAT.splitlines())


def test_inprocess_invalid_option():
    """In-process: unrecognised option exits with code 2"""
    import pytest
    with pytest.raises(SystemExit) as exc_info:
        run_main_in_process(["--no-such-option"], input_text="a b\n1 2\n")
    assert exc_info.value.code == 2


def test_inprocess_help_option():
    """In-process: --help / -h exits with code 0"""
    import pytest
    for opt in ["-h", "--help"]:
        with pytest.raises(SystemExit) as exc_info:
            run_main_in_process([opt], input_text="")
        assert exc_info.value.code == 0


def test_inprocess_invalid_format():
    """In-process: unknown --format value exits with code 3"""
    import pytest
    with pytest.raises(SystemExit) as exc_info:
        run_main_in_process(["-f", "nosuchformat"], input_text="a b\n1 2\n")
    assert exc_info.value.code == 3


def test_inprocess_invalid_fileformat():
    """In-process: unknown --read value exits with code 3"""
    import pytest
    with pytest.raises(SystemExit) as exc_info:
        run_main_in_process(["-r", "xml"], input_text="")
    assert exc_info.value.code == 3


def test_inprocess_int_option():
    """In-process: -I / --int option"""
    jsonl_ints = '{"n": 1000000}\n{"n": 2000000}\n'
    for opt in ["-I", "--int"]:
        out = run_main_in_process(
            ["-r", "jsonl", opt, "_"], input_text=jsonl_ints
        )
        assert "1_000_000" in out


def test_inprocess_colalign_option():
    """In-process: --colalign option"""
    out = run_main_in_process(
        ["--colalign", "left left left", "-1"],
        input_text=sample_input(with_headers=True),
    )
    assert "Planet" in out


def test_inprocess_rsv_custom_headers():
    """In-process: --headers with custom column names for RSV input"""
    out = run_main_in_process(
        ["--headers", "Planet,Radius,Mass"], input_text=sample_input()
    )
    assert_equal(out.splitlines(), SAMPLE_SIMPLE_FORMAT_WITH_HEADERS.splitlines())


def test_inprocess_csv_custom_headers():
    """In-process: --headers with custom column names overrides CSV first row"""
    csv_data = "Sun,696000,1.9891e9\nEarth,6371,5973.6\n"
    out = run_main_in_process(
        ["-r", "csv", "--headers", "Planet,Radius,Mass"], input_text=csv_data
    )
    assert "Planet" in out and "Radius" in out and "Mass" in out


def test_inprocess_stdin_dash_arg():
    """In-process: '-' as filename reads from stdin"""
    out = run_main_in_process(["-"], input_text=sample_input())
    assert_equal(out.splitlines(), SAMPLE_SIMPLE_FORMAT.splitlines())


def test_inprocess_jsonl_malformed_headers():
    """In-process: malformed key:header mapping falls back to no headers"""
    # A header spec without ':' can't be parsed into key-value pairs;
    # _main catches the ValueError and proceeds with an empty headers list.
    out = run_main_in_process(
        ["-r", "jsonl", "--headers", "no_colon_here"],
        input_text=SAMPLE_INPUT_JSONL,
    )
    # output should still be produced (graceful fallback), with raw keys as headers
    assert out.strip() != ""
