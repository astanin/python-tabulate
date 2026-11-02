"""First-row headers must respect whether the DataFrame index is shown."""

import pytest

from tabulate import tabulate


@pytest.mark.parametrize("tablefmt", ["simple", "grid", "html"])
@pytest.mark.parametrize("row_count", [0, 1, 2])
@pytest.mark.parametrize("showindex", [False, "never"])
def test_dataframe_firstrow_without_index(tablefmt, row_count, showindex):
    pandas = pytest.importorskip("pandas")
    rows = [["Name", "Age"]] + [[f"Person {i}", i] for i in range(row_count)]
    frame = pandas.DataFrame(rows, index=["row label"] + list(range(row_count)))

    assert tabulate(frame, headers="firstrow", showindex=showindex, tablefmt=tablefmt) == tabulate(
        rows, headers="firstrow", tablefmt=tablefmt
    )


@pytest.mark.parametrize("showindex", [True, "always", "default"])
def test_dataframe_firstrow_with_index(showindex):
    pandas = pytest.importorskip("pandas")
    frame = pandas.DataFrame([["Name", "Age"], ["Alice", 30]], index=["row label", "first"])

    assert tabulate(frame, headers="firstrow", showindex=showindex) == tabulate(
        [["row label", "Name", "Age"], ["first", "Alice", 30]], headers="firstrow"
    )


def test_dataframe_firstrow_numpy_false():
    numpy = pytest.importorskip("numpy")
    pandas = pytest.importorskip("pandas")
    rows = [["Name", "Age"], ["Alice", 30]]

    assert tabulate(
        pandas.DataFrame(rows), headers="firstrow", showindex=numpy.bool_(False)
    ) == tabulate(rows, headers="firstrow")
