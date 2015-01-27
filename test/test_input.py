# -*- coding: utf-8 -*-

"""Test support of the various forms of tabular data."""

from __future__ import print_function
from __future__ import unicode_literals
from tabulate import tabulate
from common import assert_equal, assert_in, assert_raises
from nose.plugins.skip import SkipTest


def test_iterable_of_iterables():
    "Input: an interable of iterables."
    ii = iter(map(lambda x: iter(x), [range(5), range(5,0,-1)]))
    expected = "\n".join(
        ['-  -  -  -  -',
         '0  1  2  3  4',
         '5  4  3  2  1',
         '-  -  -  -  -'])
    result   = tabulate(ii)
    assert_equal(expected, result)


def test_iterable_of_iterables_headers():
    "Input: an interable of iterables with headers."
    ii = iter(map(lambda x: iter(x), [range(5), range(5,0,-1)]))
    expected = "\n".join(
        ['  a    b    c    d    e',
         '---  ---  ---  ---  ---',
         '  0    1    2    3    4',
         '  5    4    3    2    1'])
    result   = tabulate(ii, "abcde")
    assert_equal(expected, result)


def test_iterable_of_iterables_firstrow():
    "Input: an interable of iterables with the first row as headers"
    ii = iter(map(lambda x: iter(x), ["abcde", range(5), range(5,0,-1)]))
    expected = "\n".join(
        ['  a    b    c    d    e',
         '---  ---  ---  ---  ---',
         '  0    1    2    3    4',
         '  5    4    3    2    1'])
    result   = tabulate(ii, "firstrow")
    assert_equal(expected, result)


def test_list_of_lists():
    "Input: a list of lists with headers."
    ll = [["a","one",1],["b","two",None]]
    expected = "\n".join([
        '    string      number',
        '--  --------  --------',
        'a   one              1',
        'b   two'])
    result   = tabulate(ll, headers=["string","number"])
    assert_equal(expected, result)


def test_list_of_lists_firstrow():
    "Input: a list of lists with the first row as headers."
    ll = [["string","number"],["a","one",1],["b","two",None]]
    expected = "\n".join([
        '    string      number',
        '--  --------  --------',
        'a   one              1',
        'b   two'])
    result   = tabulate(ll, headers="firstrow")
    assert_equal(expected, result)


def test_list_of_lists_keys():
    "Input: a list of lists with column indices as headers."
    ll = [["a","one",1],["b","two",None]]
    expected = "\n".join([
        '0    1      2',
        '---  ---  ---',
        'a    one    1',
        'b    two'])
    result   = tabulate(ll, headers="keys")
    assert_equal(expected, result)


def test_dict_like():
    "Input: a dict of iterables with keys as headers."
    # columns should be padded with None, keys should be used as headers
    dd = {"a": range(3), "b": range(101,105)}
    # keys' order (hence columns' order) is not deterministic in Python 3
    # => we have to consider both possible results as valid
    expected1 = "\n".join([
        '  a    b',
        '---  ---',
        '  0  101',
        '  1  102',
        '  2  103',
        '     104'])
    expected2 = "\n".join([
        '  b    a',
        '---  ---',
        '101    0',
        '102    1',
        '103    2',
        '104'])
    result    = tabulate(dd, "keys")
    print("Keys' order: %s" % dd.keys())
    assert_in(result, [expected1, expected2])


def test_numpy_2d():
    "Input: a two-dimensional NumPy array with headers."
    try:
        import numpy
        na = (numpy.arange(1,10, dtype=numpy.float32).reshape((3,3))**3)*0.5
        expected = "\n".join([
            '    a      b      c',
            '-----  -----  -----',
            '  0.5    4     13.5',
            ' 32     62.5  108',
            '171.5  256    364.5'])
        result   = tabulate(na, ["a", "b", "c"])
        assert_equal(expected, result)
    except ImportError:
        print("test_numpy_2d is skipped")
        raise SkipTest()   # this test is optional


def test_numpy_2d_firstrow():
    "Input: a two-dimensional NumPy array with the first row as headers."
    try:
        import numpy
        na = (numpy.arange(1,10, dtype=numpy.int32).reshape((3,3))**3)
        expected = "\n".join([
            '  1    8    27',
            '---  ---  ----',
            ' 64  125   216',
            '343  512   729'])
        result   = tabulate(na, headers="firstrow")
        assert_equal(expected, result)
    except ImportError:
        print("test_numpy_2d_firstrow is skipped")
        raise SkipTest()   # this test is optional



