"""Custom numeric formatting through the public table API."""

from decimal import Decimal
import math

import pytest

import tabulate as tabulate_module
from tabulate import SEPARATING_LINE, tabulate


def test_engineering_notation_is_not_reparsed():
    assert (
        tabulate(
            [[Decimal("1E-7")], [Decimal("1E6")]],
            floatfmt=Decimal.to_eng_string,
            tablefmt="plain",
            numalign=None,
        )
        == "100E-9\n1E+6"
    )


def test_per_column_callable_and_format_strings():
    assert (
        tabulate(
            [[1.25, 2.75, 3.5]],
            floatfmt=(lambda value: f"<{value}>", ".1f"),
            tablefmt="plain",
        )
        == "<1.25>  2.8  3.5"
    )


def test_decimal_keeps_precision_and_identity():
    value = Decimal("99999998999.9999800000001")
    seen = []

    def formatter(number):
        seen.append(number)
        return str(number)

    assert tabulate([[value]], floatfmt=formatter, tablefmt="plain") == str(value)
    assert seen == [value]
    assert seen[0] is value


def test_type_inference_and_missing_cells():
    seen = []

    def formatter(number):
        seen.append(number)
        return f"{number:.1f}"

    result = tabulate(
        [["text", 1, 2.5], ["more", 2, None], ["last", 3, ""]],
        floatfmt=formatter,
        missingval="?",
        tablefmt="plain",
    )
    assert result == "text  1  2.5\nmore  2  ?\nlast  3"
    assert seen == [2.5]


def test_disable_numparse_does_not_format_numeric_strings():
    seen = []
    assert (
        tabulate(
            [["2.50", 1.5]],
            floatfmt=lambda value: seen.append(value) or "formatted",
            disable_numparse=[0],
            tablefmt="plain",
        )
        == "2.50  formatted"
    )
    assert seen == [1.5]


@pytest.mark.parametrize("value", [1.25, "1.25", b"1.25", "1,000.25"])
def test_callback_gets_parsed_float(value):
    seen = []
    tabulate([[value]], floatfmt=lambda number: seen.append(number) or "number")
    assert seen == [1000.25 if value == "1,000.25" else 1.25]
    assert type(seen[0]) is float


def test_callable_object():
    class Formatter:
        def __call__(self, number):
            return f"{number * 100:.0f}%"

    assert tabulate([[0.125]], floatfmt=Formatter(), tablefmt="plain") == "12%"


def test_nonfinite_values_and_negative_zero():
    seen = []
    tabulate(
        [[math.inf], [-math.inf], [math.nan], [-0.0]], floatfmt=lambda x: seen.append(x) or str(x)
    )
    assert seen[:2] == [math.inf, -math.inf]
    assert math.isnan(seen[2])
    assert math.copysign(1, seen[3]) == -1


@pytest.mark.parametrize("error_type", [ValueError, TypeError, RuntimeError])
def test_callback_exception_propagates(error_type):
    error = error_type("custom formatting failed")

    def formatter(number):
        raise error

    with pytest.raises(error_type) as caught:
        tabulate([[1.5]], floatfmt=formatter)
    assert caught.value is error


@pytest.mark.parametrize("result", [None, 3, b"1.50"])
def test_callback_must_return_string(result):
    with pytest.raises(TypeError, match="floatfmt callable must return a string"):
        tabulate([[1.5]], floatfmt=lambda value: result)


@pytest.mark.parametrize("value", ["\x1b[31m1.25\x1b[0m", b"\x1b[31m1.25\x1b[0m"])
def test_colored_numeric_input(value):
    assert tabulate([[value]], floatfmt=lambda number: f"{number:.1f}", tablefmt="plain") == (
        "\x1b[31m1.2\x1b[0m"
    )


@pytest.mark.parametrize("widechars", [False, True])
def test_output_colors_do_not_change_column_width(widechars, monkeypatch):
    monkeypatch.setattr(tabulate_module, "WIDE_CHARS_MODE", widechars)
    data = [[1.25], [20.5]]
    plain = tabulate(data, headers=["value"], tablefmt="grid", floatfmt=".2f")
    colored = tabulate(
        data,
        headers=["value"],
        tablefmt="grid",
        floatfmt=lambda value: f"\x1b[31m{value:.2f}\x1b[0m",
    )
    assert colored.replace("\x1b[31m", "").replace("\x1b[0m", "") == plain


@pytest.mark.parametrize("tablefmt", ["grid", "simple", "plain"])
def test_callback_can_introduce_multiline_cells(tablefmt):
    options = {"headers": ["value"], "tablefmt": tablefmt, "colalign": ("right",)}
    assert tabulate(
        [[1.5], [12.0]], floatfmt=lambda value: f"{value:.1f}\nunits", **options
    ) == tabulate([["1.5\nunits"], ["12.0\nunits"]], disable_numparse=True, **options)


def test_missing_blank_and_separator_rows_do_not_call_formatter():
    seen = []
    result = tabulate(
        [[1.5], [None], [""], SEPARATING_LINE, [2.5]],
        floatfmt=lambda value: seen.append(value) or f"{value:.1f}",
        tablefmt="simple",
        missingval="?",
        numalign=None,
    )
    assert seen == [1.5, 2.5]
    assert "?" in result and "2.5" in result


def test_empty_table_with_callable():
    assert tabulate([], floatfmt=lambda value: pytest.fail("empty table")) == ""
