"""Discretely test functionality of our custom TextWrapper"""

import datetime
from textwrap import TextWrapper as OTW

from tabulate import _CustomTextWrap as CTW, _strip_ansi, tabulate

from common import assert_equal, skip


def test_wrap_multiword_non_wide():
    """TextWrapper: non-wide character regression tests"""
    data = "this is a test string for regression splitting"
    for width in range(1, len(data)):
        orig = OTW(width=width)
        cust = CTW(width=width)

        assert [line.rstrip() for line in orig.wrap(data)] == [
            line.rstrip() for line in cust.wrap(data)
        ], f"Failure on non-wide char multiword regression check for width {width}"


def test_wrap_multiword_non_wide_with_hypens():
    """TextWrapper: non-wide character regression tests that contain hyphens"""
    data = "how should-we-split-this non-sense string that-has-lots-of-hypens"
    for width in range(1, len(data)):
        orig = OTW(width=width)
        cust = CTW(width=width)

        assert [line.rstrip() for line in orig.wrap(data)] == [
            line.rstrip() for line in cust.wrap(data)
        ], f"Failure on non-wide char hyphen regression check for width {width}"


def test_wrap_longword_non_wide():
    """TextWrapper: Some non-wide character regression tests"""
    data = "ThisIsASingleReallyLongWordThatWeNeedToSplit"
    for width in range(1, len(data)):
        orig = OTW(width=width)
        cust = CTW(width=width)

        assert orig.wrap(data) == cust.wrap(data), (
            f"Failure on non-wide char longword regression check for width {width}"
        )


def test_wrap_wide_char_multiword():
    """TextWrapper: wrapping support for wide characters with multiple words"""
    try:
        import wcwidth  # noqa: F401
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
        import wcwidth  # noqa: F401
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
    data = "\033[31m\033[104mThis is a test string for testing TextWrap with colors\033[0m"

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


