"""Footer rows share the body formatting pipeline and have a distinct boundary."""

from copy import deepcopy
from decimal import Decimal
from xml.etree import ElementTree

import pytest

from tabulate import SEPARATING_LINE, simple_separated_format, tabulate, tabulate_formats


def test_total_formats_like_body_and_expands_width():
    assert tabulate(
        [["A", 1.25], ["B", 2.5]],
        headers=["Item", "Cost"],
        footer=["Total", 3.75],
        floatfmt=".2f",
    ) == "\n".join(
        [
            "Item      Cost",
            "------  ------",
            "A         1.25",
            "B         2.50",
            "------  ------",
            "Total     3.75",
        ]
    )


def test_footer_can_widen_the_numeric_column_and_infer_float():
    assert tabulate(
        [[1]], footer=[Decimal("123456789.125")], floatfmt=".3f", tablefmt="plain"
    ) == ("        1.000\n\n123456789.125")


@pytest.mark.parametrize(
    "showindex", [True, "always", ["first", "second"], iter(["first", "second"])]
)
def test_footer_does_not_consume_an_index(showindex):
    result = tabulate(
        [["A", 1], ["B", 2]],
        headers=["item", "n"],
        footer=["Total", 3],
        showindex=showindex,
        tablefmt="tsv",
    )
    assert result.splitlines()[-1].split("\t")[0].strip() == ""
    assert result.splitlines()[-1].split("\t")[1].strip() == "Total"
    assert result.count("Total") == 1


def test_firstrow_headers_do_not_come_from_footer():
    assert tabulate(
        [["name", "value"], ["A", 1.0]], headers="firstrow", footer=["Total", 1.0]
    ) == ("name      value\n------  -------\nA             1\n------  -------\nTotal         1")


def test_dictionary_columns_and_mapped_headers():
    result = tabulate(
        [{"name": "A", "value": 1.25}],
        headers={"name": "Item", "value": "Cost"},
        footer=["Total", 1.25],
        floatfmt=".2f",
    )
    assert result.splitlines()[-1] == "Total     1.25"
    assert result.splitlines()[0] == "Item      Cost"


def test_generators_are_consumed_once_and_inputs_are_not_mutated():
    rows = [["A", 1.25], ["B", 2.5]]
    footer = ["Total", 3.75]
    original = deepcopy((rows, footer))
    result = tabulate((row for row in rows), footer=(value for value in footer), tablefmt="grid")
    assert (rows, footer) == original
    assert result.count("Total") == 1


@pytest.mark.parametrize("tablefmt", tabulate_formats)
def test_footer_none_preserves_output(tablefmt):
    rows = [["A", 1.25], ["B", 2.5]]
    assert tabulate(rows, headers=["item", "cost"], tablefmt=tablefmt, footer=None) == tabulate(
        rows,
        headers=["item", "cost"],
        tablefmt=tablefmt,
    )


@pytest.mark.parametrize("tablefmt", tabulate_formats)
def test_footer_available_in_every_builtin_format(tablefmt):
    result = tabulate(
        [["A", 1.5]],
        headers=["Item", "Cost"],
        footer=["TOTAL", 1.5],
        floatfmt=".2f",
        tablefmt=tablefmt,
    )
    assert result.count("TOTAL") == 1
    assert "1.50" in result or tablefmt == "pretty"
    assert SEPARATING_LINE not in result


@pytest.mark.parametrize("rows, headers", [([], ()), (None, ()), ([], ["item", "cost"])])
def test_footer_only(rows, headers):
    result = tabulate(
        rows, headers=headers, footer=["Total", 0.0], tablefmt="grid", floatfmt=".2f"
    )
    assert "| Total" in result and "0.00 |" in result
    assert result.count("Total") == 1


def test_footer_only_with_index():
    assert (
        tabulate([], headers=["item", "n"], footer=["Total", 0], showindex=True, tablefmt="tsv")
        .splitlines()[-1]
        .split("\t")[0]
        .strip()
        == ""
    )


def test_footer_precision_missing_values_and_int_format():
    result = tabulate(
        [["A", 1000, Decimal("1.0000000000000001"), None]],
        footer=["Total", 1000, Decimal("1.0000000000000001"), None],
        floatfmt=".16f",
        intfmt=",d",
        missingval="?",
        tablefmt="plain",
    )
    assert result.splitlines()[-1] == "Total  1,000  1.0000000000000001  ?"


