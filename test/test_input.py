"""Test support of the various forms of tabular data."""

from tabulate import SEPARATING_LINE, tabulate

from common import assert_equal, assert_in, pytest, raises, skip

try:
    from collections import UserDict
except ImportError:
    # Python2
    from UserDict import UserDict


def test_iterable_of_iterables():
    "Input: an iterable of iterables."
    ii = iter(map(iter, [range(5), range(5, 0, -1)]))
    expected = "\n".join(["-  -  -  -  -", "0  1  2  3  4", "5  4  3  2  1", "-  -  -  -  -"])
    result = tabulate(ii)
    assert_equal(expected, result)


def test_iterable_of_iterables_headers():
    "Input: an iterable of iterables with headers."
    ii = iter(map(iter, [range(5), range(5, 0, -1)]))
    expected = "\n".join(
        [
            "  a    b    c    d    e",
            "---  ---  ---  ---  ---",
            "  0    1    2    3    4",
            "  5    4    3    2    1",
        ]
    )
    result = tabulate(ii, "abcde")
    assert_equal(expected, result)


def test_iterable_of_iterables_firstrow():
    "Input: an iterable of iterables with the first row as headers"
    ii = iter(map(iter, ["abcde", range(5), range(5, 0, -1)]))
    expected = "\n".join(
        [
            "  a    b    c    d    e",
            "---  ---  ---  ---  ---",
            "  0    1    2    3    4",
            "  5    4    3    2    1",
        ]
    )
    result = tabulate(ii, "firstrow")
    assert_equal(expected, result)


def test_list_of_lists():
    "Input: a list of lists with headers."
    ll = [["a", "one", 1], ["b", "two", None]]
    expected = "\n".join(
        [
            "    string      number",
            "--  --------  --------",
            "a   one              1",
            "b   two",
        ]
    )
    result = tabulate(ll, headers=["string", "number"])
    assert_equal(expected, result)


def test_list_of_lists_firstrow():
    "Input: a list of lists with the first row as headers."
    ll = [["string", "number"], ["a", "one", 1], ["b", "two", None]]
    expected = "\n".join(
        [
            "    string      number",
            "--  --------  --------",
            "a   one              1",
            "b   two",
        ]
    )
    result = tabulate(ll, headers="firstrow")
    assert_equal(expected, result)


def test_list_of_lists_keys():
    "Input: a list of lists with column indices as headers."
    ll = [["a", "one", 1], ["b", "two", None]]
    expected = "\n".join(["0    1      2", "---  ---  ---", "a    one    1", "b    two"])
    result = tabulate(ll, headers="keys")
    assert_equal(expected, result)


def test_dict_like():
    "Input: a dict of iterables with keys as headers."
    # columns should be padded with None, keys should be used as headers
    dd = {"a": range(3), "b": range(101, 105)}
    # keys' order (hence columns' order) is not deterministic in Python 3
    # => we have to consider both possible results as valid
    expected1 = "\n".join(["  a    b", "---  ---", "  0  101", "  1  102", "  2  103", "     104"])
    expected2 = "\n".join(["  b    a", "---  ---", "101    0", "102    1", "103    2", "104"])
    result = tabulate(dd, "keys")
    print(f"Keys' order: {dd.keys()}")
    assert_in(result, [expected1, expected2])


def test_numpy_2d():
    "Input: a 2D NumPy array with headers."
    try:
        import numpy

        na = (numpy.arange(1, 10, dtype=numpy.float32).reshape((3, 3)) ** 3) * 0.5
        expected = "\n".join(
            [
                "    a      b      c",
                "-----  -----  -----",
                "  0.5    4     13.5",
                " 32     62.5  108",
                "171.5  256    364.5",
            ]
        )
        result = tabulate(na, ["a", "b", "c"])
        assert_equal(expected, result)
    except ImportError:
        skip("test_numpy_2d is skipped")


def test_numpy_2d_firstrow():
    "Input: a 2D NumPy array with the first row as headers."
    try:
        import numpy

        na = numpy.arange(1, 10, dtype=numpy.int32).reshape((3, 3)) ** 3
        expected = "\n".join(
            ["  1    8    27", "---  ---  ----", " 64  125   216", "343  512   729"]
        )
        result = tabulate(na, headers="firstrow")
        assert_equal(expected, result)
    except ImportError:
        skip("test_numpy_2d_firstrow is skipped")