def test_wrap_color_line_longword_zerowidth():
    """Lines with zero-width symbols (accents) must include those symbols with the prior symbol.
    Let's exercise the calculation where the available symbols never satisfy the available width,
    and ensure chunk calculation succeeds and ANSI colors are maintained.

    Most combining marks combine with the preceding character (even in right-to-left alphabets):
      - "e\u0301" → "é" (e + combining acute accent)
      - "a\u0308" → "ä" (a + combining diaeresis)
      - "n\u0303" → "ñ" (n + combining tilde)
    Enclosing Marks: Some combining marks enclose the base character:
      - "A\u20dd" → Ⓐ  Combining enclosing circle
    Multiple Combining Marks: You can stack multiple combining marks on a single base character:
      - "e\u0301\u0308" → e with both acute accent and diaeresis
    Zero width space → "ab" with a :
      - "a\u200bb"

    """
    try:
        import wcwidth  # noqa
    except ImportError:
        skip("test_wrap_wide_char is skipped")

    # Exactly filled, with a green zero-width segment at the end.
    data = (
        "This_is_A\u20dd_\033[31mte\u0301st_string_\u200b"
        "to_te\u0301\u0308st_a\u0308ccent\033[32m\u200b\033[0m"
    )

    expected = [
        "This_is_A\u20dd_\033[31mte\u0301\033[0m",
        "\033[31mst_string_\u200bto\033[0m",
        "\033[31m_te\u0301\u0308st_a\u0308ccent\033[32m\u200b\033[0m",
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


def test_wrap_none_value():
    """TextWrapper: Show that None can be wrapped without crashing"""
    data = [["First Entry", None], ["Second Entry", None]]
    headers = ["Title", "Value"]
    result = tabulate(data, headers=headers, tablefmt="grid", maxcolwidths=[7, 5])

    expected = [
        "+---------+---------+",
        "| Title   | Value   |",
        "+=========+=========+",
        "| First   |         |",
        "| Entry   |         |",
        "+---------+---------+",
        "| Second  |         |",
        "| Entry   |         |",
        "+---------+---------+",
    ]
    expected = "\n".join(expected)
    assert_equal(expected, result)


def test_wrap_none_value_with_missingval():
    """TextWrapper: Show that None can be wrapped without crashing and with a missing value"""
    data = [["First Entry", None], ["Second Entry", None]]
    headers = ["Title", "Value"]
    result = tabulate(
        data, headers=headers, tablefmt="grid", maxcolwidths=[7, 5], missingval="???"
    )

    expected = [
        "+---------+---------+",
        "| Title   | Value   |",
        "+=========+=========+",
        "| First   | ???     |",
        "| Entry   |         |",
        "+---------+---------+",
        "| Second  | ???     |",
        "| Entry   |         |",
        "+---------+---------+",
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
        "| Second  |        |",
        "| Entry   |        |",
        "+---------+--------+",
    ]
    expected = "\n".join(expected)
    assert_equal(expected, result)


def test_wrap_wide_char_no_column_overflow():
    "TextWrapper: wide chars must not overflow the requested column width."
    try:
        import wcwidth
    except ImportError:
        skip("test_wrap_wide_char_no_column_overflow is skipped")

    # Each Korean character occupies 2 display columns.
    data = "\ud55c\uae00\ud14c\uc2a4\ud2b8"  # 한글테스트
    for width in [2, 3, 4, 5, 6]:
        wrapper = CTW(width=width)
        lines = wrapper.wrap(data)
        for line in lines:
            display_width = wcwidth.wcswidth(line)
            assert display_width <= width, (
                f"Line {line!r} has display width {display_width} "
                f"which exceeds requested column width {width}"
            )


def test_wrap_max_lines_placeholder_on_current_line():
    """TextWrapper: max_lines truncation appends placeholder to current line after
    popping trailing words that don't leave room for it (while-loop A.inner branch)"""
    # Line 2 has "four five six" but "six" gets popped, then "five [...]" fits in 15
    wrapper = CTW(width=15, max_lines=2)
    result = wrapper.wrap("one two three four five six seven eight")
    assert_equal(["one two three", "four five [...]"], result)


def test_wrap_max_lines_placeholder_appended_to_previous_line():
    """TextWrapper: max_lines truncation appends placeholder to the previous line
    when the current line is entirely too long (while-loop else, B.1.a branch)"""
    # "toolong" alone overflows with placeholder, but prev line "ab" has room for " [...]"
    wrapper = CTW(width=8, max_lines=2)
    result = wrapper.wrap("ab toolong extra")
    assert_equal(["ab [...]"], result)


def test_wrap_max_lines_placeholder_alone_no_previous_lines():
    """TextWrapper: max_lines=1 with an unbreakable word emits placeholder alone
    when there are no previous lines (while-loop else, B.2 branch)"""
    wrapper = CTW(width=5, max_lines=1, break_long_words=False)
    result = wrapper.wrap("toolong extra")
    assert_equal(["[...]"], result)


def test_wrap_max_lines_placeholder_alone_previous_line_too_full():
    """TextWrapper: max_lines truncation emits placeholder as a new line when
    the previous line has no room for it either (while-loop else, B.1.b branch)"""
    # prev line "hello"(5) + " [...]"(6) = 11 > width(5), so placeholder becomes its own line
    wrapper = CTW(width=5, max_lines=2, break_long_words=False)
    result = wrapper.wrap("hello toolong extra")
    assert_equal(["hello", "[...]"], result)


def test_wrap_wide_char_narrower_than_char_width():
    """TextWrapper: column width smaller than a single wide char must not hang (issue #399).

    When the requested width is 1 but every character is 2 display columns
    wide, _handle_long_word must still make progress (one character per line)
    rather than looping forever.
    """
    try:
        import wcwidth  # noqa: F401
    except ImportError:
        skip("test_wrap_wide_char_narrower_than_char_width is skipped")

    data = "\ud55c\uae00"  # 한글 -- each char is 2 display cols wide
    # width=1 is narrower than any character; each char should still get its own line
    result = CTW(width=1).wrap(data)
    assert result == ["\ud55c", "\uae00"]