def test_numeric_strings_are_not_parsed_when_disabled():
    result = tabulate(
        [["A", "01.20"]],
        footer=["Total", "01.20"],
        disable_numparse=True,
        floatfmt=".1f",
        tablefmt="plain",
    )
    assert result.splitlines()[-1] == "Total  01.20"


def test_multiline_footer_and_vertical_alignment():
    result = tabulate(
        [["A", 1.0]],
        footer=["Grand\nTotal", 1.0],
        tablefmt="grid",
        floatfmt=".2f",
        rowalign=["top", "bottom"],
    )
    assert result.splitlines()[-3:] == [
        "| Grand |      |",
        "| Total | 1.00 |",
        "+-------+------+",
    ]


def test_footer_wraps_using_body_width_configuration():
    result = tabulate(
        [["A", 1]], footer=["Grand Total", 1], tablefmt="grid", maxcolwidths=[5, None]
    )
    assert result.splitlines()[-3:] == [
        "| Grand | 1 |",
        "| Total |   |",
        "+-------+---+",
    ]


def test_ansi_footer_uses_visible_width():
    options = {"headers": ["Item", "Cost"], "tablefmt": "grid", "floatfmt": ".1f"}
    result = tabulate([["A", 1.5]], footer=["\x1b[31mTotal\x1b[0m", 1.5], **options)
    assert result.replace("\x1b[31m", "").replace("\x1b[0m", "") == tabulate(
        [["A", 1.5]],
        footer=["Total", 1.5],
        **options,
    )


@pytest.mark.parametrize("tablefmt", ["simple", "grid"])
def test_existing_separators_do_not_consume_rows_or_duplicate_footer_rule(tablefmt):
    rows = [["A", 1], SEPARATING_LINE, ["B", 2], ["C", 3], SEPARATING_LINE]
    result = tabulate(rows, footer=["Total", 6], tablefmt=tablefmt)
    assert all(label in result for label in ["A", "B", "C", "Total"])
    lines = result.splitlines()
    footer_at = next(i for i, line in enumerate(lines) if "Total" in line)
    assert "C" in lines[footer_at - 2]


@pytest.mark.parametrize("tablefmt", ["html", "unsafehtml"])
def test_html_footer_is_a_separate_section_inside_one_table(tablefmt):
    result = tabulate(
        [["A", 1.5]],
        headers=["Item", "Cost"],
        footer=["Total", 1.5],
        tablefmt=tablefmt,
        floatfmt=".2f",
    )
    table = ElementTree.fromstring(result)
    assert [child.tag for child in table] == ["thead", "tbody", "tfoot"]
    assert [cell.text.strip() for cell in table.findall("./tfoot/tr/td")] == ["Total", "1.50"]
    assert len(table.findall("./tbody/tr")) == 1
    assert hasattr(result, "_repr_html_")


def test_longtable_does_not_repeat_endhead_before_footer():
    result = tabulate(
        [["A", 1]], headers=["Item", "n"], footer=["Total", 1], tablefmt="latex_longtable"
    )
    assert result.count("\\endhead") == 1
    assert result.count("\\end{longtable}") == 1
    assert "Total" in result.split("\\endhead")[1].split("\\end{longtable}")[0]


def test_custom_ruleless_format():
    assert tabulate([["A", 1]], footer=["Total", 1], tablefmt=simple_separated_format(";")) == (
        "A    ;1\n\nTotal;1"
    )


@pytest.mark.parametrize("footer", [[], ["one"], [1, 2, 3], SEPARATING_LINE, "total", {"a": 1}])
def test_invalid_footer_is_rejected(footer):
    with pytest.raises((ValueError, TypeError), match="footer"):
        tabulate([["A", 1]], footer=footer)


def test_pandas_index_is_blank_in_footer_including_empty_frame():
    pd = pytest.importorskip("pandas")
    for frame in [
        pd.DataFrame({"cost": [1.5]}, index=pd.Index(["a"], name="id")),
        pd.DataFrame({"cost": []}, index=pd.Index([], name="id")),
    ]:
        result = tabulate(frame, headers="keys", footer=[1.5], floatfmt=".2f", tablefmt="tsv")
        assert [cell.strip() for cell in result.splitlines()[-1].split("\t")] == ["", "1.50"]


def test_ragged_body_is_padded_before_wrapping_footer():
    result = tabulate(
        [["A"], ["B", 1]], footer=["Grand Total", 1], maxcolwidths=[5, None], tablefmt="grid"
    )
    assert "| Grand | 1 |" in result
    assert "| Total |   |" in result