def test_numpy_2d_keys():
    "Input: a 2D NumPy array with column indices as headers."
    try:
        import numpy

        na = (numpy.arange(1, 10, dtype=numpy.float32).reshape((3, 3)) ** 3) * 0.5
        expected = "\n".join(
            [
                "    0      1      2",
                "-----  -----  -----",
                "  0.5    4     13.5",
                " 32     62.5  108",
                "171.5  256    364.5",
            ]
        )
        result = tabulate(na, headers="keys")
        assert_equal(expected, result)
    except ImportError:
        skip("test_numpy_2d_keys is skipped")


def test_numpy_record_array():
    "Input: a 2D NumPy record array without header."
    try:
        import numpy

        na = numpy.asarray(
            [("Alice", 23, 169.5), ("Bob", 27, 175.0)],
            dtype={
                "names": ["name", "age", "height"],
                "formats": ["S32", "uint8", "float32"],
            },
        )
        expected = "\n".join(
            [
                "-----  --  -----",
                "Alice  23  169.5",
                "Bob    27  175",
                "-----  --  -----",
            ]
        )
        result = tabulate(na)
        assert_equal(expected, result)
    except ImportError:
        skip("test_numpy_2d_keys is skipped")


def test_numpy_record_array_keys():
    "Input: a 2D NumPy record array with column names as headers."
    try:
        import numpy

        na = numpy.asarray(
            [("Alice", 23, 169.5), ("Bob", 27, 175.0)],
            dtype={
                "names": ["name", "age", "height"],
                "formats": ["S32", "uint8", "float32"],
            },
        )
        expected = "\n".join(
            [
                "name      age    height",
                "------  -----  --------",
                "Alice      23     169.5",
                "Bob        27     175",
            ]
        )
        result = tabulate(na, headers="keys")
        assert_equal(expected, result)
    except ImportError:
        skip("test_numpy_2d_keys is skipped")


def test_numpy_record_array_headers():
    "Input: a 2D NumPy record array with user-supplied headers."
    try:
        import numpy

        na = numpy.asarray(
            [("Alice", 23, 169.5), ("Bob", 27, 175.0)],
            dtype={
                "names": ["name", "age", "height"],
                "formats": ["S32", "uint8", "float32"],
            },
        )
        expected = "\n".join(
            [
                "person      years     cm",
                "--------  -------  -----",
                "Alice          23  169.5",
                "Bob            27  175",
            ]
        )
        result = tabulate(na, headers=["person", "years", "cm"])
        assert_equal(expected, result)
    except ImportError:
        skip("test_numpy_2d_keys is skipped")


def test_pandas():
    "Input: a Pandas DataFrame."
    try:
        import pandas

        df = pandas.DataFrame([["one", 1], ["two", None]], index=["a", "b"])
        expected = "\n".join(
            [
                "    string      number",
                "--  --------  --------",
                "a   one              1",
                "b   two            nan",
            ]
        )
        result = tabulate(df, headers=["string", "number"])
        assert_equal(expected, result)
    except ImportError:
        skip("test_pandas is skipped")


def test_pandas_firstrow():
    "Input: a Pandas DataFrame with the first row as headers."
    try:
        import pandas

        df = pandas.DataFrame(
            [["one", 1], ["two", None]], columns=["string", "number"], index=["a", "b"]
        )
        expected = "\n".join(["a    one      1.0", "---  -----  -----", "b    two      nan"])
        result = tabulate(df, headers="firstrow")
        assert_equal(expected, result)
    except ImportError:
        skip("test_pandas_firstrow is skipped")


def test_pandas_keys():
    "Input: a Pandas DataFrame with keys as headers."
    try:
        import pandas

        df = pandas.DataFrame(
            [["one", 1], ["two", None]], columns=["string", "number"], index=["a", "b"]
        )
        expected = "\n".join(
            [
                "    string      number",
                "--  --------  --------",
                "a   one              1",
                "b   two            nan",
            ]
        )
        result = tabulate(df, headers="keys")
        assert_equal(expected, result)
    except ImportError:
        skip("test_pandas_keys is skipped")


