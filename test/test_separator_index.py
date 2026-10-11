import pytest

from tabulate import SEPARATING_LINE, tabulate


@pytest.mark.parametrize("indices", [["A", "B"], ("A", "B"), iter(["A", "B"])])
def test_custom_index_skips_separator_rows(indices):
    table = [["apple"], SEPARATING_LINE, ["pear"]]
    assert tabulate(table, showindex=indices, tablefmt="plain") == "A  apple\n\nB  pear"


def test_automatic_index_skips_separator_rows():
    table = [["apple"], SEPARATING_LINE, ["pear"]]
    assert tabulate(table, showindex=True, tablefmt="plain") == "0  apple\n\n1  pear"


def test_custom_index_length_counts_only_data_rows():
    table = [["apple"], SEPARATING_LINE, ["pear"]]
    with pytest.raises(ValueError, match="len\\(rows\\)=2"):
        tabulate(table, showindex=["A"], tablefmt="plain")
