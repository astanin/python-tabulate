# -*- coding: utf-8 -*-

"""Test output of the various forms of tabular data."""

from __future__ import print_function
from __future__ import unicode_literals
import tabulate as tabulate_module
from tabulate import tabulate, simple_separated_format
from common import assert_equal, raises, skip


# _test_table shows
#  - coercion of a string to a number,
#  - left alignment of text,
#  - decimal point alignment of numbers
_test_table = [["spam", 41.9999], ["eggs", "451.0"]]
_test_table_headers = ["strings", "numbers"]


def test_plain():
    "Output: plain with headers"
    expected = "\n".join(
        ["strings      numbers", "spam         41.9999", "eggs        451"]
    )
    result = tabulate(_test_table, _test_table_headers, tablefmt="plain")
    assert_equal(expected, result)


def test_plain_headerless():
    "Output: plain without headers"
    expected = "\n".join(["spam   41.9999", "eggs  451"])
    result = tabulate(_test_table, tablefmt="plain")
    assert_equal(expected, result)


def test_plain_multiline_headerless():
    "Output: plain with multiline cells without headers"
    table = [["foo bar\nbaz\nbau", "hello"], ["", "multiline\nworld"]]
    expected = "\n".join(
        ["foo bar    hello", "  baz", "  bau", "         multiline", "           world"]
    )
    result = tabulate(table, stralign="center", tablefmt="plain")
    assert_equal(expected, result)


def test_plain_multiline():
    "Output: plain with multiline cells with headers"
    table = [[2, "foo\nbar"]]
    headers = ("more\nspam \x1b[31meggs\x1b[0m", "more spam\n& eggs")
    expected = "\n".join(
        [
            "       more  more spam",
            "  spam \x1b[31meggs\x1b[0m  & eggs",
            "          2  foo",
            "             bar",
        ]
    )
    result = tabulate(table, headers, tablefmt="plain")
    assert_equal(expected, result)


def test_plain_multiline_with_links():
    "Output: plain with multiline cells with links and headers"
    table = [[2, "foo\nbar"]]
    headers = ("more\nspam \x1b]8;;target\x1b\\eggs\x1b]8;;\x1b\\", "more spam\n& eggs")
    expected = "\n".join(
        [
            "       more  more spam",
            "  spam \x1b]8;;target\x1b\\eggs\x1b]8;;\x1b\\  & eggs",
            "          2  foo",
            "             bar",
        ]
    )
    result = tabulate(table, headers, tablefmt="plain")
    assert_equal(expected, result)


def test_plain_multiline_with_empty_cells():
    "Output: plain with multiline cells and empty cells with headers"
    table = [
        ["hdr", "data", "fold"],
        ["1", "", ""],
        ["2", "very long data", "fold\nthis"],
    ]
    expected = "\n".join(
        [
            "  hdr  data            fold",
            "    1",
            "    2  very long data  fold",
            "                       this",
        ]
    )
    result = tabulate(table, headers="firstrow", tablefmt="plain")
    assert_equal(expected, result)


def test_plain_multiline_with_empty_cells_headerless():
    "Output: plain with multiline cells and empty cells without headers"
    table = [["0", "", ""], ["1", "", ""], ["2", "very long data", "fold\nthis"]]
    expected = "\n".join(
        ["0", "1", "2  very long data  fold", "                   this"]
    )
    result = tabulate(table, tablefmt="plain")
    assert_equal(expected, result)


def test_simple():
    "Output: simple with headers"
    expected = "\n".join(
        [
            "strings      numbers",
            "---------  ---------",
            "spam         41.9999",
            "eggs        451",
        ]
    )
    result = tabulate(_test_table, _test_table_headers, tablefmt="simple")
    assert_equal(expected, result)


def test_simple_multiline_2():
    "Output: simple with multiline cells"
    expected = "\n".join(
        [
            " key     value",
            "-----  ---------",
            " foo      bar",
            "spam   multiline",
            "         world",
        ]
    )
    table = [["key", "value"], ["foo", "bar"], ["spam", "multiline\nworld"]]
    result = tabulate(table, headers="firstrow", stralign="center", tablefmt="simple")
    assert_equal(expected, result)


def test_simple_headerless():
    "Output: simple without headers"
    expected = "\n".join(
        ["----  --------", "spam   41.9999", "eggs  451", "----  --------"]
    )
    result = tabulate(_test_table, tablefmt="simple")
    assert_equal(expected, result)


def test_simple_multiline_headerless():
    "Output: simple with multiline cells without headers"
    table = [["foo bar\nbaz\nbau", "hello"], ["", "multiline\nworld"]]
    expected = "\n".join(
        [
            "-------  ---------",
            "foo bar    hello",
            "  baz",
            "  bau",
            "         multiline",
            "           world",
            "-------  ---------",
        ]
    )
    result = tabulate(table, stralign="center", tablefmt="simple")
    assert_equal(expected, result)


def test_simple_multiline():
    "Output: simple with multiline cells with headers"
    table = [[2, "foo\nbar"]]
    headers = ("more\nspam \x1b[31meggs\x1b[0m", "more spam\n& eggs")
    expected = "\n".join(
        [
            "       more  more spam",
            "  spam \x1b[31meggs\x1b[0m  & eggs",
            "-----------  -----------",
            "          2  foo",
            "             bar",
        ]
    )
    result = tabulate(table, headers, tablefmt="simple")
    assert_equal(expected, result)


def test_simple_multiline_with_links():
    "Output: simple with multiline cells with links and headers"
    table = [[2, "foo\nbar"]]
    headers = ("more\nspam \x1b]8;;target\x1b\\eggs\x1b]8;;\x1b\\", "more spam\n& eggs")
    expected = "\n".join(
        [
            "       more  more spam",
            "  spam \x1b]8;;target\x1b\\eggs\x1b]8;;\x1b\\  & eggs",
            "-----------  -----------",
            "          2  foo",
            "             bar",
        ]
    )
    result = tabulate(table, headers, tablefmt="simple")
    assert_equal(expected, result)


