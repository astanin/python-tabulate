# -*- coding: utf-8 -*-

"""Tests of the internal tabulate functions."""

from __future__ import print_function
from __future__ import unicode_literals
import tabulate as T
from common import assert_equal


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
