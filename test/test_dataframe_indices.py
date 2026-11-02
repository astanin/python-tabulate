"""DataFrame row-index options must not compare array-like values as scalars."""

import pytest

from tabulate import tabulate


@pytest.mark.parametrize("index_type", ["array", "Index", "Series"])
@pytest.mark.parametrize("index_name", [None, "original"])
@pytest.mark.parametrize("row_ids", [[], [10, 20], [1], ["default"], ["always"], [True]])
def test_dataframe_array_like_row_indices(index_type, index_name, row_ids):
    numpy = pytest.importorskip("numpy")
    pandas = pytest.importorskip("pandas")
    frame = pandas.DataFrame({"value": range(len(row_ids))})
    frame.index.name = index_name
    factory = numpy.array if index_type == "array" else getattr(pandas, index_type)
    indices = factory(row_ids)

    expected = tabulate(frame, headers="keys", showindex=list(indices))
    actual = tabulate(frame, headers="keys", showindex=indices)

    assert actual == expected
    assert "original" not in actual


def test_dataframe_sequence_row_indices():
    pandas = pytest.importorskip("pandas")
    frame = pandas.DataFrame({"value": [1, 2]})
    frame.index.name = "original"

    class RowIndices:
        def __len__(self):
            return 2

        def __getitem__(self, index):
            return [10, 20][index]

        def __eq__(self, other):
            raise AssertionError("Custom row indices must not be compared to scalar modes")

    assert tabulate(frame, headers="keys", showindex=RowIndices()) == tabulate(
        frame, headers="keys", showindex=[10, 20]
    )


@pytest.mark.parametrize("showindex", ["default", "always", True, "never", False])
def test_dataframe_scalar_row_index_options(showindex):
    pandas = pytest.importorskip("pandas")
    frame = pandas.DataFrame({"value": [1, 2]})
    frame.index.name = "original"

    actual = tabulate(frame, headers="keys", showindex=showindex)

    assert ("original" in actual) == (showindex in ["default", "always", True])


def test_dataframe_numpy_boolean_row_index_options():
    numpy = pytest.importorskip("numpy")
    pandas = pytest.importorskip("pandas")
    frame = pandas.DataFrame({"value": [1, 2]})
    frame.index.name = "original"

    for showindex in (True, False):
        assert tabulate(frame, headers="keys", showindex=numpy.bool_(showindex)) == tabulate(
            frame, headers="keys", showindex=showindex
        )