@pytest.mark.parametrize("integer", [123456789, 2**53 + 1, -(2**53 + 1), 2**63 - 1])
@pytest.mark.parametrize(
    "index_name, showindex", [(None, "default"), ("row", "default"), ("row", False)]
)
def test_pandas_preserves_integer_columns(integer, index_name, showindex):
    "Integer columns retain their precision and formatting beside float columns."
    pandas = pytest.importorskip("pandas")
    df = pandas.DataFrame({"integer": [integer], "float": [1.23456789]})
    df.index.name = index_name
    rows = [[integer, 1.23456789]]
    headers = ["integer", "float"]
    if showindex == "default":
        rows = [[0] + row for row in rows]
        headers = [index_name or ""] + headers
    options = {"intfmt": ",", "floatfmt": ".2f"}

    result = tabulate(df, headers="keys", showindex=showindex, **options)

    assert result == tabulate(rows, headers=headers, **options)
    assert format(integer, ",") in result.split()
    assert format(1.23456789, ".2f") in result.split()


@pytest.mark.parametrize("columns", [["number", "number"], ["not an identifier", "_value"]])
def test_pandas_numeric_column_labels(columns):
    "Numeric columns keep their order even with duplicate or unusual labels."
    pandas = pytest.importorskip("pandas")
    rows = [[2**53 + 1, 1.25]]
    df = pandas.DataFrame(rows, columns=columns)
    options = {"showindex": False, "intfmt": ",", "floatfmt": ".2f"}
    assert tabulate(df, headers="keys", **options) == tabulate(rows, headers=columns, **options)


@pytest.mark.parametrize("dtype", ["int64", "Int64"])
@pytest.mark.parametrize("with_text", [False, True])
def test_pandas_integer_column_types(dtype, with_text):
    "Integer-only and mixed object tables retain their existing formatting."
    pandas = pytest.importorskip("pandas")
    df = pandas.DataFrame({"integer": pandas.Series([2**63 - 1], dtype=dtype)})
    rows = [[2**63 - 1]]
    if with_text:
        df["text"] = ["value"]
        rows[0].append("value")
    options = {"showindex": False, "intfmt": ",", "floatfmt": ".2f"}
    assert tabulate(df, **options) == tabulate(rows, **options)


@pytest.mark.parametrize("showindex", ["default", False])
@pytest.mark.parametrize("columns", [[], ["integer", "float"]])
def test_pandas_empty_dimensions(columns, showindex):
    "Empty rows and columns retain headers and any requested index."
    pandas = pytest.importorskip("pandas")
    index = [] if columns else ["a", "b"]
    df = pandas.DataFrame(index=index, columns=columns)
    rows = [] if columns else ([["a"], ["b"]] if showindex == "default" else [[], []])
    assert tabulate(df, headers="keys", showindex=showindex) == tabulate(rows, headers=columns)


def test_pandas_signed_and_unsigned_integer_columns():
    "Combining signed and unsigned integer columns must not round their values."
    pandas = pytest.importorskip("pandas")
    df = pandas.DataFrame(
        {
            "signed": pandas.Series([2**63 - 1], dtype="int64"),
            "unsigned": pandas.Series([2**64 - 1], dtype="uint64"),
        }
    )
    options = {"showindex": False, "intfmt": ","}
    result = tabulate(df, **options)
    assert result == tabulate([[2**63 - 1, 2**64 - 1]], **options)
    assert format(2**64 - 1, ",") in result.split()


@pytest.mark.parametrize("dtype", ["Int64", "UInt64"])
def test_pandas_nullable_integer_and_float_columns(dtype):
    "Nullable integer columns keep their precision beside floating point columns."
    pandas = pytest.importorskip("pandas")
    df = pandas.DataFrame({"integer": pandas.Series([2**63 - 1], dtype=dtype), "float": [1.25]})
    options = {"showindex": False, "intfmt": ",", "floatfmt": ".2f"}
    assert tabulate(df, **options) == tabulate([[2**63 - 1, 1.25]], **options)


@pytest.mark.parametrize("with_text", [False, True])
@pytest.mark.parametrize("kind", ["datetime", "timedelta", "timezone"])
def test_pandas_preserves_temporal_rendering(kind, with_text):
    "Numeric normalization does not change existing temporal scalar rendering."
    pandas = pytest.importorskip("pandas")
    if kind == "timedelta":
        values = pandas.to_timedelta([1], unit="D")
    else:
        values = pandas.to_datetime(["2020-01-01"])
        if kind == "timezone":
            values = values.tz_localize("UTC")
    df = pandas.DataFrame({"value": values})
    if with_text:
        df["text"] = ["value"]
    assert tabulate(df, showindex=False) == tabulate(df.values, showindex=False)