def test_numpy_2d_keys():
    "Input: a two-dimensional NumPy array with column indices as headers."
    try:
        import numpy
        na = (numpy.arange(1,10, dtype=numpy.float32).reshape((3,3))**3)*0.5
        expected = "\n".join([
            '    0      1      2',
            '-----  -----  -----',
            '  0.5    4     13.5',
            ' 32     62.5  108',
            '171.5  256    364.5'])
        result   = tabulate(na, headers="keys")
        assert_equal(expected, result)
    except ImportError:
        print("test_numpy_2d_keys is skipped")
        raise SkipTest()   # this test is optional


def test_numpy_record_array():
    "Input: a two-dimensional NumPy record array without header."
    try:
        import numpy
        na = numpy.asarray([("Alice", 23, 169.5),
                            ("Bob", 27, 175.0)],
                           dtype={"names":["name","age","height"],
                                  "formats":["a32","uint8","float32"]})
        expected = "\n".join([
            "-----  --  -----",
            "Alice  23  169.5",
            "Bob    27  175",
            "-----  --  -----" ])
        result   = tabulate(na)
        assert_equal(expected, result)
    except ImportError:
        print("test_numpy_2d_keys is skipped")
        raise SkipTest()   # this test is optional


def test_numpy_record_array_keys():
    "Input: a two-dimensional NumPy record array with column names as headers."
    try:
        import numpy
        na = numpy.asarray([("Alice", 23, 169.5),
                            ("Bob", 27, 175.0)],
                           dtype={"names":["name","age","height"],
                                  "formats":["a32","uint8","float32"]})
        expected = "\n".join([
            "name      age    height",
            "------  -----  --------",
            "Alice      23     169.5",
            "Bob        27     175"  ])
        result   = tabulate(na, headers="keys")
        assert_equal(expected, result)
    except ImportError:
        print("test_numpy_2d_keys is skipped")
        raise SkipTest()   # this test is optional


def test_numpy_record_array_headers():
    "Input: a two-dimensional NumPy record array with user-supplied headers."
    try:
        import numpy
        na = numpy.asarray([("Alice", 23, 169.5),
                            ("Bob", 27, 175.0)],
                           dtype={"names":["name","age","height"],
                                  "formats":["a32","uint8","float32"]})
        expected = "\n".join([
            "person      years     cm",
            "--------  -------  -----",
            "Alice          23  169.5",
            "Bob            27  175" ])
        result   = tabulate(na, headers=["person", "years", "cm"])
        assert_equal(expected, result)
    except ImportError:
        print("test_numpy_2d_keys is skipped")
        raise SkipTest()   # this test is optional


def test_pandas():
    "Input: a Pandas DataFrame."
    try:
        import pandas
        df = pandas.DataFrame([["one",1],["two",None]], index=["a","b"])
        expected = "\n".join([
            '    string      number',
            '--  --------  --------',
            'a   one              1',
            'b   two            nan'])
        result   = tabulate(df, headers=["string", "number"])
        assert_equal(expected, result)
    except ImportError:
        print("test_pandas is skipped")
        raise SkipTest()   # this test is optional


def test_pandas_firstrow():
    "Input: a Pandas DataFrame with the first row as headers."
    try:
        import pandas
        df = pandas.DataFrame([["one",1],["two",None]],
                              columns=["string","number"],
                              index=["a","b"])
        expected = "\n".join([
            'a    one      1.0',
            '---  -----  -----',
            'b    two      nan'])
        result   = tabulate(df, headers="firstrow")
        assert_equal(expected, result)
    except ImportError:
        print("test_pandas_firstrow is skipped")
        raise SkipTest()   # this test is optional


def test_pandas_keys():
    "Input: a Pandas DataFrame with keys as headers."
    try:
        import pandas
        df = pandas.DataFrame([["one",1],["two",None]],
                              columns=["string","number"],
                              index=["a","b"])
        expected = "\n".join(
            ['    string      number',
             '--  --------  --------',
             'a   one              1',
             'b   two            nan'])
        result   = tabulate(df, headers="keys")
        assert_equal(expected, result)
    except ImportError:
        print("test_pandas_keys is skipped")
        raise SkipTest()   # this test is optional