def test_simple_multiline_with_empty_cells():
    "Output: simple with multiline cells and empty cells with headers"
    table = [
        ["hdr", "data", "fold"],
        ["1", "", ""],
        ["2", "very long data", "fold\nthis"],
    ]
    expected = "\n".join(
        [
            "  hdr  data            fold",
            "-----  --------------  ------",
            "    1",
            "    2  very long data  fold",
            "                       this",
        ]
    )
    result = tabulate(table, headers="firstrow", tablefmt="simple")
    assert_equal(expected, result)


def test_simple_multiline_with_empty_cells_headerless():
    "Output: simple with multiline cells and empty cells without headers"
    table = [["0", "", ""], ["1", "", ""], ["2", "very long data", "fold\nthis"]]
    expected = "\n".join(
        [
            "-  --------------  ----",
            "0",
            "1",
            "2  very long data  fold",
            "                   this",
            "-  --------------  ----",
        ]
    )
    result = tabulate(table, tablefmt="simple")
    assert_equal(expected, result)


def test_github():
    "Output: github with headers"
    expected = "\n".join(
        [
            "| strings   |   numbers |",
            "|-----------|-----------|",
            "| spam      |   41.9999 |",
            "| eggs      |  451      |",
        ]
    )
    result = tabulate(_test_table, _test_table_headers, tablefmt="github")
    assert_equal(expected, result)


def test_grid():
    "Output: grid with headers"
    expected = "\n".join(
        [
            "+-----------+-----------+",
            "| strings   |   numbers |",
            "+===========+===========+",
            "| spam      |   41.9999 |",
            "+-----------+-----------+",
            "| eggs      |  451      |",
            "+-----------+-----------+",
        ]
    )
    result = tabulate(_test_table, _test_table_headers, tablefmt="grid")
    assert_equal(expected, result)


def test_grid_wide_characters():
    "Output: grid with wide characters in headers"
    try:
        import wcwidth  # noqa
    except ImportError:
        skip("test_grid_wide_characters is skipped")
    headers = list(_test_table_headers)
    headers[1] = "配列"
    expected = "\n".join(
        [
            "+-----------+----------+",
            "| strings   |     配列 |",
            "+===========+==========+",
            "| spam      |  41.9999 |",
            "+-----------+----------+",
            "| eggs      | 451      |",
            "+-----------+----------+",
        ]
    )
    result = tabulate(_test_table, headers, tablefmt="grid")
    assert_equal(expected, result)


def test_grid_headerless():
    "Output: grid without headers"
    expected = "\n".join(
        [
            "+------+----------+",
            "| spam |  41.9999 |",
            "+------+----------+",
            "| eggs | 451      |",
            "+------+----------+",
        ]
    )
    result = tabulate(_test_table, tablefmt="grid")
    assert_equal(expected, result)


def test_grid_multiline_headerless():
    "Output: grid with multiline cells without headers"
    table = [["foo bar\nbaz\nbau", "hello"], ["", "multiline\nworld"]]
    expected = "\n".join(
        [
            "+---------+-----------+",
            "| foo bar |   hello   |",
            "|   baz   |           |",
            "|   bau   |           |",
            "+---------+-----------+",
            "|         | multiline |",
            "|         |   world   |",
            "+---------+-----------+",
        ]
    )
    result = tabulate(table, stralign="center", tablefmt="grid")
    assert_equal(expected, result)


def test_grid_multiline():
    "Output: grid with multiline cells with headers"
    table = [[2, "foo\nbar"]]
    headers = ("more\nspam \x1b[31meggs\x1b[0m", "more spam\n& eggs")
    expected = "\n".join(
        [
            "+-------------+-------------+",
            "|        more | more spam   |",
            "|   spam \x1b[31meggs\x1b[0m | & eggs      |",
            "+=============+=============+",
            "|           2 | foo         |",
            "|             | bar         |",
            "+-------------+-------------+",
        ]
    )
    result = tabulate(table, headers, tablefmt="grid")
    assert_equal(expected, result)


def test_grid_multiline_with_empty_cells():
    "Output: grid with multiline cells and empty cells with headers"
    table = [
        ["hdr", "data", "fold"],
        ["1", "", ""],
        ["2", "very long data", "fold\nthis"],
    ]
    expected = "\n".join(
        [
            "+-------+----------------+--------+",
            "|   hdr | data           | fold   |",
            "+=======+================+========+",
            "|     1 |                |        |",
            "+-------+----------------+--------+",
            "|     2 | very long data | fold   |",
            "|       |                | this   |",
            "+-------+----------------+--------+",
        ]
    )
    result = tabulate(table, headers="firstrow", tablefmt="grid")
    assert_equal(expected, result)


def test_grid_multiline_with_empty_cells_headerless():
    "Output: grid with multiline cells and empty cells without headers"
    table = [["0", "", ""], ["1", "", ""], ["2", "very long data", "fold\nthis"]]
    expected = "\n".join(
        [
            "+---+----------------+------+",
            "| 0 |                |      |",
            "+---+----------------+------+",
            "| 1 |                |      |",
            "+---+----------------+------+",
            "| 2 | very long data | fold |",
            "|   |                | this |",
            "+---+----------------+------+",
        ]
    )
    result = tabulate(table, tablefmt="grid")
    assert_equal(expected, result)


def test_fancy_grid():
    "Output: fancy_grid with headers"
    expected = "\n".join(
        [
            "╒═══════════╤═══════════╕",
            "│ strings   │   numbers │",
            "╞═══════════╪═══════════╡",
            "│ spam      │   41.9999 │",
            "├───────────┼───────────┤",
            "│ eggs      │  451      │",
            "╘═══════════╧═══════════╛",
        ]
    )
    result = tabulate(_test_table, _test_table_headers, tablefmt="fancy_grid")
    assert_equal(expected, result)


def test_fancy_grid_headerless():
    "Output: fancy_grid without headers"
    expected = "\n".join(
        [
            "╒══════╤══════════╕",
            "│ spam │  41.9999 │",
            "├──────┼──────────┤",
            "│ eggs │ 451      │",
            "╘══════╧══════════╛",
        ]
    )
    result = tabulate(_test_table, tablefmt="fancy_grid")
    assert_equal(expected, result)