def test_sqlite3():
    "Input: an sqlite3 cursor"
    try:
        import sqlite3

        conn = sqlite3.connect(":memory:")
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE people (name, age, height)")
        for values in [("Alice", 23, 169.5), ("Bob", 27, 175.0)]:
            cursor.execute("INSERT INTO people VALUES (?, ?, ?)", values)
        cursor.execute("SELECT name, age, height FROM people ORDER BY name")
        result = tabulate(cursor, headers=["whom", "how old", "how tall"])
        conn.close()
        expected = """\
whom      how old    how tall
------  ---------  ----------
Alice          23       169.5
Bob            27       175"""
        assert_equal(expected, result)
    except ImportError:
        skip("test_sqlite3 is skipped")


def test_sqlite3_keys():
    "Input: an sqlite3 cursor with keys as headers"
    try:
        import sqlite3

        conn = sqlite3.connect(":memory:")
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE people (name, age, height)")
        for values in [("Alice", 23, 169.5), ("Bob", 27, 175.0)]:
            cursor.execute("INSERT INTO people VALUES (?, ?, ?)", values)
        cursor.execute(
            'SELECT name "whom", age "how old", height "how tall" FROM people ORDER BY name'
        )
        result = tabulate(cursor, headers="keys")
        conn.close()
        expected = """\
whom      how old    how tall
------  ---------  ----------
Alice          23       169.5
Bob            27       175"""
        assert_equal(expected, result)
    except ImportError:
        skip("test_sqlite3_keys is skipped")


def test_list_of_namedtuples():
    "Input: a list of named tuples with field names as headers."
    from collections import namedtuple

    NT = namedtuple("NT", ["foo", "bar"])
    lt = [NT(1, 2), NT(3, 4)]
    expected = "\n".join(["-  -", "1  2", "3  4", "-  -"])
    result = tabulate(lt)
    assert_equal(expected, result)


def test_list_of_namedtuples_keys():
    "Input: a list of named tuples with field names as headers."
    from collections import namedtuple

    NT = namedtuple("NT", ["foo", "bar"])
    lt = [NT(1, 2), NT(3, 4)]
    expected = "\n".join(["  foo    bar", "-----  -----", "    1      2", "    3      4"])
    result = tabulate(lt, headers="keys")
    assert_equal(expected, result)


def test_list_of_dicts():
    "Input: a list of dictionaries."
    lod = [{"foo": 1, "bar": 2}, {"foo": 3, "bar": 4}]
    expected1 = "\n".join(["-  -", "1  2", "3  4", "-  -"])
    expected2 = "\n".join(["-  -", "2  1", "4  3", "-  -"])
    result = tabulate(lod)
    assert_in(result, [expected1, expected2])


def test_list_of_userdicts():
    "Input: a list of UserDicts."
    lod = [UserDict(foo=1, bar=2), UserDict(foo=3, bar=4)]
    expected1 = "\n".join(["-  -", "1  2", "3  4", "-  -"])
    expected2 = "\n".join(["-  -", "2  1", "4  3", "-  -"])
    result = tabulate(lod)
    assert_in(result, [expected1, expected2])


def test_list_of_dicts_keys():
    "Input: a list of dictionaries, with keys as headers."
    lod = [{"foo": 1, "bar": 2}, {"foo": 3, "bar": 4}]
    expected1 = "\n".join(["  foo    bar", "-----  -----", "    1      2", "    3      4"])
    expected2 = "\n".join(["  bar    foo", "-----  -----", "    2      1", "    4      3"])
    result = tabulate(lod, headers="keys")
    assert_in(result, [expected1, expected2])


def test_list_of_userdicts_keys():
    "Input: a list of UserDicts."
    lod = [UserDict(foo=1, bar=2), UserDict(foo=3, bar=4)]
    expected1 = "\n".join(["  foo    bar", "-----  -----", "    1      2", "    3      4"])
    expected2 = "\n".join(["  bar    foo", "-----  -----", "    2      1", "    4      3"])
    result = tabulate(lod, headers="keys")
    assert_in(result, [expected1, expected2])


def test_list_of_dicts_with_missing_keys():
    "Input: a list of dictionaries, with missing keys."
    lod = [{"foo": 1}, {"bar": 2}, {"foo": 4, "baz": 3}]
    expected = "\n".join(
        [
            "  foo    bar    baz",
            "-----  -----  -----",
            "    1",
            "           2",
            "    4             3",
        ]
    )
    result = tabulate(lod, headers="keys")
    assert_equal(expected, result)


