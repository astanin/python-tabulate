# -*- coding: utf-8 -*-

"""Test support of the various forms of tabular data."""

from __future__ import print_function
from __future__ import unicode_literals
from tabulate import tabulate


def test_iterable_of_iterables():
    "Input: an interable of iterables."
    ii = iter(map(lambda x: iter(x), [range(5), range(5,0,-1)]))
    expected = "\n".join(
        [u'-  -  -  -  -',
         u'0  1  2  3  4',
         u'5  4  3  2  1',
         u'-  -  -  -  -'])
    result   = tabulate(ii)
    print("Expected:\n%s\n" % expected)
    print("Got:\n%s\n" % result)
    assert expected == result


def test_iterable_of_iterables_headers():
    "Input: an interable of iterables with headers."
    ii = iter(map(lambda x: iter(x), [range(5), range(5,0,-1)]))
    expected = "\n".join(
        [u'  a    b    c    d    e',
         u'---  ---  ---  ---  ---',
         u'  0    1    2    3    4',
         u'  5    4    3    2    1'])
    result   = tabulate(ii, "abcde")
    print("Expected:\n%s\n" % expected)
    print("Got:\n%s\n" % result)
    assert expected == result


def test_iterable_of_iterables_firstrow():
    "Input: an interable of iterables with the first row as headers"
    ii = iter(map(lambda x: iter(x), ["abcde", range(5), range(5,0,-1)]))
    expected = "\n".join(
        [u'  a    b    c    d    e',
         u'---  ---  ---  ---  ---',
         u'  0    1    2    3    4',
         u'  5    4    3    2    1'])
    result   = tabulate(ii, "firstrow")
    print("Expected:\n%s\n" % expected)
    print("Got:\n%s\n" % result)
    assert expected == result


def test_list_of_lists():
    "Input: a list of lists with headers."
    ll = [["a","one",1],["b","two",None]]
    expected = "\n".join([
        u'    string      number',
        u'--  --------  --------',
        u'a   one              1',
        u'b   two'])
    result   = tabulate(ll, headers=["string","number"])
    print("Expected:\n%s\n" % expected)
    print("Got:\n%s\n" % result)
    assert expected == result


def test_list_of_lists_firstrow():
    "Input: a list of lists with the first row as headers."
    ll = [["string","number"],["a","one",1],["b","two",None]]
    expected = "\n".join([
        u'    string      number',
        u'--  --------  --------',
        u'a   one              1',
        u'b   two'])
    result   = tabulate(ll, headers="firstrow")
    print("Expected:\n%s\n" % expected)
    print("Got:\n%s\n" % result)
    assert expected == result


def test_list_of_lists_keys():
    "Input: a list of lists with column indices as headers."
    ll = [["a","one",1],["b","two",None]]
    expected = "\n".join([
        u'0    1      2',
        u'---  ---  ---',
        u'a    one    1',
        u'b    two'])
    result   = tabulate(ll, headers="keys")
    print("Expected:\n%s\n" % expected)
    print("Got:\n%s\n" % result)
    assert expected == result


def test_dict_like():
    "Input: a dict of iterables with keys as headers."
    # columns should be padded with None, keys should be used as headers
    dd = {"a": range(3), "b": range(101,105)}
    # keys' order (hence columns' order) is not deterministic in Python 3
    # => we have to consider both possible results as valid
    expected1 = "\n".join([
        u'  a    b',
        u'---  ---',
        u'  0  101',
        u'  1  102',
        u'  2  103',
        u'     104'])
    expected2 = "\n".join([
        u'  b    a',
        u'---  ---',
        u'101    0',
        u'102    1',
        u'103    2',
        u'104'])
    result    = tabulate(dd, "keys")
    print("Keys' order: %s" % dd.keys())
    print("Expected 1:\n%s\n" % expected1)
    print("Expected 2:\n%s\n" % expected2)
    print("Got:\n%s\n" % result)
    assert result in [expected1, expected2]


def test_numpy_2d():
    "Input: a two-dimensional NumPy array with headers."
    try:
        import numpy
        na = (numpy.arange(1,10, dtype=numpy.float32).reshape((3,3))**3)*0.5
        expected = "\n".join([
            u'    a      b      c',
            u'-----  -----  -----',
            u'  0.5    4     13.5',
            u' 32     62.5  108',
            u'171.5  256    364.5'])
        result   = tabulate(na, ["a", "b", "c"])
        print("Expected:\n%s\n" % expected)
        print("Got:\n%s\n" % result)
        assert expected == result
    except ImportError:
        print("test_numpy_2d is skipped")
        pass   # this test is optional


def test_numpy_2d_firstrow():
    "Input: a two-dimensional NumPy array with the first row as headers."
    try:
        import numpy
        na = (numpy.arange(1,10, dtype=numpy.int32).reshape((3,3))**3)
        expected = "\n".join([
            u'  1    8    27',
            u'---  ---  ----',
            u' 64  125   216',
            u'343  512   729'])
        result   = tabulate(na, headers="firstrow")
        print("Expected:\n%s\n" % expected)
        print("Got:\n%r\n" % result)
        assert expected == result
    except ImportError:
        print("test_numpy_2d_firstrow is skipped")
        pass   # this test is optional