def test_fancy_grid_multiline_headerless():
    "Output: fancy_grid with multiline cells without headers"
    table = [["foo bar\nbaz\nbau", "hello"], ["", "multiline\nworld"]]
    expected = "\n".join(
        [
            "╒═════════╤═══════════╕",
            "│ foo bar │   hello   │",
            "│   baz   │           │",
            "│   bau   │           │",
            "├─────────┼───────────┤",
            "│         │ multiline │",
            "│         │   world   │",
            "╘═════════╧═══════════╛",
        ]
    )
    result = tabulate(table, stralign="center", tablefmt="fancy_grid")
    assert_equal(expected, result)


def test_fancy_grid_multiline():
    "Output: fancy_grid with multiline cells with headers"
    table = [[2, "foo\nbar"]]
    headers = ("more\nspam \x1b[31meggs\x1b[0m", "more spam\n& eggs")
    expected = "\n".join(
        [
            "╒═════════════╤═════════════╕",
            "│        more │ more spam   │",
            "│   spam \x1b[31meggs\x1b[0m │ & eggs      │",
            "╞═════════════╪═════════════╡",
            "│           2 │ foo         │",
            "│             │ bar         │",
            "╘═════════════╧═════════════╛",
        ]
    )
    result = tabulate(table, headers, tablefmt="fancy_grid")
    assert_equal(expected, result)


def test_fancy_grid_multiline_with_empty_cells():
    "Output: fancy_grid with multiline cells and empty cells with headers"
    table = [
        ["hdr", "data", "fold"],
        ["1", "", ""],
        ["2", "very long data", "fold\nthis"],
    ]
    expected = "\n".join(
        [
            "╒═══════╤════════════════╤════════╕",
            "│   hdr │ data           │ fold   │",
            "╞═══════╪════════════════╪════════╡",
            "│     1 │                │        │",
            "├───────┼────────────────┼────────┤",
            "│     2 │ very long data │ fold   │",
            "│       │                │ this   │",
            "╘═══════╧════════════════╧════════╛",
        ]
    )
    result = tabulate(table, headers="firstrow", tablefmt="fancy_grid")
    assert_equal(expected, result)


def test_fancy_grid_multiline_with_empty_cells_headerless():
    "Output: fancy_grid with multiline cells and empty cells without headers"
    table = [["0", "", ""], ["1", "", ""], ["2", "very long data", "fold\nthis"]]
    expected = "\n".join(
        [
            "╒═══╤════════════════╤══════╕",
            "│ 0 │                │      │",
            "├───┼────────────────┼──────┤",
            "│ 1 │                │      │",
            "├───┼────────────────┼──────┤",
            "│ 2 │ very long data │ fold │",
            "│   │                │ this │",
            "╘═══╧════════════════╧══════╛",
        ]
    )
    result = tabulate(table, tablefmt="fancy_grid")
    assert_equal(expected, result)


def test_pipe():
    "Output: pipe with headers"
    expected = "\n".join(
        [
            "| strings   |   numbers |",
            "|:----------|----------:|",
            "| spam      |   41.9999 |",
            "| eggs      |  451      |",
        ]
    )
    result = tabulate(_test_table, _test_table_headers, tablefmt="pipe")
    assert_equal(expected, result)


def test_pipe_headerless():
    "Output: pipe without headers"
    expected = "\n".join(
        ["|:-----|---------:|", "| spam |  41.9999 |", "| eggs | 451      |"]
    )
    result = tabulate(_test_table, tablefmt="pipe")
    assert_equal(expected, result)


def test_presto():
    "Output: presto with headers"
    expected = "\n".join(
        [
            " strings   |   numbers",
            "-----------+-----------",
            " spam      |   41.9999",
            " eggs      |  451",
        ]
    )
    result = tabulate(_test_table, _test_table_headers, tablefmt="presto")
    assert_equal(expected, result)


def test_presto_headerless():
    "Output: presto without headers"
    expected = "\n".join([" spam |  41.9999", " eggs | 451"])
    result = tabulate(_test_table, tablefmt="presto")
    assert_equal(expected, result)


def test_presto_multiline_headerless():
    "Output: presto with multiline cells without headers"
    table = [["foo bar\nbaz\nbau", "hello"], ["", "multiline\nworld"]]
    expected = "\n".join(
        [
            " foo bar |   hello",
            "   baz   |",
            "   bau   |",
            "         | multiline",
            "         |   world",
        ]
    )
    result = tabulate(table, stralign="center", tablefmt="presto")
    assert_equal(expected, result)


def test_presto_multiline():
    "Output: presto with multiline cells with headers"
    table = [[2, "foo\nbar"]]
    headers = ("more\nspam \x1b[31meggs\x1b[0m", "more spam\n& eggs")
    expected = "\n".join(
        [
            "        more | more spam",
            "   spam \x1b[31meggs\x1b[0m | & eggs",
            "-------------+-------------",
            "           2 | foo",
            "             | bar",
        ]
    )
    result = tabulate(table, headers, tablefmt="presto")
    assert_equal(expected, result)


def test_presto_multiline_with_empty_cells():
    "Output: presto with multiline cells and empty cells with headers"
    table = [
        ["hdr", "data", "fold"],
        ["1", "", ""],
        ["2", "very long data", "fold\nthis"],
    ]
    expected = "\n".join(
        [
            "   hdr | data           | fold",
            "-------+----------------+--------",
            "     1 |                |",
            "     2 | very long data | fold",
            "       |                | this",
        ]
    )
    result = tabulate(table, headers="firstrow", tablefmt="presto")
    assert_equal(expected, result)


def test_presto_multiline_with_empty_cells_headerless():
    "Output: presto with multiline cells and empty cells without headers"
    table = [["0", "", ""], ["1", "", ""], ["2", "very long data", "fold\nthis"]]
    expected = "\n".join(
        [
            " 0 |                |",
            " 1 |                |",
            " 2 | very long data | fold",
            "   |                | this",
        ]
    )
    result = tabulate(table, tablefmt="presto")
    assert_equal(expected, result)


def test_orgtbl():
    "Output: orgtbl with headers"
    expected = "\n".join(
        [
            "| strings   |   numbers |",
            "|-----------+-----------|",
            "| spam      |   41.9999 |",
            "| eggs      |  451      |",
        ]
    )
    result = tabulate(_test_table, _test_table_headers, tablefmt="orgtbl")
    assert_equal(expected, result)


