# -*- coding: utf-8 -*-

"""Test support of the various forms of tabular data."""

from __future__ import print_function
from __future__ import unicode_literals
from tabulate import tabulate


def test_iterable_of_iterables():
    "Printing an interable of iterables."
    ii = iter(map(lambda x: iter(x), [range(5), range(5,0,-1)]))
    expected = u'-  -  -  -  -\n0  1  2  3  4\n5  4  3  2  1\n-  -  -  -  -'
    result   = tabulate(ii)
    print("Expected:\n%s\n" % expected)
    print("Got:\n%s\n" % result)
    assert expected == result


def test_iterable_of_iterables_headers():
    "Printing an interable of iterables."
    ii = iter(map(lambda x: iter(x), [range(5), range(5,0,-1)]))
    expected = u'  a    b    c    d    e\n---  ---  ---  ---  ---\n' + \
               u'  0    1    2    3    4\n  5    4    3    2    1'
    result   = tabulate(ii, "abcde")
    print("Expected:\n%s\n" % expected)
    print("Got:\n%s\n" % result)
    assert expected == result


def test_iterable_of_iterables_firstrow():
    "Printing an interable of iterables."
    ii = iter(map(lambda x: iter(x), ["abcde", range(5), range(5,0,-1)]))
    expected = u'  a    b    c    d    e\n---  ---  ---  ---  ---\n' + \
               u'  0    1    2    3    4\n  5    4    3    2    1'
    result   = tabulate(ii, "firstrow")
    print("Expected:\n%s\n" % expected)
    print("Got:\n%s\n" % result)
    assert expected == result


def test_list_of_lists():
    "Printing a list of lists."
    ll = [["a","one",1],["b","two",None]]
    expected = u'    string      number\n--  --------  --------\n' + \
               u'a   one              1\nb   two'
    result   = tabulate(ll, headers=["string","number"])
    print("Expected:\n%s\n" % expected)
    print("Got:\n%s\n" % result)
    assert expected == result


def test_list_of_lists_firstrow():
    "Printing an interable of iterables with firstrow as headers."
    ll = [["string","number"],["a","one",1],["b","two",None]]
    expected = u'    string      number\n--  --------  --------\n' + \
               u'a   one              1\nb   two'
    result   = tabulate(ll, headers="firstrow")
    print("Expected:\n%s\n" % expected)
    print("Got:\n%s\n" % result)
    assert expected == result


def test_list_of_lists_keys():
    "Printing an interable of iterables with column indices as headers."
    ll = [["a","one",1],["b","two",None]]
    expected = u'0    1      2\n---  ---  ---\na    one    1\nb    two'
    result   = tabulate(ll, headers="keys")
    print("Expected:\n%s\n" % expected)
    print("Got:\n%s\n" % result)
    assert expected == result


def test_dict_like():
    "Printing a dict of iterables with keys as headers."
    # columns should be padded with None, keys should be used as headers
    dd = {"a": range(3), "b": range(101,105)}
    # keys' order (hence columns' order) is not deterministic in Python 3
    # => we have to consider both possible results as valid
    expected1 = u'  a    b\n---  ---\n  0  101\n  1  102\n  2  103\n     104'
    expected2 = u'  b    a\n---  ---\n101    0\n102    1\n103    2\n104'
    result    = tabulate(dd, "keys")
    print("Keys' order: %s" % dd.keys())
    print("Expected 1:\n%s\n" % expected1)
    print("Expected 2:\n%s\n" % expected2)
    print("Got:\n%s\n" % result)
    assert result in [expected1, expected2]


def test_numpy_2d():
    "Printing a two-dimensional NumPy array."
    try:
        import numpy
        na = (numpy.arange(1,10, dtype=numpy.float32).reshape((3,3))**3)*0.5
        expected = u'    a      b      c\n-----  -----  -----\n' + \
                   u'  0.5    4     13.5\n 32     62.5  108\n171.5  256    364.5'
        result   = tabulate(na, ["a", "b", "c"])
        print("Expected:\n%s\n" % expected)
        print("Got:\n%s\n" % result)
        assert expected == result
    except ImportError:
        print("test_numpy_2d is skipped")
        pass   # this test is optional


def test_numpy_2d_firstrow():
    "Printing a two-dimensional NumPy array with the first row as headers."
    try:
        import numpy
        na = (numpy.arange(1,10, dtype=numpy.int32).reshape((3,3))**3)
        expected = u'  1    8    27\n---  ---  ----\n 64  125   216\n343  512   729'
        result   = tabulate(na, headers="firstrow")
        print("Expected:\n%s\n" % expected)
        print("Got:\n%r\n" % result)
        assert expected == result
    except ImportError:
        print("test_numpy_2d_firstrow is skipped")
        pass   # this test is optional


def test_numpy_2d_keys():
    "Printing a two-dimensional NumPy array with column indices as headers."
    try:
        import numpy
        na = (numpy.arange(1,10, dtype=numpy.float32).reshape((3,3))**3)*0.5
        expected = u'    0      1      2\n-----  -----  -----\n' + \
                   u'  0.5    4     13.5\n 32     62.5  108\n171.5  256    364.5'
        result   = tabulate(na, headers="keys")
        print("Expected:\n%s\n" % expected)
        print("Got:\n%s\n" % result)
        assert expected == result
    except ImportError:
        print("test_numpy_2d_keys is skipped")
        pass   # this test is optional


def test_pandas():
    "Printing a Pandas DataFrame."
    try:
        import pandas
        df = pandas.DataFrame([["one",1],["two",None]], index=["a","b"])
        expected = u'    string      number\n--  --------  --------\n' + \
                   u'a   one              1\nb   two            nan'
        result   = tabulate(df, headers=["string", "number"])
        print("Expected:\n%s\n" % expected)
        print("Got:\n%s\n" % result)
        assert expected == result
    except ImportError:
        print("test_pandas is skipped")
        pass   # this test is optional


def test_pandas_firstrow():
    "Printing a Pandas DataFrame with the first row as headers."
    try:
        import pandas
        df = pandas.DataFrame([["one",1],["two",None]],
                              columns=["string","number"],
                              index=["a","b"])
        expected = u'a    one      1.0\n---  -----  -----\nb    two      nan'
        result   = tabulate(df, headers="firstrow")
        print("Expected:\n%s\n" % expected)
        print("Got:\n%s\n" % result)
        assert expected == result
    except ImportError:
        print("test_pandas_firstrow is skipped")
        pass   # this test is optional


def test_pandas_keys():
    "Printing a Pandas DataFrame with keys as headers."
    try:
        import pandas
        df = pandas.DataFrame([["one",1],["two",None]],
                              columns=["string","number"],
                              index=["a","b"])
        expected = u'    string      number\n--  --------  --------\n' + \
                   u'a   one              1\nb   two            nan'
        result   = tabulate(df, headers="keys")
        print("Expected:\n%s\n" % expected)
        print("Got:\n%s\n" % result)
        assert expected == result
    except ImportError:
        print("test_pandas_keys is skipped")
        pass   # this test is optional
