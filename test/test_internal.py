# -*- coding: utf-8 -*-

"""Tests of the internal tabulate functions."""

from __future__ import print_function
from __future__ import unicode_literals
import tabulate as T
from common import assert_equal, assert_in, assert_raises, SkipTest


def test_align_multiline_column():
    "Internal: _align_column(..., is_multiline=True)"
    column = ["1", "123", "12345\n6"]
    output = T._align_column(column, "center", is_multiline=True)
    expected_output = ["  1  ", " 123 ", "12345" + "\n" + "  6  "]
    assert_equal(output, expected_output)