def test_orgtbl_headerless():
    "Output: orgtbl without headers"
    expected = "\n".join(["| spam |  41.9999 |", "| eggs | 451      |"])
    result = tabulate(_test_table, tablefmt="orgtbl")
    assert_equal(expected, result)


def test_psql():
    "Output: psql with headers"
    expected = "\n".join(
        [
            "+-----------+-----------+",
            "| strings   |   numbers |",
            "|-----------+-----------|",
            "| spam      |   41.9999 |",
            "| eggs      |  451      |",
            "+-----------+-----------+",
        ]
    )
    result = tabulate(_test_table, _test_table_headers, tablefmt="psql")
    assert_equal(expected, result)


def test_psql_headerless():
    "Output: psql without headers"
    expected = "\n".join(
        [
            "+------+----------+",
            "| spam |  41.9999 |",
            "| eggs | 451      |",
            "+------+----------+",
        ]
    )
    result = tabulate(_test_table, tablefmt="psql")
    assert_equal(expected, result)


def test_psql_multiline_headerless():
    "Output: psql with multiline cells without headers"
    table = [["foo bar\nbaz\nbau", "hello"], ["", "multiline\nworld"]]
    expected = "\n".join(
        [
            "+---------+-----------+",
            "| foo bar |   hello   |",
            "|   baz   |           |",
            "|   bau   |           |",
            "|         | multiline |",
            "|         |   world   |",
            "+---------+-----------+",
        ]
    )
    result = tabulate(table, stralign="center", tablefmt="psql")
    assert_equal(expected, result)


def test_psql_multiline():
    "Output: psql with multiline cells with headers"
    table = [[2, "foo\nbar"]]
    headers = ("more\nspam \x1b[31meggs\x1b[0m", "more spam\n& eggs")
    expected = "\n".join(
        [
            "+-------------+-------------+",
            "|        more | more spam   |",
            "|   spam \x1b[31meggs\x1b[0m | & eggs      |",
            "|-------------+-------------|",
            "|           2 | foo         |",
            "|             | bar         |",
            "+-------------+-------------+",
        ]
    )
    result = tabulate(table, headers, tablefmt="psql")
    assert_equal(expected, result)


def test_psql_multiline_with_empty_cells():
    "Output: psql with multiline cells and empty cells with headers"
    table = [
        ["hdr", "data", "fold"],
        ["1", "", ""],
        ["2", "very long data", "fold\nthis"],
    ]
    expected = "\n".join(
        [
            "+-------+----------------+--------+",
            "|   hdr | data           | fold   |",
            "|-------+----------------+--------|",
            "|     1 |                |        |",
            "|     2 | very long data | fold   |",
            "|       |                | this   |",
            "+-------+----------------+--------+",
        ]
    )
    result = tabulate(table, headers="firstrow", tablefmt="psql")
    assert_equal(expected, result)


def test_psql_multiline_with_empty_cells_headerless():
    "Output: psql with multiline cells and empty cells without headers"
    table = [["0", "", ""], ["1", "", ""], ["2", "very long data", "fold\nthis"]]
    expected = "\n".join(
        [
            "+---+----------------+------+",
            "| 0 |                |      |",
            "| 1 |                |      |",
            "| 2 | very long data | fold |",
            "|   |                | this |",
            "+---+----------------+------+",
        ]
    )
    result = tabulate(table, tablefmt="psql")
    assert_equal(expected, result)


def test_pretty():
    "Output: pretty with headers"
    expected = "\n".join(
        [
            "+---------+---------+",
            "| strings | numbers |",
            "+---------+---------+",
            "|  spam   | 41.9999 |",
            "|  eggs   |  451.0  |",
            "+---------+---------+",
        ]
    )
    result = tabulate(_test_table, _test_table_headers, tablefmt="pretty")
    assert_equal(expected, result)


def test_pretty_headerless():
    "Output: pretty without headers"
    expected = "\n".join(
        [
            "+------+---------+",
            "| spam | 41.9999 |",
            "| eggs |  451.0  |",
            "+------+---------+",
        ]
    )
    result = tabulate(_test_table, tablefmt="pretty")
    assert_equal(expected, result)


def test_pretty_multiline_headerless():
    "Output: pretty with multiline cells without headers"
    table = [["foo bar\nbaz\nbau", "hello"], ["", "multiline\nworld"]]
    expected = "\n".join(
        [
            "+---------+-----------+",
            "| foo bar |   hello   |",
            "|   baz   |           |",
            "|   bau   |           |",
            "|         | multiline |",
            "|         |   world   |",
            "+---------+-----------+",
        ]
    )
    result = tabulate(table, tablefmt="pretty")
    assert_equal(expected, result)


def test_pretty_multiline():
    "Output: pretty with multiline cells with headers"
    table = [[2, "foo\nbar"]]
    headers = ("more\nspam \x1b[31meggs\x1b[0m", "more spam\n& eggs")
    expected = "\n".join(
        [
            "+-----------+-----------+",
            "|   more    | more spam |",
            "| spam \x1b[31meggs\x1b[0m |  & eggs   |",
            "+-----------+-----------+",
            "|     2     |    foo    |",
            "|           |    bar    |",
            "+-----------+-----------+",
        ]
    )
    result = tabulate(table, headers, tablefmt="pretty")
    assert_equal(expected, result)


def test_pretty_multiline_with_links():
    "Output: pretty with multiline cells with headers"
    table = [[2, "foo\nbar"]]
    headers = ("more\nspam \x1b]8;;target\x1b\\eggs\x1b]8;;\x1b\\", "more spam\n& eggs")
    expected = "\n".join(
        [
            "+-----------+-----------+",
            "|   more    | more spam |",
            "| spam \x1b]8;;target\x1b\\eggs\x1b]8;;\x1b\\ |  & eggs   |",
            "+-----------+-----------+",
            "|     2     |    foo    |",
            "|           |    bar    |",
            "+-----------+-----------+",
        ]
    )
    result = tabulate(table, headers, tablefmt="pretty")
    assert_equal(expected, result)


