"""Tests for code paths executed when the wcwidth library is not available.

These tests mock wcwidth as None to cover branches that would otherwise only
run in environments without wcwidth installed.
"""

from unittest.mock import patch

import tabulate as T
from tabulate import tabulate

from common import assert_equal


def _patch_no_wcwidth():
    """Return a context manager that simulates wcwidth being unavailable."""
    return (
        patch.object(T, "wcwidth", None),
        patch.object(T, "WIDE_CHARS_MODE", False),
    )


# ---------------------------------------------------------------------------
# _visible_width() fallback paths
# ---------------------------------------------------------------------------


def test_visible_width_str_no_wcwidth():
    "Internal: _visible_width() falls back to len() for str when wcwidth is None"
    with patch.object(T, "wcwidth", None), patch.object(T, "WIDE_CHARS_MODE", False):
        assert T._visible_width("hello") == 5
        # ANSI codes must still be stripped
        assert T._visible_width("\x1b[31mhello\x1b[0m") == 5
        # Wide chars are counted as 1 each (no wcwidth)
        assert T._visible_width("配列") == 2


def test_visible_width_bytes_no_wcwidth():
    "Internal: _visible_width() falls back to len() for bytes when wcwidth is None"
    with patch.object(T, "wcwidth", None), patch.object(T, "WIDE_CHARS_MODE", False):
        assert T._visible_width(b"hello") == 5


def test_visible_width_non_string_no_wcwidth():
    "Internal: _visible_width() falls back to len(str(...)) for non-strings when wcwidth is None"
    with patch.object(T, "wcwidth", None), patch.object(T, "WIDE_CHARS_MODE", False):
        assert T._visible_width(12345) == 5
        assert T._visible_width(3.14) == 4


# ---------------------------------------------------------------------------
# _choose_width_fn() and _align_column_choose_width_fn() fallback paths
# ---------------------------------------------------------------------------


def test_choose_width_fn_no_wcwidth_no_invisible():
    "Internal: _choose_width_fn() returns len when wcwidth is None and no invisible chars"
    with patch.object(T, "wcwidth", None), patch.object(T, "WIDE_CHARS_MODE", False):
        fn = T._choose_width_fn(has_invisible=False, enable_widechars=False, is_multiline=False)
        assert fn is len


def test_choose_width_fn_no_wcwidth_multiline():
    "Internal: _choose_width_fn() wraps len in multiline handler when wcwidth is None"
    with patch.object(T, "wcwidth", None), patch.object(T, "WIDE_CHARS_MODE", False):
        fn = T._choose_width_fn(has_invisible=False, enable_widechars=False, is_multiline=True)
        # The result is a lambda, not len directly, but it should compute max line length
        assert fn("foo\nbarbaz") == 6


def test_align_column_choose_width_fn_no_wcwidth():
    "Internal: _align_column_choose_width_fn() returns len when wcwidth is None"
    with patch.object(T, "wcwidth", None), patch.object(T, "WIDE_CHARS_MODE", False):
        fn = T._align_column_choose_width_fn(
            has_invisible=False, enable_widechars=False, is_multiline=False
        )
        assert fn is len


def test_align_column_choose_width_fn_no_wcwidth_multiline():
    "Internal: _align_column_choose_width_fn() returns per-line widths list for multiline when wcwidth is None"
    with patch.object(T, "wcwidth", None), patch.object(T, "WIDE_CHARS_MODE", False):
        fn = T._align_column_choose_width_fn(
            has_invisible=False, enable_widechars=False, is_multiline=True
        )
        # _align_column_multiline_width returns a list of widths per line
        assert fn("foo\nbarbaz") == [3, 6]


# ---------------------------------------------------------------------------
# _CustomTextWrap._len() fallback path
# ---------------------------------------------------------------------------


def test_textwrapper_len_no_wcwidth():
    "Internal: _CustomTextWrap._len() falls back to len() when wcwidth is None"
    with patch.object(T, "wcwidth", None), patch.object(T, "WIDE_CHARS_MODE", False):
        assert T._CustomTextWrap._len("hello") == 5
        assert T._CustomTextWrap._len("\x1b[31mhello\x1b[0m") == 5


# ---------------------------------------------------------------------------
# End-to-end tabulate() with wide characters, no wcwidth
# ---------------------------------------------------------------------------


def test_tabulate_wide_chars_no_wcwidth_grid():
    "Output: grid with wide characters treats them as width-1 when wcwidth is None"
    with patch.object(T, "wcwidth", None), patch.object(T, "WIDE_CHARS_MODE", False):
        table = [["spam", 41.9999], ["eggs", "451.0"]]
        headers = ["strings", "配列"]
        result = tabulate(table, headers, tablefmt="grid")
        # With no wcwidth, "配列" is treated as 2 chars wide (not 4),
        # so column width matches len("配列") == 2, padded to fit content.
        # We only assert the result is a non-empty string and doesn't crash;
        # the exact layout depends on len()-based widths.
        assert len(result) > 0
        assert "配列" in result
        assert "spam" in result
        expected = "\n".join(
            [
                "+-----------+----------+",
                "| strings   |       配列 |",
                "+===========+==========+",
                "| spam      |  41.9999 |",
                "+-----------+----------+",
                "| eggs      | 451      |",
                "+-----------+----------+",
            ]
        )
        assert_equal(expected.splitlines(), result.splitlines())


def test_tabulate_wide_chars_no_wcwidth_plain():
    "Output: plain with wide characters uses len() when wcwidth is None"
    with patch.object(T, "wcwidth", None), patch.object(T, "WIDE_CHARS_MODE", False):
        table = [["привет", 1], ["你好", 2]]
        result = tabulate(table, tablefmt="plain")
        assert "привет" in result
        assert "你好" in result


def test_tabulate_wide_chars_no_wcwidth_simple_grid():
    "Output: simple_grid with wide characters uses len() when wcwidth is None"
    with patch.object(T, "wcwidth", None), patch.object(T, "WIDE_CHARS_MODE", False):
        table = [["가나", "abc"], ["de", "fgh"]]
        result = tabulate(table, tablefmt="simple_grid")
        assert "가나" in result
        assert len(result) > 0


# ---------------------------------------------------------------------------
# maxcolwidths path through CustomTextWrapper when wcwidth is None
# ---------------------------------------------------------------------------


def test_maxcolwidths_no_wcwidth():
    "Output: maxcolwidths autowrap uses len() when wcwidth is None"
    with patch.object(T, "wcwidth", None), patch.object(T, "WIDE_CHARS_MODE", False):
        table = [["hdr", "fold"], ["1", "very long data"]]
        expected = "\n".join(["  hdr  fold", "    1  very long", "       data"])
        result = tabulate(table, headers="firstrow", tablefmt="plain", maxcolwidths=[10, 10])
        assert_equal(expected, result)


def test_maxcolwidths_wide_chars_no_wcwidth():
    "Output: maxcolwidths with wide chars wraps by byte-len when wcwidth is None"
    with patch.object(T, "wcwidth", None), patch.object(T, "WIDE_CHARS_MODE", False):
        table = [["hdr", "fold"], ["1", "약간 감싸면 더 잘 보일 수있는 긴 설명"]]
        result = tabulate(table, headers="firstrow", tablefmt="plain", maxcolwidths=[10, 10])
        assert "hdr" in result
        assert len(result) > 0
