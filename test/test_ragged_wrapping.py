"""Column wrapping must preserve every cell in ragged tables."""

import pytest

from tabulate import tabulate


@pytest.mark.parametrize("widths", [10, [10], [10, 10], [None]])
@pytest.mark.parametrize("first_row", [["A"], []])
def test_wrapping_preserves_later_columns(widths, first_row):
    table = [first_row, ["B", "keep"]]
    assert tabulate(table, tablefmt="grid", maxcolwidths=widths) == tabulate(
        table, tablefmt="grid"
    )


def test_wrapping_applies_to_later_columns():
    table = [["A"], ["B", "abcdef"]]
    expected = "+---+-----+\n| A |     |\n+---+-----+\n| B | abc |\n|   | def |\n+---+-----+"
    assert tabulate(table, tablefmt="grid", maxcolwidths=3) == expected


def test_wrapping_ragged_rows_after_firstrow_headers():
    table = [["first", "second"], ["A"], ["B", "keep"]]
    assert tabulate(table, headers="firstrow", maxcolwidths=10) == tabulate(
        table, headers="firstrow"
    )


@pytest.mark.parametrize("table", [[], [[]], [["A", "B"], ["C", "D"]]])
def test_wrapping_uniform_and_empty_tables_unchanged(table):
    assert tabulate(table, tablefmt="grid", maxcolwidths=10) == tabulate(table, tablefmt="grid")
