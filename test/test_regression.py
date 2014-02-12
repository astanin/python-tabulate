# -*- coding: utf-8 -*-

"""Regression tests."""

from __future__ import print_function
from __future__ import unicode_literals
from tabulate import tabulate
from common import assert_equal


def test_ansi_color_in_table_cells():
    "Regression: ANSI color in table cells (issue #5)."
    colortable = [('test', '\x1b[31mtest\x1b[0m', '\x1b[32mtest\x1b[0m')]
    colorlessheaders = ('test', 'test', 'test')
    formatted = tabulate(colortable, colorlessheaders, 'pipe')
    expected = "\n".join(['| test   | test   | test   |',
                          '|:-------|:-------|:-------|',
                          '| test   | \x1b[31mtest\x1b[0m   | \x1b[32mtest\x1b[0m   |'])
    print("expected: %r\n\ngot:      %r\n" % (expected, formatted))
    assert_equal(expected, formatted)


def test_alignment_of_colored_cells():
    "Regression: Align ANSI-colored values as if they were colorless."
    colortable = [('test', 42, '\x1b[31m42\x1b[0m'), ('test', 101, '\x1b[32m101\x1b[0m')]
    colorheaders = ('test', '\x1b[34mtest\x1b[0m', 'test')
    formatted = tabulate(colortable, colorheaders, 'grid')
    expected = '\n'.join(['+--------+--------+--------+',
                          '| test   |   \x1b[34mtest\x1b[0m |   test |',
                          '+========+========+========+',
                          '| test   |     42 |     \x1b[31m42\x1b[0m |',
                          '+--------+--------+--------+',
                          '| test   |    101 |    \x1b[32m101\x1b[0m |',
                          '+--------+--------+--------+'])
    print("expected: %r\n\ngot:      %r\n" % (expected, formatted))
    assert_equal(expected, formatted)


def test_iter_of_iters_with_headers():
    "Regression: Generator of generators with a generator of headers (issue #9)."

    def mk_iter_of_iters():
        def mk_iter():
            for i in range(3):
                yield i
        for r in range(3):
            yield mk_iter()

    def mk_headers():
        for h in ["a", "b", "c"]:
            yield h

    formatted = tabulate(mk_iter_of_iters(), headers=mk_headers())
    expected = '\n'.join(['  a    b    c',
                          '---  ---  ---',
                          '  0    1    2',
                          '  0    1    2',
                          '  0    1    2'])
    print("expected: %r\n\ngot:      %r\n" % (expected, formatted))
    assert_equal(expected, formatted)


def test_datetime_values():
    "Regression: datetime, date, and time values in cells (issue #10)."
    import datetime
    dt = datetime.datetime(1991,2,19,17,35,26)
    d = datetime.date(1991,2,19)
    t = datetime.time(17,35,26)
    formatted = tabulate([[dt, d, t]])
    expected = '\n'.join(['-------------------  ----------  --------',
                          '1991-02-19 17:35:26  1991-02-19  17:35:26',
                          '-------------------  ----------  --------'])
    print("expected: %r\n\ngot:      %r\n" % (expected, formatted))
    assert_equal(expected, formatted)


def test_simple_separated_format():
    "Regression: simple_separated_format() accepts any separator (issue #12)"
    from tabulate import simple_separated_format
    fmt = simple_separated_format("!")
    expected = 'spam!eggs'
    formatted = tabulate([["spam", "eggs"]], tablefmt=fmt)
    print("expected: %r\n\ngot:      %r\n" % (expected, formatted))
    assert_equal(expected, formatted)


def py3test_require_py3():
    "Regression: py33 tests should actually use Python 3 (issue #13)"
    from platform import python_version_tuple
    print("Expected Python version: 3.x.x")
    print("Python version used for tests: %s.%s.%s" % python_version_tuple())
    assert_equal(python_version_tuple()[0], '3')


def test_simple_separated_format_with_headers():
    "Regression: simple_separated_format() on tables with headers (issue #15)"
    from tabulate import simple_separated_format
    expected = '  a|  b\n  1|  2'
    formatted = tabulate([[1,2]], headers=["a", "b"], tablefmt=simple_separated_format("|"))
    assert_equal(expected, formatted)


def test_column_type_of_bytestring_columns():
    "Regression: column type for columns of bytestrings (issue #16)"
    from tabulate import _column_type, _binary_type
    result = _column_type([b"foo", b"bar"])
    expected = _binary_type
    assert_equal(result, expected)


def test_numeric_column_headers():
    "Regression: numbers as column headers (issue #22)"
    result = tabulate([[1],[2]], [42])
    expected = '  42\n----\n   1\n   2'
    assert_equal(result, expected)

    lod = [dict((p,i) for p in range(5)) for i in range(5)]
    result = tabulate(lod, "keys")
    expected = "\n".join([
        "  0    1    2    3    4",
        "---  ---  ---  ---  ---",
        "  0    0    0    0    0",
        "  1    1    1    1    1",
        "  2    2    2    2    2",
        "  3    3    3    3    3",
        "  4    4    4    4    4",])
    assert_equal(result, expected)
