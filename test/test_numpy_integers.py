"""NumPy integer values retain their precision and integer formatting."""

import pytest

from tabulate import tabulate


@pytest.mark.parametrize("input_type", ["list", "numpy", "dataframe"])
@pytest.mark.parametrize("intfmt", [",", "x"])
@pytest.mark.parametrize(
    "dtype",
    [
        "int8",
        "int16",
        "int32",
        "int64",
        "uint8",
        "uint16",
        "uint32",
        "uint64",
        "longlong",
        "ulonglong",
    ],
)
def test_numpy_integer_formats(input_type, intfmt, dtype):
    numpy = pytest.importorskip("numpy")
    integer_type = getattr(numpy, dtype)
    value = integer_type(numpy.iinfo(integer_type).max)
    rows = [[value]]
    if input_type == "numpy":
        table = numpy.array(rows, dtype=integer_type)
    elif input_type == "dataframe":
        pandas = pytest.importorskip("pandas")
        table = pandas.DataFrame(rows, dtype=integer_type)
    else:
        table = rows

    options = {"tablefmt": "plain", "showindex": False, "intfmt": intfmt, "floatfmt": ".0f"}
    assert tabulate(table, **options) == tabulate([[int(value)]], **options)


def test_numpy_duration_is_not_formatted_as_integer():
    numpy = pytest.importorskip("numpy")
    value = numpy.timedelta64(1, "D")

    assert tabulate([[value]], tablefmt="plain", intfmt="x") == str(value)
