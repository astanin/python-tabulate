"""OSC 8 hyperlinks must not affect column widths."""

from pytest import mark

import tabulate as T


@mark.parametrize("opening_end", ["\x1b\\", "\x07"])
@mark.parametrize("closing_end", ["\x1b\\", "\x07"])
@mark.parametrize("as_bytes", [False, True])
def test_strip_hyperlink_terminators(opening_end, closing_end, as_bytes):
    link = f"\x1b]8;id=docs;https://example.com/a;b{opening_end}docs\x1b]8;;{closing_end}"
    text = "before " + link + " after"
    expected = "before docs after"
    if as_bytes:
        text = text.encode()
        expected = expected.encode()
    assert T._strip_ansi(text) == expected


@mark.parametrize("opening_end", ["\x1b\\", "\x07"])
@mark.parametrize("closing_end", ["\x1b\\", "\x07"])
@mark.parametrize("wide_chars_mode", [False, True])
@mark.parametrize("as_bytes", [False, True])
def test_hyperlink_table_alignment(
    monkeypatch, opening_end, closing_end, wide_chars_mode, as_bytes
):
    monkeypatch.setattr(T, "WIDE_CHARS_MODE", wide_chars_mode)
    link = f"\x1b]8;;https://example.com{opening_end}docs\x1b]8;;{closing_end}"
    cell = link.encode() if as_bytes else link
    result = T.tabulate([[cell, "ok"]], headers=[link, "state"], tablefmt="grid")
    expected = T.tabulate([["docs", "ok"]], headers=["docs", "state"], tablefmt="grid")
    assert result.replace(link, "docs") == expected
    assert result.count(link) == 2


def test_adjacent_hyperlinks_with_different_terminators():
    first = "\x1b]8;;https://example.com/one\x07one\x1b]8;;\x07"
    second = "\x1b]8;;https://example.com/two\x1b\\two\x1b]8;;\x1b\\"
    assert T._strip_ansi(first + " " + second) == "one two"