def test_pretty_multiline_with_empty_cells():
    "Output: pretty with multiline cells and empty cells with headers"
    table = [
        ["hdr", "data", "fold"],
        ["1", "", ""],
        ["2", "very long data", "fold\nthis"],
    ]
    expected = "\n".join(
        [
            "+-----+----------------+------+",
            "| hdr |      data      | fold |",
            "+-----+----------------+------+",
            "|  1  |                |      |",
            "|  2  | very long data | fold |",
            "|     |                | this |",
            "+-----+----------------+------+",
        ]
    )
    result = tabulate(table, headers="firstrow", tablefmt="pretty")
    assert_equal(expected, result)


def test_pretty_multiline_with_empty_cells_headerless():
    "Output: pretty with multiline cells and empty cells without headers"
    table = [["0", "", ""], ["1", "", ""], ["2", "very long data", "fold\nthis"]]
    expected = "\n".join(
        [
            "+---+----------------+------+",
            "| 0 |                |      |",
            "| 1 |                |      |",
            "| 2 | very long data | fold |",
            "|   |                | this |",
            "+---+----------------+------+",
        ]
    )
    result = tabulate(table, tablefmt="pretty")
    assert_equal(expected, result)


def test_jira():
    "Output: jira with headers"
    expected = "\n".join(
        [
            "|| strings   ||   numbers ||",
            "| spam      |   41.9999 |",
            "| eggs      |  451      |",
        ]
    )

    result = tabulate(_test_table, _test_table_headers, tablefmt="jira")
    assert_equal(expected, result)


def test_jira_headerless():
    "Output: jira without headers"
    expected = "\n".join(["| spam |  41.9999 |", "| eggs | 451      |"])

    result = tabulate(_test_table, tablefmt="jira")
    assert_equal(expected, result)


def test_rst():
    "Output: rst with headers"
    expected = "\n".join(
        [
            "=========  =========",
            "strings      numbers",
            "=========  =========",
            "spam         41.9999",
            "eggs        451",
            "=========  =========",
        ]
    )
    result = tabulate(_test_table, _test_table_headers, tablefmt="rst")
    assert_equal(expected, result)


def test_rst_with_empty_values_in_first_column():
    "Output: rst with dots in first column"
    test_headers = ["", "what"]
    test_data = [("", "spam"), ("", "eggs")]
    expected = "\n".join(
        [
            "====  ======",
            "..    what",
            "====  ======",
            "..    spam",
            "..    eggs",
            "====  ======",
        ]
    )
    result = tabulate(test_data, test_headers, tablefmt="rst")
    assert_equal(expected, result)


def test_rst_headerless():
    "Output: rst without headers"
    expected = "\n".join(
        ["====  ========", "spam   41.9999", "eggs  451", "====  ========"]
    )
    result = tabulate(_test_table, tablefmt="rst")
    assert_equal(expected, result)


def test_rst_multiline():
    "Output: rst with multiline cells with headers"
    table = [[2, "foo\nbar"]]
    headers = ("more\nspam \x1b[31meggs\x1b[0m", "more spam\n& eggs")
    expected = "\n".join(
        [
            "===========  ===========",
            "       more  more spam",
            "  spam \x1b[31meggs\x1b[0m  & eggs",
            "===========  ===========",
            "          2  foo",
            "             bar",
            "===========  ===========",
        ]
    )
    result = tabulate(table, headers, tablefmt="rst")
    assert_equal(expected, result)


def test_rst_multiline_with_links():
    "Output: rst with multiline cells with headers"
    table = [[2, "foo\nbar"]]
    headers = ("more\nspam \x1b]8;;target\x1b\\eggs\x1b]8;;\x1b\\", "more spam\n& eggs")
    expected = "\n".join(
        [
            "===========  ===========",
            "       more  more spam",
            "  spam \x1b]8;;target\x1b\\eggs\x1b]8;;\x1b\\  & eggs",
            "===========  ===========",
            "          2  foo",
            "             bar",
            "===========  ===========",
        ]
    )
    result = tabulate(table, headers, tablefmt="rst")
    assert_equal(expected, result)


def test_rst_multiline_with_empty_cells():
    "Output: rst with multiline cells and empty cells with headers"
    table = [
        ["hdr", "data", "fold"],
        ["1", "", ""],
        ["2", "very long data", "fold\nthis"],
    ]
    expected = "\n".join(
        [
            "=====  ==============  ======",
            "  hdr  data            fold",
            "=====  ==============  ======",
            "    1",
            "    2  very long data  fold",
            "                       this",
            "=====  ==============  ======",
        ]
    )
    result = tabulate(table, headers="firstrow", tablefmt="rst")
    assert_equal(expected, result)


def test_rst_multiline_with_empty_cells_headerless():
    "Output: rst with multiline cells and empty cells without headers"
    table = [["0", "", ""], ["1", "", ""], ["2", "very long data", "fold\nthis"]]
    expected = "\n".join(
        [
            "=  ==============  ====",
            "0",
            "1",
            "2  very long data  fold",
            "                   this",
            "=  ==============  ====",
        ]
    )
    result = tabulate(table, tablefmt="rst")
    assert_equal(expected, result)


def test_mediawiki():
    "Output: mediawiki with headers"
    expected = "\n".join(
        [
            '{| class="wikitable" style="text-align: left;"',
            "|+ <!-- caption -->",
            "|-",
            '! strings   !! align="right"|   numbers',
            "|-",
            '| spam      || align="right"|   41.9999',
            "|-",
            '| eggs      || align="right"|  451',
            "|}",
        ]
    )
    result = tabulate(_test_table, _test_table_headers, tablefmt="mediawiki")
    assert_equal(expected, result)


def test_mediawiki_headerless():
    "Output: mediawiki without headers"
    expected = "\n".join(
        [
            '{| class="wikitable" style="text-align: left;"',
            "|+ <!-- caption -->",
            "|-",
            '| spam || align="right"|  41.9999',
            "|-",
            '| eggs || align="right"| 451',
            "|}",
        ]
    )
    result = tabulate(_test_table, tablefmt="mediawiki")
    assert_equal(expected, result)


