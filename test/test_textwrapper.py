"""Discretely test functionality of our custom TextWrapper"""

import datetime
from unittest.mock import patch, MagicMock

import pytest

from tabulate import _CustomTextWrap as CTW, _wrap_text, tabulate, _strip_ansi
from textwrap import TextWrapper as OTW

from common import assert_equal

try:
    import wcwidth

    HAS_WCWIDTH = True
    HAS_WCWIDTH_WRAP = hasattr(wcwidth, "wrap")
except ImportError:
    wcwidth = None
    HAS_WCWIDTH = False
    HAS_WCWIDTH_WRAP = False

requires_wcwidth = pytest.mark.skipif(not HAS_WCWIDTH, reason="requires wcwidth")


@pytest.fixture(params=["wcwidth_wrap", "custom_textwrap"])
def wrap_backend(request):
    """Fixture to test both wrap backends: wcwidth.wrap and _CustomTextWrap fallback."""
    # This ensures both code paths in _wrap_text() are tested:
    #  def _wrap_text(text, width, ...):
    #      if wcwidth is not None and hasattr(wcwidth, "wrap"):
    #          # Path 1: wcwidth.wrap (tested by wcwidth_wrap)
    #          return _propagate_ansi_codes(wcwidth.wrap(...))
    #      else:
    #          # Path 2: fallback (tested by custom_textwrap)
    #          return _CustomTextWrap(...).wrap(text)
    #
    # Tests using this fixture verify both backends produce identical results.
    if request.param == "wcwidth_wrap":
        if not HAS_WCWIDTH_WRAP:
            pytest.skip("wcwidth.wrap not available")
        yield "wcwidth_wrap"
    else:
        # Mock wcwidth to not have wrap attribute, forcing _CustomTextWrap fallback
        if not HAS_WCWIDTH:
            pytest.skip("wcwidth not available")
        mock_wcwidth = MagicMock(spec=["wcswidth", "wcwidth"])
        mock_wcwidth.wcswidth = wcwidth.wcswidth
        mock_wcwidth.wcwidth = wcwidth.wcwidth
        with patch("tabulate.wcwidth", mock_wcwidth):
            yield "custom_textwrap"


def _nwrap(lines):
    """Normalize wrapped lines for cross-version comparison.

    https://github.com/python/cpython/issues/140627
    """
    return [line.rstrip() for line in lines]


def test_wrap_multiword_non_wide():
    """TextWrapper: non-wide character regression tests"""
    data = "this is a test string for regression splitting"
    for width in range(1, len(data)):
        orig = OTW(width=width)
        cust = CTW(width=width)

        assert _nwrap(orig.wrap(data)) == _nwrap(
            cust.wrap(data)
        ), "Failure on non-wide char multiword regression check for width " + str(width)


def test_wrap_multiword_non_wide_with_hypens():
    """TextWrapper: non-wide character regression tests that contain hyphens"""
    data = "how should-we-split-this non-sense string that-has-lots-of-hypens"
    for width in range(1, len(data)):
        orig = OTW(width=width)
        cust = CTW(width=width)

        assert _nwrap(orig.wrap(data)) == _nwrap(
            cust.wrap(data)
        ), "Failure on non-wide char hyphen regression check for width " + str(width)


def test_wrap_longword_non_wide():
    """TextWrapper: Some non-wide character regression tests"""
    data = "ThisIsASingleReallyLongWordThatWeNeedToSplit"
    for width in range(1, len(data)):
        orig = OTW(width=width)
        cust = CTW(width=width)

        assert _nwrap(orig.wrap(data)) == _nwrap(
            cust.wrap(data)
        ), "Failure on non-wide char longword regression check for width " + str(width)


@requires_wcwidth
def test_wrap_wide_char_multiword(wrap_backend):
    """TextWrapper: wrapping support for wide characters with multiple words"""
    data = "약간 감싸면 더 잘 보일 수있는 다소 긴 설명입니다"

    expected = ["약간 감싸면 더", "잘 보일 수있는", "다소 긴", "설명입니다"]

    result = _wrap_text(data, width=15)
    assert result == expected