def test_numpy_2d_keys():
    "Input: a two-dimensional NumPy array with column indices as headers."
    try:
        import numpy
        na = (numpy.arange(1,10, dtype=numpy.float32).reshape((3,3))**3)*0.5
        expected = "\n".join([
            u'    0      1      2',
            u'-----  -----  -----',
            u'  0.5    4     13.5',
            u' 32     62.5  108',
            u'171.5  256    364.5'])
        result   = tabulate(na, headers="keys")
        print("Expected:\n%s\n" % expected)
        print("Got:\n%s\n" % result)
        assert expected == result
    except ImportError:
        print("test_numpy_2d_keys is skipped")
        pass   # this test is optional


def test_numpy_record_array():
    "Input: a two-dimensional NumPy record array without header."
    try:
        import numpy
        na = numpy.asarray([("Alice", 23, 169.5),
                            ("Bob", 27, 175.0)],
                           dtype={"names":["name","age","height"],
                                  "formats":["a32","uint8","f32"]})
        expected = "\n".join([
            "-----  --  -----",
            "Alice  23  169.5",
            "Bob    27  175",
            "-----  --  -----" ])
        result   = tabulate(na)
        print("Expected:\n%s\n" % expected)
        print("Got:\n%s\n" % result)
        assert expected == result
    except ImportError:
        print("test_numpy_2d_keys is skipped")
        pass   # this test is optional


def test_numpy_record_array_keys():
    "Input: a two-dimensional NumPy record array with column names as headers."
    try:
        import numpy
        na = numpy.asarray([("Alice", 23, 169.5),
                            ("Bob", 27, 175.0)],
                           dtype={"names":["name","age","height"],
                                  "formats":["a32","uint8","f32"]})
        expected = "\n".join([
            "name      age    height",
            "------  -----  --------",
            "Alice      23     169.5",
            "Bob        27     175"  ])
        result   = tabulate(na, headers="keys")
        print("Expected:\n%s\n" % expected)
        print("Got:\n%s\n" % result)
        assert expected == result
    except ImportError:
        print("test_numpy_2d_keys is skipped")
        pass   # this test is optional


def test_numpy_record_array_headers():
    "Input: a two-dimensional NumPy record array with user-supplied headers."
    try:
        import numpy
        na = numpy.asarray([("Alice", 23, 169.5),
                            ("Bob", 27, 175.0)],
                           dtype={"names":["name","age","height"],
                                  "formats":["a32","uint8","f32"]})
        expected = "\n".join([
            "person      years     cm",
            "--------  -------  -----",
            "Alice          23  169.5",
            "Bob            27  175" ])
        result   = tabulate(na, headers=["person", "years", "cm"])
        print("Expected:\n%s\n" % expected)
        print("Got:\n%s\n" % result)
        assert expected == result
    except ImportError:
        print("test_numpy_2d_keys is skipped")
        pass   # this test is optional


def test_pandas():
    "Input: a Pandas DataFrame."
    try:
        import pandas
        df = pandas.DataFrame([["one",1],["two",None]], index=["a","b"])
        expected = "\n".join([
            u'    string      number',
            u'--  --------  --------',
            u'a   one              1',
            u'b   two            nan'])
        result   = tabulate(df, headers=["string", "number"])
        print("Expected:\n%s\n" % expected)
        print("Got:\n%s\n" % result)
        assert expected == result
    except ImportError:
        print("test_pandas is skipped")
        pass   # this test is optional


def test_pandas_firstrow():
    "Input: a Pandas DataFrame with the first row as headers."
    try:
        import pandas
        df = pandas.DataFrame([["one",1],["two",None]],
                              columns=["string","number"],
                              index=["a","b"])
        expected = "\n".join([
            u'a    one      1.0',
            u'---  -----  -----',
            u'b    two      nan'])
        result   = tabulate(df, headers="firstrow")
        print("Expected:\n%s\n" % expected)
        print("Got:\n%s\n" % result)
        assert expected == result
    except ImportError:
        print("test_pandas_firstrow is skipped")
        pass   # this test is optional


def test_pandas_keys():
    "Input: a Pandas DataFrame with keys as headers."
    try:
        import pandas
        df = pandas.DataFrame([["one",1],["two",None]],
                              columns=["string","number"],
                              index=["a","b"])
        expected = "\n".join(
            [u'    string      number',
             u'--  --------  --------',
             u'a   one              1',
             u'b   two            nan'])
        result   = tabulate(df, headers="keys")
        print("Expected:\n%s\n" % expected)
        print("Got:\n%s\n" % result)
        assert expected == result
    except ImportError:
        print("test_pandas_keys is skipped")
        pass   # this test is optional


def test_list_of_namedtuples():
    "Input: a list of named tuples with field names as headers."
    from collections import namedtuple
    NT = namedtuple("NT", ['foo', 'bar'])
    lt = [NT(1,2), NT(3,4)]
    expected = u"\n".join([
        u'-  -',
        u'1  2',
        u'3  4',
        u'-  -'])
    result = tabulate(lt)
    print("Expected:\n%s\n" % expected)
    print("Got:\n%s\n" % result)
    assert expected == result


def test_list_of_namedtuples_keys():
    "Input: a list of named tuples with field names as headers."
    from collections import namedtuple
    NT = namedtuple("NT", ['foo', 'bar'])
    lt = [NT(1,2), NT(3,4)]
    expected = u"\n".join([
        u'  foo    bar',
        u'-----  -----',
        u'    1      2',
        u'    3      4'])
    result = tabulate(lt, headers="keys")
    print("Expected:\n%s\n" % expected)
    print("Got:\n%s\n" % result)
    assert expected == result