def test_moinmoin():
    "Output: moinmoin with headers"
    expected = "\n".join(
        [
            "|| ''' strings   ''' ||<style=\"text-align: right;\"> '''   numbers ''' ||",
            '||  spam       ||<style="text-align: right;">    41.9999  ||',
            '||  eggs       ||<style="text-align: right;">   451       ||',
        ]
    )
    result = tabulate(_test_table, _test_table_headers, tablefmt="moinmoin")
    assert_equal(expected, result)


def test_youtrack():
    "Output: youtrack with headers"
    expected = "\n".join(
        [
            "||  strings    ||    numbers  ||",
            "|  spam       |    41.9999  |",
            "|  eggs       |   451       |",
        ]
    )
    result = tabulate(_test_table, _test_table_headers, tablefmt="youtrack")
    assert_equal(expected, result)


def test_moinmoin_headerless():
    "Output: moinmoin without headers"
    expected = "\n".join(
        [
            '||  spam  ||<style="text-align: right;">   41.9999  ||',
            '||  eggs  ||<style="text-align: right;">  451       ||',
        ]
    )
    result = tabulate(_test_table, tablefmt="moinmoin")
    assert_equal(expected, result)


_test_table_html_headers = ["<strings>", "<&numbers&>"]
_test_table_html = [["spam >", 41.9999], ["eggs &", 451.0]]
_test_table_unsafehtml_headers = ["strings", "numbers"]
_test_table_unsafehtml = [
    ["spam", '<font color="red">41.9999</font>'],
    ["eggs", '<font color="red">451.0</font>'],
]


def test_html():
    "Output: html with headers"
    expected = "\n".join(
        [
            "<table>",
            "<thead>",
            '<tr><th>&lt;strings&gt;  </th><th style="text-align: right;">  &lt;&amp;numbers&amp;&gt;</th></tr>',  # noqa
            "</thead>",
            "<tbody>",
            '<tr><td>spam &gt;     </td><td style="text-align: right;">      41.9999</td></tr>',
            '<tr><td>eggs &amp;     </td><td style="text-align: right;">     451     </td></tr>',
            "</tbody>",
            "</table>",
        ]
    )
    result = tabulate(_test_table_html, _test_table_html_headers, tablefmt="html")
    assert_equal(expected, result)
    assert hasattr(result, "_repr_html_")
    assert result._repr_html_() == result.str


def test_unsafehtml():
    "Output: unsafe html with headers"
    expected = "\n".join(
        [
            "<table>",
            "<thead>",
            "<tr><th>strings  </th><th>numbers                         </th></tr>",  # noqa
            "</thead>",
            "<tbody>",
            '<tr><td>spam     </td><td><font color="red">41.9999</font></td></tr>',
            '<tr><td>eggs     </td><td><font color="red">451.0</font>  </td></tr>',
            "</tbody>",
            "</table>",
        ]
    )
    result = tabulate(
        _test_table_unsafehtml, _test_table_unsafehtml_headers, tablefmt="unsafehtml"
    )
    assert_equal(expected, result)
    assert hasattr(result, "_repr_html_")
    assert result._repr_html_() == result.str


def test_html_headerless():
    "Output: html without headers"
    expected = "\n".join(
        [
            "<table>",
            "<tbody>",
            '<tr><td>spam &gt;</td><td style="text-align: right;"> 41.9999</td></tr>',
            '<tr><td>eggs &amp;</td><td style="text-align: right;">451     </td></tr>',
            "</tbody>",
            "</table>",
        ]
    )
    result = tabulate(_test_table_html, tablefmt="html")
    assert_equal(expected, result)
    assert hasattr(result, "_repr_html_")
    assert result._repr_html_() == result.str


def test_unsafehtml_headerless():
    "Output: unsafe html without headers"
    expected = "\n".join(
        [
            "<table>",
            "<tbody>",
            '<tr><td>spam</td><td><font color="red">41.9999</font></td></tr>',
            '<tr><td>eggs</td><td><font color="red">451.0</font>  </td></tr>',
            "</tbody>",
            "</table>",
        ]
    )
    result = tabulate(_test_table_unsafehtml, tablefmt="unsafehtml")
    assert_equal(expected, result)
    assert hasattr(result, "_repr_html_")
    assert result._repr_html_() == result.str


def test_latex():
    "Output: latex with headers and replaced characters"
    raw_test_table_headers = list(_test_table_headers)
    raw_test_table_headers[-1] += " ($N_0$)"
    result = tabulate(_test_table, raw_test_table_headers, tablefmt="latex")
    expected = "\n".join(
        [
            r"\begin{tabular}{lr}",
            r"\hline",
            r" strings   &   numbers (\$N\_0\$) \\",
            r"\hline",
            r" spam      &           41.9999 \\",
            r" eggs      &          451      \\",
            r"\hline",
            r"\end{tabular}",
        ]
    )
    assert_equal(expected, result)


def test_latex_raw():
    "Output: raw latex with headers"
    raw_test_table_headers = list(_test_table_headers)
    raw_test_table_headers[-1] += " ($N_0$)"
    raw_test_table = list(map(list, _test_table))
    raw_test_table[0][0] += "$_1$"
    raw_test_table[1][0] = "\\emph{" + raw_test_table[1][0] + "}"
    print(raw_test_table)
    result = tabulate(raw_test_table, raw_test_table_headers, tablefmt="latex_raw")
    expected = "\n".join(
        [
            r"\begin{tabular}{lr}",
            r"\hline",
            r" strings     &   numbers ($N_0$) \\",
            r"\hline",
            r" spam$_1$    &           41.9999 \\",
            r" \emph{eggs} &          451      \\",
            r"\hline",
            r"\end{tabular}",
        ]
    )
    assert_equal(expected, result)


def test_latex_headerless():
    "Output: latex without headers"
    result = tabulate(_test_table, tablefmt="latex")
    expected = "\n".join(
        [
            r"\begin{tabular}{lr}",
            r"\hline",
            r" spam &  41.9999 \\",
            r" eggs & 451      \\",
            r"\hline",
            r"\end{tabular}",
        ]
    )
    assert_equal(expected, result)