@requires_wcwidth
def test_wrap_wide_char_longword(wrap_backend):
    """TextWrapper: wrapping wide char word that needs to be broken up"""
    data = "약간감싸면더잘보일수있"

    expected = ["약간", "감싸", "면더", "잘보", "일수", "있"]

    # Explicit odd number to ensure the 2 width is taken into account
    result = _wrap_text(data, width=5)
    assert result == expected


@requires_wcwidth
def test_wrap_mixed_string(wrap_backend):
    """TextWrapper: wrapping string with mix of wide and non-wide chars"""
    data = (
        "This content of this string (この文字列のこの内容) contains "
        "multiple character types (複数の文字タイプが含まれています)"
    )

    expected = [
        "This content of this",
        "string (この文字列の",
        "この内容) contains",
        "multiple character",
        "types (複数の文字タイ",
        "プが含まれています)",
    ]
    result = _wrap_text(data, width=21)
    assert result == expected


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
    propagate them to other lines when they don't need to be"""
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
    other lines when required, requires adding the colors tags to other lines as appropriate
    """
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


def test_wrap_color_line_longword():
    """TextWrapper: Wrap a line - preserve internal color tags and wrap them to
    other lines when required, requires adding the colors tags to other lines as appropriate
    and avoiding splitting escape codes."""
    data = "This_is_a_\033[31mtest_string_for_testing_TextWrap\033[0m_with_colors"

    expected = [
        "This_is_a_\033[31mte\033[0m",
        "\033[31mst_string_fo\033[0m",
        "\033[31mr_testing_Te\033[0m",
        "\033[31mxtWrap\033[0m_with_",
        "colors",
    ]
    wrapper = CTW(width=12)
    result = wrapper.wrap(data)
    assert_equal(expected, result)


def test_wrap_color_line_multiple_escapes():
    data = "012345(\x1b[32ma\x1b[0mbc\x1b[32mdefghij\x1b[0m)"
    expected = [
        "012345(\x1b[32ma\x1b[0mbc\x1b[32m\x1b[0m",
        "\x1b[32mdefghij\x1b[0m)",
    ]
    wrapper = CTW(width=10)
    result = wrapper.wrap(data)
    assert_equal(expected, result)

    clean_data = _strip_ansi(data)
    for width in range(2, len(clean_data)):
        wrapper = CTW(width=width)
        result = wrapper.wrap(data)
        # Comparing after stripping ANSI should be enough to catch broken escape codes
        assert_equal(clean_data, _strip_ansi("".join(result)))


def test_wrap_datetime():
    """TextWrapper: Show that datetimes can be wrapped without crashing"""
    data = [
        ["First Entry", datetime.datetime(2020, 1, 1, 5, 6, 7)],
        ["Second Entry", datetime.datetime(2021, 2, 2, 0, 0, 0)],
    ]
    headers = ["Title", "When"]
    result = tabulate(data, headers=headers, tablefmt="grid", maxcolwidths=[7, 5])

    expected = [
        "+---------+--------+",
        "| Title   | When   |",
        "+=========+========+",
        "| First   | 2020-  |",
        "| Entry   | 01-01  |",
        "|         | 05:06  |",
        "|         | :07    |",
        "+---------+--------+",
        "| Second  | 2021-  |",
        "| Entry   | 02-02  |",
        "|         | 00:00  |",
        "|         | :00    |",
        "+---------+--------+",
    ]
    expected = "\n".join(expected)
    assert_equal(expected, result)


def test_wrap_optional_bool_strs():
    """TextWrapper: Show that str bools and None can be wrapped without crashing"""
    data = [
        ["First Entry", "True"],
        ["Second Entry", None],
    ]
    headers = ["Title", "When"]
    result = tabulate(data, headers=headers, tablefmt="grid", maxcolwidths=[7, 5])

    expected = [
        "+---------+--------+",
        "| Title   | When   |",
        "+=========+========+",
        "| First   | True   |",
        "| Entry   |        |",
        "+---------+--------+",
        "| Second  | None   |",
        "| Entry   |        |",
        "+---------+--------+",
    ]
    expected = "\n".join(expected)
    assert_equal(expected, result)
