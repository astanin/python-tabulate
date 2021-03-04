# -*- coding: utf-8 -*-

"""Discretely test functionality of our custom TextWrapper"""
from __future__ import unicode_literals

from tabulate import _CustomTextWrap as CTW
from textwrap import TextWrapper as OTW

from common import skip, assert_equal


def test_wrap_multiword_non_wide():
    """TextWrapper: non-wide character regression tests"""
    data = "this is a test string for regression spiltting"
    for width in range(1, len(data)):
        orig = OTW(width=width)
        cust = CTW(width=width)

        assert orig.wrap(data) == cust.wrap(
            data
        ), "Failure on non-wide char multiword regression check for width " + str(width)


def test_wrap_multiword_non_wide_with_hypens():
    """TextWrapper: non-wide character regression tests that contain hypens"""
    data = "how should-we-split-this non-sense string that-has-lots-of-hypens"
    for width in range(1, len(data)):
        orig = OTW(width=width)
        cust = CTW(width=width)

        assert orig.wrap(data) == cust.wrap(
            data
        ), "Failure on non-wide char hyphen regression check for width " + str(width)


def test_wrap_longword_non_wide():
    """TextWrapper: Some non-wide character regression tests"""
    data = "ThisIsASingleReallyLongWordThatWeNeedToSplit"
    for width in range(1, len(data)):
        orig = OTW(width=width)
        cust = CTW(width=width)

        assert orig.wrap(data) == cust.wrap(
            data
        ), "Failure on non-wide char longword regression check for width " + str(width)


def test_wrap_wide_char_multiword():
    """TextWrapper: wrapping support for wide characters with mulitple words"""
    try:
        import wcwidth  # noqa
    except ImportError:
        skip("test_wrap_wide_char is skipped")

    data = "약간 감싸면 더 잘 보일 수있는 다소 긴 설명입니다"

    expected = ["약간 감싸면 더", "잘 보일 수있는", "다소 긴", "설명입니다"]

    wrapper = CTW(width=15)
    result = wrapper.wrap(data)
    assert_equal(expected, result)


def test_wrap_wide_char_longword():
    """TextWrapper: wrapping wide char word that needs to be broken up"""
    try:
        import wcwidth  # noqa
    except ImportError:
        skip("test_wrap_wide_char_longword is skipped")

    data = "약간감싸면더잘보일수있"

    expected = ["약간", "감싸", "면더", "잘보", "일수", "있"]

    # Explicit odd number to ensure the 2 width is taken into account
    wrapper = CTW(width=5)
    result = wrapper.wrap(data)
    assert_equal(expected, result)


def test_wrap_mixed_string():
    """TextWrapper: wrapping string with mix of wide and non-wide chars"""
    try:
        import wcwidth  # noqa
    except ImportError:
        skip("test_wrap_wide_char is skipped")

    data = (
        "This content of this string (この文字列のこの内容) contains "
        "mulitple character types (複数の文字タイプが含まれています)"
    )

    expected = [
        "This content of this",
        "string (この文字列の",
        "この内容) contains",
        "mulitple character",
        "types (複数の文字タイ",
        "プが含まれています)",
    ]
    wrapper = CTW(width=21)
    result = wrapper.wrap(data)
    assert_equal(expected, result)


def test_wrapper_len_ignores_color_chars():
    data = "\033[31m\033[104mtenletters\033[0m"
    result = CTW._len(data)
    assert_equal(10, result)


def test_wrap_full_line_color():
    """TextWrapper: Wrap a line when the full thing is enclosed in color tags"""
    # This has both a text color and a background color
    data = (
        "\033[31m\033[104mThis is a test string for testing TextWrap with colors\033[0m"
    )

    expected = [
        "\033[31m\033[104mThis is a test\033[0m",
        "\033[31m\033[104mstring for testing\033[0m",
        "\033[31m\033[104mTextWrap with colors\033[0m",
    ]
    wrapper = CTW(width=20)
    result = wrapper.wrap(data)
    assert_equal(expected, result)


def test_wrap_color_in_single_line():
    """TextWrapper: Wrap a line - preserve internal color tags, and don't
    propogate them to other lines when they don't need to be"""
    # This has both a text color and a background color
    data = "This is a test string for testing \033[31mTextWrap\033[0m with colors"

    expected = [
        "This is a test string for",
        "testing \033[31mTextWrap\033[0m with",
        "colors",
    ]
    wrapper = CTW(width=25)
    result = wrapper.wrap(data)
    assert_equal(expected, result)


def test_wrap_color_line_splillover():
    """TextWrapper: Wrap a line - preserve internal color tags and wrap them to
    other lines when required, requires adding the colors tags to other lines as appropriate"""
    # This has both a text color and a background color
    data = "This is a \033[31mtest string for testing TextWrap\033[0m with colors"

    expected = [
        "This is a \033[31mtest string for\033[0m",
        "\033[31mtesting TextWrap\033[0m with",
        "colors",
    ]
    wrapper = CTW(width=25)
    result = wrapper.wrap(data)
    assert_equal(expected, result)
