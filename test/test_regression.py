# -*- coding: utf-8 -*-

"""Regression tests."""

from __future__ import print_function
from __future__ import unicode_literals
from tabulate import tabulate, _text_type
from common import assert_equal, assert_in


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


def test_88_256_ANSI_color_codes():
    "Regression: color codes for terminals with 88/256 colors (issue #26)"
    colortable = [('\x1b[48;5;196mred\x1b[49m',
                   '\x1b[38;5;196mred\x1b[39m')]
    colorlessheaders = ('background', 'foreground')
    formatted = tabulate(colortable, colorlessheaders, 'pipe')
    expected = "\n".join([
        '| background   | foreground   |',
        '|:-------------|:-------------|',
        '| \x1b[48;5;196mred\x1b[49m          | \x1b[38;5;196mred\x1b[39m          |'])
    print("expected: %r\n\ngot:      %r\n" % (expected, formatted))
    assert_equal(expected, formatted)


def test_column_with_mixed_value_types():
    "Regression: mixed value types in the same column (issue #31)"
    expected = '\n'.join([
        '-----',
        '',
        'a',
        'я',
        '0',
        'False',
        '-----',
    ])
    data = [[None], ['a'], ['\u044f'], [0], [False]]
    table = tabulate(data)
    assert_equal(table, expected)


def test_latex_escape_special_chars():
    "Regression: escape special characters in LaTeX output (issue #32)"
    expected = "\n".join([
        r'\begin{tabular}{l}',
        r'\hline',
        r' foo\^{}bar     \\',
        r'\hline',
        r' \&\%\^{}\_\$\#\{\}\ensuremath{<}\ensuremath{>}\textasciitilde{} \\',
        r'\hline',
        r'\end{tabular}'])
    result = tabulate([["&%^_$#{}<>~"]], ["foo^bar"], tablefmt="latex")
    assert_equal(result, expected)


def test_isconvertible_on_set_values():
    "Regression: don't fail with TypeError on set values (issue #35)"
    expected_py2 = "\n".join([
        'a    b',
        '---  -------',
        'Foo  set([])',])
    expected_py3 = "\n".join([
        'a    b',
        '---  -----',
        'Foo  set()',])
    result = tabulate([["Foo",set()]], headers=["a","b"])
    assert_in(result, [expected_py2, expected_py3])


def test_ansi_color_for_decimal_numbers():
    "Regression: ANSI colors for decimal numbers (issue #36)"
    table = [["Magenta", "\033[95m" + "1.1" + "\033[0m"]]
    expected = "\n".join([
        '-------  ---',
        'Magenta  \x1b[95m1.1\x1b[0m',
        '-------  ---'])
    result = tabulate(table)
    assert_equal(result, expected)


def test_alignment_of_decimal_numbers_with_ansi_color():
    "Regression: alignment for decimal numbers with ANSI color (issue #42)"
    v1 = "\033[95m" + "12.34" + "\033[0m"
    v2 = "\033[95m" + "1.23456" + "\033[0m"
    table = [[v1], [v2]]
    expected = "\n".join([
        '\x1b[95m12.34\x1b[0m',
        ' \x1b[95m1.23456\x1b[0m'])
    result = tabulate(table, tablefmt="plain")
    assert_equal(result, expected)


def test_long_integers():
    "Regression: long integers should be printed as integers (issue #48)"
    table = [[18446744073709551614]]
    result = tabulate(table, tablefmt="plain")
    expected = "18446744073709551614"
    assert_equal(result, expected)


def test_colorclass_colors():
    "Regression: ANSI colors in a unicode/str subclass (issue #49)"
    try:
        import colorclass
        s = colorclass.Color("{magenta}3.14{/magenta}")
        result = tabulate([[s]], tablefmt="plain")
        expected = "\x1b[35m3.14\x1b[39m"
        assert_equal(result, expected)
    except ImportError:
        class textclass(_text_type):
            pass
        s = textclass("\x1b[35m3.14\x1b[39m")
        result = tabulate([[s]], tablefmt="plain")
        expected = "\x1b[35m3.14\x1b[39m"
        assert_equal(result, expected)