def test_latex_booktabs():
    "Output: latex with headers, using the booktabs format"
    result = tabulate(_test_table, _test_table_headers, tablefmt="latex_booktabs")
    expected = "\n".join(
        [
            r"\begin{tabular}{lr}",
            r"\toprule",
            r" strings   &   numbers \\",
            r"\midrule",
            r" spam      &   41.9999 \\",
            r" eggs      &  451      \\",
            r"\bottomrule",
            r"\end{tabular}",
        ]
    )
    assert_equal(expected, result)


def test_latex_booktabs_headerless():
    "Output: latex without headers, using the booktabs format"
    result = tabulate(_test_table, tablefmt="latex_booktabs")
    expected = "\n".join(
        [
            r"\begin{tabular}{lr}",
            r"\toprule",
            r" spam &  41.9999 \\",
            r" eggs & 451      \\",
            r"\bottomrule",
            r"\end{tabular}",
        ]
    )
    assert_equal(expected, result)


def test_textile():
    "Output: textile without header"
    result = tabulate(_test_table, tablefmt="textile")
    expected = """\
|<. spam  |>.  41.9999 |
|<. eggs  |>. 451      |"""

    assert_equal(expected, result)


def test_textile_with_header():
    "Output: textile with header"
    result = tabulate(_test_table, ["strings", "numbers"], tablefmt="textile")
    expected = """\
|_.  strings   |_.   numbers |
|<. spam       |>.   41.9999 |
|<. eggs       |>.  451      |"""

    assert_equal(expected, result)


def test_textile_with_center_align():
    "Output: textile with center align"
    result = tabulate(_test_table, tablefmt="textile", stralign="center")
    expected = """\
|=. spam  |>.  41.9999 |
|=. eggs  |>. 451      |"""

    assert_equal(expected, result)


def test_no_data():
    "Output: table with no data"
    expected = "\n".join(["strings    numbers", "---------  ---------"])
    result = tabulate(None, _test_table_headers, tablefmt="simple")
    assert_equal(expected, result)


def test_empty_data():
    "Output: table with empty data"
    expected = "\n".join(["strings    numbers", "---------  ---------"])
    result = tabulate([], _test_table_headers, tablefmt="simple")
    assert_equal(expected, result)


def test_no_data_without_headers():
    "Output: table with no data and no headers"
    expected = ""
    result = tabulate(None, tablefmt="simple")
    assert_equal(expected, result)


def test_empty_data_without_headers():
    "Output: table with empty data and no headers"
    expected = ""
    result = tabulate([], tablefmt="simple")
    assert_equal(expected, result)


def test_floatfmt():
    "Output: floating point format"
    result = tabulate([["1.23456789"], [1.0]], floatfmt=".3f", tablefmt="plain")
    expected = "1.235\n1.000"
    assert_equal(expected, result)


def test_floatfmt_multi():
    "Output: floating point format different for each column"
    result = tabulate(
        [[0.12345, 0.12345, 0.12345]], floatfmt=(".1f", ".3f"), tablefmt="plain"
    )
    expected = "0.1  0.123  0.12345"
    assert_equal(expected, result)


def test_colalign_multi():
    "Output: string columns with custom colalign"
    result = tabulate(
        [["one", "two"], ["three", "four"]], colalign=("right",), tablefmt="plain"
    )
    expected = "  one  two\nthree  four"
    assert_equal(expected, result)


def test_float_conversions():
    "Output: float format parsed"
    test_headers = ["str", "bad_float", "just_float", "with_inf", "with_nan", "neg_inf"]
    test_table = [
        ["spam", 41.9999, "123.345", "12.2", "nan", "0.123123"],
        ["eggs", "451.0", 66.2222, "inf", 123.1234, "-inf"],
        ["asd", "437e6548", 1.234e2, float("inf"), float("nan"), 0.22e23],
    ]
    result = tabulate(test_table, test_headers, tablefmt="grid")
    expected = "\n".join(
        [
            "+-------+-------------+--------------+------------+------------+-------------+",
            "| str   | bad_float   |   just_float |   with_inf |   with_nan |     neg_inf |",
            "+=======+=============+==============+============+============+=============+",
            "| spam  | 41.9999     |     123.345  |       12.2 |    nan     |    0.123123 |",
            "+-------+-------------+--------------+------------+------------+-------------+",
            "| eggs  | 451.0       |      66.2222 |      inf   |    123.123 | -inf        |",
            "+-------+-------------+--------------+------------+------------+-------------+",
            "| asd   | 437e6548    |     123.4    |      inf   |    nan     |    2.2e+22  |",
            "+-------+-------------+--------------+------------+------------+-------------+",
        ]
    )
    assert_equal(expected, result)


def test_missingval():
    "Output: substitution of missing values"
    result = tabulate(
        [["Alice", 10], ["Bob", None]], missingval="n/a", tablefmt="plain"
    )
    expected = "Alice   10\nBob    n/a"
    assert_equal(expected, result)


def test_missingval_multi():
    "Output: substitution of missing values with different values per column"
    result = tabulate(
        [["Alice", "Bob", "Charlie"], [None, None, None]],
        missingval=("n/a", "?"),
        tablefmt="plain",
    )
    expected = "Alice  Bob  Charlie\nn/a    ?"
    assert_equal(expected, result)


def test_column_alignment():
    "Output: custom alignment for text and numbers"
    expected = "\n".join(["-----  ---", "Alice   1", "  Bob  333", "-----  ---"])
    result = tabulate([["Alice", 1], ["Bob", 333]], stralign="right", numalign="center")
    assert_equal(expected, result)


def test_unaligned_separated():
    "Output: non-aligned data columns"
    expected = "\n".join(["name|score", "Alice|1", "Bob|333"])
    fmt = simple_separated_format("|")
    result = tabulate(
        [["Alice", 1], ["Bob", 333]],
        ["name", "score"],
        tablefmt=fmt,
        stralign=None,
        numalign=None,
    )
    assert_equal(expected, result)


def test_pandas_with_index():
    "Output: a pandas Dataframe with an index"
    try:
        import pandas

        df = pandas.DataFrame(
            [["one", 1], ["two", None]], columns=["string", "number"], index=["a", "b"]
        )
        expected = "\n".join(
            [
                "    string      number",
                "--  --------  --------",
                "a   one              1",
                "b   two            nan",
            ]
        )
        result = tabulate(df, headers="keys")
        assert_equal(expected, result)
    except ImportError:
        skip("test_pandas_with_index is skipped")


