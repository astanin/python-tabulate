"""Tests for Unicode grapheme cluster handling in tabulate."""

import pytest

from tabulate import tabulate

try:
    import wcwidth

    HAS_WCWIDTH = True
    HAS_WCWIDTH_030 = hasattr(wcwidth, "wrap")
except ImportError:
    wcwidth = None
    HAS_WCWIDTH = False
    HAS_WCWIDTH_030 = False

requires_wcwidth = pytest.mark.skipif(not HAS_WCWIDTH, reason="requires wcwidth")

requires_wcwidth_030 = pytest.mark.skipif(
    not HAS_WCWIDTH_030, reason="requires wcwidth >= 0.3.0"
)


class TestGraphemeClusterWidth:
    """Tests for correct width calculation of grapheme clusters."""

    @requires_wcwidth
    def test_zwj_family_emoji_width(self):
        """ZWJ family emoji has display width 2."""
        family = "\U0001f468\u200d\U0001f469\u200d\U0001f467"
        assert wcwidth.wcswidth(family) == 2

    @requires_wcwidth
    def test_regional_indicator_flag_width(self):
        """Regional indicator pair (flag) has display width 2."""
        us_flag = "\U0001f1fa\U0001f1f8"
        assert wcwidth.wcswidth(us_flag) == 2

    @requires_wcwidth
    def test_vs16_emoji_width(self):
        """VS16 variation selector creates wide emoji."""
        heart = "\u2764\ufe0f"
        assert wcwidth.wcswidth(heart) == 2


class TestGraphemeClusterAlignment:
    """Tests for correct alignment of cells containing grapheme clusters."""

    @requires_wcwidth
    def test_zwj_alignment_in_grid(self):
        """ZWJ emoji aligns correctly in grid format."""
        family = "\U0001f468\u200d\U0001f469\u200d\U0001f467"
        data = [
            ["ABC", "text"],
            [family, "emoji"],
        ]
        result = tabulate(data, headers=["col", "desc"], tablefmt="grid")
        lines = result.split("\n")

        border_width = len(lines[0])
        for line in lines:
            from tabulate import _visible_width

            assert _visible_width(line) == border_width

    @requires_wcwidth
    def test_flag_alignment_in_grid(self):
        """Regional indicator flags align correctly in grid format."""
        us_flag = "\U0001f1fa\U0001f1f8"
        data = [
            ["AB", "text"],
            [us_flag, "flag"],
        ]
        result = tabulate(data, headers=["col", "desc"], tablefmt="grid")
        lines = result.split("\n")

        border_width = len(lines[0])
        for line in lines:
            from tabulate import _visible_width

            assert _visible_width(line) == border_width


class TestGraphemeClusterWrapping:
    """Tests for grapheme cluster preservation during text wrapping.

    These tests require wcwidth >= 0.3.0 for iter_graphemes and wrap() APIs.
    """

    @requires_wcwidth_030
    def test_zwj_not_broken_during_wrap(self):
        """ZWJ sequence preserved as single unit during wrap."""
        family = "\U0001f468\u200d\U0001f469\u200d\U0001f467"
        data = [[f"A{family}B"]]
        result = tabulate(data, tablefmt="plain", maxcolwidths=3)

        graphemes_in_result = []
        for line in result.split("\n"):
            graphemes_in_result.extend(list(wcwidth.iter_graphemes(line.strip())))

        assert family in graphemes_in_result

    @requires_wcwidth_030
    def test_flag_not_broken_during_wrap(self):
        """Regional indicator flag preserved as single unit during wrap."""
        us_flag = "\U0001f1fa\U0001f1f8"
        gb_flag = "\U0001f1ec\U0001f1e7"
        fr_flag = "\U0001f1eb\U0001f1f7"
        flags = us_flag + gb_flag + fr_flag

        data = [[flags]]
        result = tabulate(data, tablefmt="plain", maxcolwidths=5)

        graphemes_in_result = []
        for line in result.split("\n"):
            graphemes_in_result.extend(list(wcwidth.iter_graphemes(line.strip())))

        assert us_flag in graphemes_in_result
        assert gb_flag in graphemes_in_result
        assert fr_flag in graphemes_in_result

    @requires_wcwidth_030
    def test_vs16_not_broken_during_wrap(self):
        """VS16 variation selector kept with base character during wrap."""
        heart = "\u2764\ufe0f"
        data = [[heart * 3]]
        result = tabulate(data, tablefmt="plain", maxcolwidths=4)

        graphemes_in_result = []
        for line in result.split("\n"):
            graphemes_in_result.extend(list(wcwidth.iter_graphemes(line.strip())))

        heart_count = sum(1 for g in graphemes_in_result if g == heart)
        assert heart_count == 3

    @requires_wcwidth_030
    def test_skin_tone_modifier_not_broken(self):
        """Skin tone modifier preserved with emoji during wrap."""
        wave_light = "\U0001f44b\U0001f3fb"
        data = [[f"Hi{wave_light}there"]]
        result = tabulate(data, tablefmt="plain", maxcolwidths=5)

        graphemes_in_result = []
        for line in result.split("\n"):
            graphemes_in_result.extend(list(wcwidth.iter_graphemes(line.strip())))

        assert wave_light in graphemes_in_result


