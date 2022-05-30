# -*- coding: utf-8 -*-

"""Tests of the internal tabulate functions."""

from __future__ import print_function
from __future__ import unicode_literals
import tabulate as T
from common import assert_equal, skip


def test_multiline_width():
    "Internal: _multiline_width()"
    multiline_string = "\n".join(["foo", "barbaz", "spam"])
    assert_equal(T._multiline_width(multiline_string), 6)
    oneline_string = "12345"
    assert_equal(T._multiline_width(oneline_string), len(oneline_string))


def test_align_column_decimal():
    "Internal: _align_column(..., 'decimal')"
    column = ["12.345", "-1234.5", "1.23", "1234.5", "1e+234", "1.0e234"]
    output = T._align_column(column, "decimal")
    expected = [
        "   12.345  ",
        "-1234.5    ",
        "    1.23   ",
        " 1234.5    ",
        "    1e+234 ",
        "    1.0e234",
    ]
    assert_equal(output, expected)


def test_align_column_decimal_with_thousand_separators():
    "Internal: _align_column(..., 'decimal')"
    column = ["12.345", "-1234.5", "1.23", "1,234.5", "1e+234", "1.0e234"]
    output = T._align_column(column, "decimal")
    expected = [
        "   12.345  ",
        "-1234.5    ",
        "    1.23   ",
        "1,234.5    ",
        "    1e+234 ",
        "    1.0e234",
    ]
    assert_equal(output, expected)


def test_align_column_decimal_with_incorrect_thousand_separators():
    "Internal: _align_column(..., 'decimal')"
    column = ["12.345", "-1234.5", "1.23", "12,34.5", "1e+234", "1.0e234"]
    output = T._align_column(column, "decimal")
    expected = [
        "     12.345  ",
        "  -1234.5    ",
        "      1.23   ",
        "12,34.5      ",
        "      1e+234 ",
        "      1.0e234",
    ]
    assert_equal(output, expected)


def test_align_column_none():
    "Internal: _align_column(..., None)"
    column = ["123.4", "56.7890"]
    output = T._align_column(column, None)
    expected = ["123.4", "56.7890"]
    assert_equal(output, expected)


def test_align_column_multiline():
    "Internal: _align_column(..., is_multiline=True)"
    column = ["1", "123", "12345\n6"]
    output = T._align_column(column, "center", is_multiline=True)
    expected = ["  1  ", " 123 ", "12345" + "\n" + "  6  "]
    assert_equal(output, expected)


def test_wrap_text_to_colwidths():
    "Internal: Test _wrap_text_to_colwidths to show it will wrap text based on colwidths"
    rows = [
        ["mini", "medium", "decently long", "wrap will be ignored"],
        [
            "small",
            "JustOneWordThatIsWayTooLong",
            "this is unreasonably long for a single cell length",
            "also ignored here",
        ],
    ]
    widths = [10, 10, 20, None]
    expected = [
        ["mini", "medium", "decently long", "wrap will be ignored"],
        [
            "small",
            "JustOneWor\ndThatIsWay\nTooLong",
            "this is unreasonably\nlong for a single\ncell length",
            "also ignored here",
        ],
    ]
    result = T._wrap_text_to_colwidths(rows, widths)

    assert_equal(result, expected)


def test_wrap_text_wide_chars():
    "Internal: Wrap wide characters based on column width"
    try:
        import wcwidth  # noqa
    except ImportError:
        skip("test_wrap_text_wide_chars is skipped")

    rows = [["청자청자청자청자청자", "약간 감싸면 더 잘 보일 수있는 다소 긴 설명입니다"]]
    widths = [5, 20]
    expected = [["청자\n청자\n청자\n청자\n청자", "약간 감싸면 더 잘\n보일 수있는 다소 긴\n설명입니다"]]
    result = T._wrap_text_to_colwidths(rows, widths)

    assert_equal(result, expected)


def test_wrap_text_to_numbers():
    """Internal: Test _wrap_text_to_colwidths force ignores numbers by
    default so as not to break alignment behaviors"""
    rows = [
        ["first number", 123.456789, "123.456789"],
        ["second number", "987654.123", "987654.123"],
    ]
    widths = [6, 6, 6]
    expected = [
        ["first\nnumber", 123.456789, "123.45\n6789"],
        ["second\nnumber", "987654.123", "987654\n.123"],
    ]

    result = T._wrap_text_to_colwidths(rows, widths, numparses=[True, True, False])
    assert_equal(result, expected)


def test_wrap_text_to_colwidths_single_ansi_colors_full_cell():
    """Internal: autowrapped text can retain a single ANSI colors
    when it is at the beginning and end of full cell"""
    data = [
        [
            (
                "\033[31mThis is a rather long description that might"
                " look better if it is wrapped a bit\033[0m"
            )
        ]
    ]
    result = T._wrap_text_to_colwidths(data, [30])

    expected = [
        [
            "\n".join(
                [
                    "\033[31mThis is a rather long\033[0m",
                    "\033[31mdescription that might look\033[0m",
                    "\033[31mbetter if it is wrapped a bit\033[0m",
                ]
            )
        ]
    ]
    assert_equal(expected, result)


def test_wrap_text_to_colwidths_colors_wide_char():
    """Internal: autowrapped text can retain a ANSI colors with wide chars"""
    try:
        import wcwidth  # noqa
    except ImportError:
        skip("test_wrap_text_to_colwidths_colors_wide_char is skipped")

    data = [[("\033[31m약간 감싸면 더 잘 보일 수있는 다소 긴" " 설명입니다 설명입니다 설명입니다 설명입니다 설명\033[0m")]]
    result = T._wrap_text_to_colwidths(data, [30])

    expected = [
        [
            "\n".join(
                [
                    "\033[31m약간 감싸면 더 잘 보일 수있는\033[0m",
                    "\033[31m다소 긴 설명입니다 설명입니다\033[0m",
                    "\033[31m설명입니다 설명입니다 설명\033[0m",
                ]
            )
        ]
    ]
    assert_equal(expected, result)


def test_wrap_text_to_colwidths_multi_ansi_colors_full_cell():
    """Internal: autowrapped text can retain multiple ANSI colors
    when they are at the beginning and end of full cell
    (e.g. text and background colors)"""
    data = [
        [
            (
                "\033[31m\033[43mThis is a rather long description that"
                " might look better if it is wrapped a bit\033[0m"
            )
        ]
    ]
    result = T._wrap_text_to_colwidths(data, [30])

    expected = [
        [
            "\n".join(
                [
                    "\033[31m\033[43mThis is a rather long\033[0m",
                    "\033[31m\033[43mdescription that might look\033[0m",
                    "\033[31m\033[43mbetter if it is wrapped a bit\033[0m",
                ]
            )
        ]
    ]
    assert_equal(expected, result)


def test_wrap_text_to_colwidths_multi_ansi_colors_in_subset():
    """Internal: autowrapped text can retain multiple ANSI colors
    when they are around subsets of the cell"""
    data = [
        [
            (
                "This is a rather \033[31mlong description\033[0m that"
                " might look better \033[93mif it is wrapped\033[0m a bit"
            )
        ]
    ]
    result = T._wrap_text_to_colwidths(data, [30])

    expected = [
        [
            "\n".join(
                [
                    "This is a rather \033[31mlong\033[0m",
                    "\033[31mdescription\033[0m that might look",
                    "better \033[93mif it is wrapped\033[0m a bit",
                ]
            )
        ]
    ]
    assert_equal(expected, result)