def test_pandas_without_index():
    "Output: a pandas Dataframe without an index"
    try:
        import pandas

        df = pandas.DataFrame(
            [["one", 1], ["two", None]],
            columns=["string", "number"],
            index=pandas.Index(["a", "b"], name="index"),
        )
        expected = "\n".join(
            [
                "string      number",
                "--------  --------",
                "one              1",
                "two            nan",
            ]
        )
        result = tabulate(df, headers="keys", showindex=False)
        assert_equal(expected, result)
    except ImportError:
        skip("test_pandas_without_index is skipped")


def test_pandas_rst_with_index():
    "Output: a pandas Dataframe with an index in ReStructuredText format"
    try:
        import pandas

        df = pandas.DataFrame(
            [["one", 1], ["two", None]], columns=["string", "number"], index=["a", "b"]
        )
        expected = "\n".join(
            [
                "====  ========  ========",
                "..    string      number",
                "====  ========  ========",
                "a     one              1",
                "b     two            nan",
                "====  ========  ========",
            ]
        )
        result = tabulate(df, tablefmt="rst", headers="keys")
        assert_equal(expected, result)
    except ImportError:
        skip("test_pandas_rst_with_index is skipped")


def test_pandas_rst_with_named_index():
    "Output: a pandas Dataframe with a named index in ReStructuredText format"
    try:
        import pandas

        index = pandas.Index(["a", "b"], name="index")
        df = pandas.DataFrame(
            [["one", 1], ["two", None]], columns=["string", "number"], index=index
        )
        expected = "\n".join(
            [
                "=======  ========  ========",
                "index    string      number",
                "=======  ========  ========",
                "a        one              1",
                "b        two            nan",
                "=======  ========  ========",
            ]
        )
        result = tabulate(df, tablefmt="rst", headers="keys")
        assert_equal(expected, result)
    except ImportError:
        skip("test_pandas_rst_with_index is skipped")


def test_dict_like_with_index():
    "Output: a table with a running index"
    dd = {"b": range(101, 104)}
    expected = "\n".join(["      b", "--  ---", " 0  101", " 1  102", " 2  103"])
    result = tabulate(dd, "keys", showindex=True)
    assert_equal(result, expected)


def test_list_of_lists_with_index():
    "Output: a table with a running index"
    dd = zip(*[range(3), range(101, 104)])
    # keys' order (hence columns' order) is not deterministic in Python 3
    # => we have to consider both possible results as valid
    expected = "\n".join(
        ["      a    b", "--  ---  ---", " 0    0  101", " 1    1  102", " 2    2  103"]
    )
    result = tabulate(dd, headers=["a", "b"], showindex=True)
    assert_equal(result, expected)


def test_list_of_lists_with_supplied_index():
    "Output: a table with a supplied index"
    dd = zip(*[list(range(3)), list(range(101, 104))])
    expected = "\n".join(
        ["      a    b", "--  ---  ---", " 1    0  101", " 2    1  102", " 3    2  103"]
    )
    result = tabulate(dd, headers=["a", "b"], showindex=[1, 2, 3])
    assert_equal(result, expected)
    # TODO: make it a separate test case
    # the index must be as long as the number of rows
    with raises(ValueError):
        tabulate(dd, headers=["a", "b"], showindex=[1, 2])


def test_list_of_lists_with_index_firstrow():
    "Output: a table with a running index and header='firstrow'"
    dd = zip(*[["a"] + list(range(3)), ["b"] + list(range(101, 104))])
    expected = "\n".join(
        ["      a    b", "--  ---  ---", " 0    0  101", " 1    1  102", " 2    2  103"]
    )
    result = tabulate(dd, headers="firstrow", showindex=True)
    assert_equal(result, expected)
    # TODO: make it a separate test case
    # the index must be as long as the number of rows
    with raises(ValueError):
        tabulate(dd, headers="firstrow", showindex=[1, 2])


def test_disable_numparse_default():
    "Output: Default table output with number parsing and alignment"
    expected = "\n".join(
        [
            "strings      numbers",
            "---------  ---------",
            "spam         41.9999",
            "eggs        451",
        ]
    )
    result = tabulate(_test_table, _test_table_headers)
    assert_equal(expected, result)
    result = tabulate(_test_table, _test_table_headers, disable_numparse=False)
    assert_equal(expected, result)


def test_disable_numparse_true():
    "Output: Default table output, but without number parsing and alignment"
    expected = "\n".join(
        [
            "strings    numbers",
            "---------  ---------",
            "spam       41.9999",
            "eggs       451.0",
        ]
    )
    result = tabulate(_test_table, _test_table_headers, disable_numparse=True)
    assert_equal(expected, result)


def test_disable_numparse_list():
    "Output: Default table output, but with number parsing selectively disabled"
    table_headers = ["h1", "h2", "h3"]
    test_table = [["foo", "bar", "42992e1"]]
    expected = "\n".join(
        ["h1    h2    h3", "----  ----  -------", "foo   bar   42992e1"]
    )
    result = tabulate(test_table, table_headers, disable_numparse=[2])
    assert_equal(expected, result)

    expected = "\n".join(
        ["h1    h2        h3", "----  ----  ------", "foo   bar   429920"]
    )
    result = tabulate(test_table, table_headers, disable_numparse=[0, 1])
    assert_equal(expected, result)


def test_preserve_whitespace():
    "Output: Default table output, but with preserved leading whitespace."
    tabulate_module.PRESERVE_WHITESPACE = True
    table_headers = ["h1", "h2", "h3"]
    test_table = [["  foo", " bar   ", "foo"]]
    expected = "\n".join(
        ["h1     h2       h3", "-----  -------  ----", "  foo   bar     foo"]
    )
    result = tabulate(test_table, table_headers)
    assert_equal(expected, result)

    tabulate_module.PRESERVE_WHITESPACE = False
    table_headers = ["h1", "h2", "h3"]
    test_table = [["  foo", " bar   ", "foo"]]
    expected = "\n".join(["h1    h2    h3", "----  ----  ----", "foo   bar   foo"])
    result = tabulate(test_table, table_headers)
    assert_equal(expected, result)
