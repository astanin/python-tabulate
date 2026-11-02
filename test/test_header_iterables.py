"""Iterable column labels must not be interpreted as scalar header modes."""

import pytest

from tabulate import tabulate


@pytest.mark.parametrize("input_type", ["list", "numpy", "dict", "dataframe"])
@pytest.mark.parametrize(
    "labels", [["firstrow"], ["keys"], ["literal"], ["firstrow", "keys"], [], [0], [True]]
)
def test_numpy_array_column_labels(input_type, labels):
    numpy = pytest.importorskip("numpy")
    rows = [["keep first"], ["keep second"]]
    if input_type == "numpy":
        table = numpy.array(rows)
    elif input_type == "dict":
        table = {"column": [row[0] for row in rows]}
    elif input_type == "dataframe":
        pandas = pytest.importorskip("pandas")
        table = pandas.DataFrame(rows)
    else:
        table = rows
    headers = numpy.array(labels)

    assert tabulate(table, headers=headers) == tabulate(table, headers=list(headers))