class TestComplexGraphemeClusters:
    """Tests for complex grapheme cluster scenarios.

    These tests require wcwidth >= 0.3.0 for iter_graphemes API.
    """

    @requires_wcwidth_030
    def test_multiple_zwj_sequences_in_cell(self):
        """Multiple ZWJ sequences in single cell handled correctly."""
        family = "\U0001f468\u200d\U0001f469\u200d\U0001f467"
        technologist = "\U0001f468\U0001f3fb\u200d\U0001f4bb"
        data = [[f"{family} and {technologist}"]]
        result = tabulate(data, tablefmt="plain", maxcolwidths=15)

        graphemes_in_result = []
        for line in result.split("\n"):
            graphemes_in_result.extend(list(wcwidth.iter_graphemes(line.strip())))

        assert family in graphemes_in_result
        assert technologist in graphemes_in_result

    @requires_wcwidth_030
    def test_flags_with_text_wrap(self):
        """Flags interspersed with text wrap correctly."""
        us_flag = "\U0001f1fa\U0001f1f8"
        data = [[f"Visit {us_flag} USA today!"]]
        result = tabulate(data, tablefmt="plain", maxcolwidths=10)

        graphemes_in_result = []
        for line in result.split("\n"):
            graphemes_in_result.extend(list(wcwidth.iter_graphemes(line.strip())))

        assert us_flag in graphemes_in_result

    @requires_wcwidth_030
    def test_combining_marks_preserved(self):
        """Combining diacritical marks stay with base character."""
        e_acute = "e\u0301"
        data = [[f"caf{e_acute} au lait"]]
        result = tabulate(data, tablefmt="plain", maxcolwidths=5)

        graphemes_in_result = []
        for line in result.split("\n"):
            graphemes_in_result.extend(list(wcwidth.iter_graphemes(line.strip())))

        assert e_acute in graphemes_in_result


class TestAnsiWithGraphemeClusters:
    """Tests for ANSI escape codes combined with grapheme clusters."""

    @requires_wcwidth
    def test_ansi_colored_zwj_width(self):
        """ANSI colored ZWJ emoji has correct width."""
        family = "\U0001f468\u200d\U0001f469\u200d\U0001f467"
        colored = f"\x1b[31m{family}\x1b[0m"

        from tabulate import _visible_width

        assert _visible_width(colored) == 2

    @requires_wcwidth
    def test_ansi_colored_zwj_alignment(self):
        """ANSI colored ZWJ emoji aligns correctly."""
        family = "\U0001f468\u200d\U0001f469\u200d\U0001f467"
        colored = f"\x1b[31m{family}\x1b[0m"
        data = [
            ["AB", "text"],
            [colored, "emoji"],
        ]
        result = tabulate(data, headers=["col", "desc"], tablefmt="grid")
        lines = result.split("\n")

        from tabulate import _visible_width

        border_width = _visible_width(lines[0])
        for line in lines:
            assert _visible_width(line) == border_width

    @requires_wcwidth_030
    def test_ansi_colored_flag_wrap(self):
        """ANSI colored flag not broken during wrap."""
        us_flag = "\U0001f1fa\U0001f1f8"
        colored = f"\x1b[34m{us_flag}\x1b[0m"
        data = [[f"A{colored}B"]]
        result = tabulate(data, tablefmt="plain", maxcolwidths=4)

        assert "\U0001f1fa" in result
        assert "\U0001f1f8" in result
        lines = [line.strip() for line in result.split("\n") if line.strip()]
        flag_parts_same_line = any(
            "\U0001f1fa" in line and "\U0001f1f8" in line for line in lines
        )
        assert flag_parts_same_line