def test_list_of_namedtuples():
    "Input: a list of named tuples with field names as headers."
    from collections import namedtuple
    NT = namedtuple("NT", ['foo', 'bar'])
    lt = [NT(1,2), NT(3,4)]
    expected = "\n".join([
        '-  -',
        '1  2',
        '3  4',
        '-  -'])
    result = tabulate(lt)
    assert_equal(expected, result)


def test_list_of_namedtuples_keys():
    "Input: a list of named tuples with field names as headers."
    from collections import namedtuple
    NT = namedtuple("NT", ['foo', 'bar'])
    lt = [NT(1,2), NT(3,4)]
    expected = "\n".join([
        '  foo    bar',
        '-----  -----',
        '    1      2',
        '    3      4'])
    result = tabulate(lt, headers="keys")
    assert_equal(expected, result)


def test_list_of_dicts():
    "Input: a list of dictionaries."
    lod = [{'foo' : 1, 'bar' : 2}, {'foo' : 3, 'bar' : 4}]
    expected1 = "\n".join([
        '-  -',
        '1  2',
        '3  4',
        '-  -'])
    expected2 = "\n".join([
        '-  -',
        '2  1',
        '4  3',
        '-  -'])
    result = tabulate(lod)
    assert_in(result, [expected1, expected2])


def test_list_of_dicts_keys():
    "Input: a list of dictionaries, with keys as headers."
    lod = [{'foo' : 1, 'bar' : 2}, {'foo' : 3, 'bar' : 4}]
    expected1 = "\n".join([
        '  foo    bar',
        '-----  -----',
        '    1      2',
        '    3      4'])
    expected2 = "\n".join([
        '  bar    foo',
        '-----  -----',
        '    2      1',
        '    4      3'])
    result = tabulate(lod, headers="keys")
    assert_in(result, [expected1, expected2])


def test_list_of_dicts_with_missing_keys():
    "Input: a list of dictionaries, with missing keys."
    lod = [{"foo": 1}, {"bar": 2}, {"foo":4, "baz": 3}]
    expected = "\n".join([
        '  foo    bar    baz',
        '-----  -----  -----',
        '    1',
        '           2',
        '    4             3'])
    result = tabulate(lod, headers="keys")
    assert_equal(expected, result)


def test_list_of_dicts_firstrow():
    "Input: a list of dictionaries, with the first dict as headers."
    lod = [{'foo' : "FOO", 'bar' : "BAR"}, {'foo' : 3, 'bar': 4, 'baz': 5}]
    # if some key is missing in the first dict, use the key name instead
    expected1 = "\n".join([
        '  FOO    BAR    baz',
        '-----  -----  -----',
        '    3      4      5'])
    expected2 = "\n".join([
        '  BAR    FOO    baz',
        '-----  -----  -----',
        '    4      3      5'])
    result = tabulate(lod, headers="firstrow")
    assert_in(result, [expected1, expected2])


def test_list_of_dicts_with_dict_of_headers():
    "Input: a dict of user headers for a list of dicts (issue #23)"
    table = [{"letters": "ABCDE", "digits": 12345}]
    headers = {"digits": "DIGITS", "letters": "LETTERS"}
    expected1 = "\n".join([
        '  DIGITS  LETTERS',
        '--------  ---------',
        '   12345  ABCDE'])
    expected2 = "\n".join([
        'LETTERS      DIGITS',
        '---------  --------',
        'ABCDE         12345'])
    result = tabulate(table, headers=headers)
    assert_in(result, [expected1, expected2])


def test_list_of_dicts_with_list_of_headers():
    "Input: a list of headers for a list of dicts, raise ValueError (issue #23)"
    table = [{"letters": "ABCDE", "digits": 12345}]
    headers = ["DIGITS", "LETTERS"]
    with assert_raises(ValueError):
        tabulate(table, headers=headers)


def test_py27orlater_list_of_ordereddicts():
    "Input: a list of OrderedDicts."
    from collections import OrderedDict
    od = OrderedDict([('b', 1), ('a', 2)])
    lod = [od, od]
    expected = "\n".join([
        '  b    a',
        '---  ---',
        '  1    2',
        '  1    2'])
    result = tabulate(lod, headers="keys")
    assert_equal(expected, result)