def test_list_of_dicts_firstrow():
    "Input: a list of dictionaries, with the first dict as headers."
    lod = [{"foo": "FOO", "bar": "BAR"}, {"foo": 3, "bar": 4, "baz": 5}]
    # if some key is missing in the first dict, use the key name instead
    expected1 = "\n".join(["  FOO    BAR    baz", "-----  -----  -----", "    3      4      5"])
    expected2 = "\n".join(["  BAR    FOO    baz", "-----  -----  -----", "    4      3      5"])
    result = tabulate(lod, headers="firstrow")
    assert_in(result, [expected1, expected2])


def test_list_of_dicts_with_dict_of_headers():
    "Input: a dict of user headers for a list of dicts (issue #23)"
    table = [{"letters": "ABCDE", "digits": 12345}]
    headers = {"digits": "DIGITS", "letters": "LETTERS"}
    expected1 = "\n".join(["  DIGITS  LETTERS", "--------  ---------", "   12345  ABCDE"])
    expected2 = "\n".join(["LETTERS      DIGITS", "---------  --------", "ABCDE         12345"])
    result = tabulate(table, headers=headers)
    assert_in(result, [expected1, expected2])


def test_list_of_dicts_with_list_of_headers():
    "Input: ValueError on a list of headers with a list of dicts (issue #23)"
    table = [{"letters": "ABCDE", "digits": 12345}]
    headers = ["DIGITS", "LETTERS"]
    with raises(ValueError):
        tabulate(table, headers=headers)


def test_list_of_ordereddicts():
    "Input: a list of OrderedDicts."
    from collections import OrderedDict

    od = OrderedDict([("b", 1), ("a", 2)])
    lod = [od, od]
    expected = "\n".join(["  b    a", "---  ---", "  1    2", "  1    2"])
    result = tabulate(lod, headers="keys")
    assert_equal(expected, result)


def test_py37orlater_list_of_dataclasses_keys():
    "Input: a list of dataclasses with first item's fields as keys and headers"
    try:
        from dataclasses import make_dataclass

        Person = make_dataclass("Person", ["name", "age", "height"])
        ld = [Person("Alice", 23, 169.5), Person("Bob", 27, 175.0)]
        result = tabulate(ld, headers="keys")
        expected = "\n".join(
            [
                "name      age    height",
                "------  -----  --------",
                "Alice      23     169.5",
                "Bob        27     175",
            ]
        )
        assert_equal(expected, result)
    except ImportError:
        skip("test_py37orlater_list_of_dataclasses_keys is skipped")


def test_py37orlater_list_of_dataclasses_headers():
    "Input: a list of dataclasses with user-supplied headers"
    try:
        from dataclasses import make_dataclass

        Person = make_dataclass("Person", ["name", "age", "height"])
        ld = [Person("Alice", 23, 169.5), Person("Bob", 27, 175.0)]
        result = tabulate(ld, headers=["person", "years", "cm"])
        expected = "\n".join(
            [
                "person      years     cm",
                "--------  -------  -----",
                "Alice          23  169.5",
                "Bob            27  175",
            ]
        )
        assert_equal(expected, result)
    except ImportError:
        skip("test_py37orlater_list_of_dataclasses_headers is skipped")


def test_py37orlater_list_of_dataclasses_with_separating_line():
    "Input: a list of dataclasses with a separating line"
    try:
        from dataclasses import make_dataclass

        Person = make_dataclass("Person", ["name", "age", "height"])
        ld = [Person("Alice", 23, 169.5), SEPARATING_LINE, Person("Bob", 27, 175.0)]
        result = tabulate(ld, headers="keys")
        expected = "\n".join(
            [
                "name      age    height",
                "------  -----  --------",
                "Alice      23     169.5",
                "------  -----  --------",
                "Bob        27     175",
            ]
        )
        assert_equal(expected, result)
    except ImportError:
        skip("test_py37orlater_list_of_dataclasses_keys is skipped")


def test_list_bytes():
    "Input: a list of bytes. (issue #192)"
    lb = [["你好".encode()], ["你好"]]
    expected = "\n".join(
        ["bytes", "---------------------------", r"b'\xe4\xbd\xa0\xe5\xa5\xbd'", "你好"]
    )
    result = tabulate(lb, headers=["bytes"])
    assert_equal(expected, result)
