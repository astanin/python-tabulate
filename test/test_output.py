# -*- coding: utf-8 -*-

"""Test output of the various forms of tabular data."""

from __future__ import print_function
from __future__ import unicode_literals
from tabulate import tabulate

try:
    from nose.tools import assert_equal
except ImportError:
    def assert_equal(expected, result):
        print("Expected:\n%s\n" % expected)
        print("Got:\n%s\n" % result)
        assert expected == result


# _test_table shows
#  - coercion of a string to a number,
#  - left alignment of text,
#  - decimal point alignment of numbers
_test_table = [["spam", 41.9999], ["eggs", "451.0"]]
_test_table_headers = ["strings", "numbers"]


def test_plain():
    "Output: plain with headers"
    expected = u"\n".join([u'strings      numbers',
                           u'spam         41.9999',
                           u'eggs        451',])
    result = tabulate(_test_table, _test_table_headers, tablefmt="plain")
    assert_equal(expected, result)


def test_plain_headerless():
    "Output: plain without headers"
    expected = u"\n".join([u'spam   41.9999',
                           u'eggs  451',])
    result = tabulate(_test_table, tablefmt="plain")
    assert_equal(expected, result)


def test_simple():
    "Output: simple with headers"
    expected = u"\n".join([u'strings      numbers',
                           u'---------  ---------',
                           u'spam         41.9999',
                           u'eggs        451',])
    result = tabulate(_test_table, _test_table_headers, tablefmt="simple")
    assert_equal(expected, result)


def test_simple_headerless():
    "Output: simple without headers"
    expected = u"\n".join([u'----  --------',
                           u'spam   41.9999',
                           u'eggs  451',
                           u'----  --------',])
    result = tabulate(_test_table, tablefmt="simple")
    assert_equal(expected, result)


def test_grid():
    "Output: grid with headers"
    expected = u'\n'.join([u'+-----------+-----------+',
                           u'| strings   |   numbers |',
                           u'+===========+===========+',
                           u'| spam      |   41.9999 |',
                           u'+-----------+-----------+',
                           u'| eggs      |  451      |',
                           u'+-----------+-----------+',])
    result = tabulate(_test_table, _test_table_headers, tablefmt="grid")
    assert_equal(expected, result)


def test_grid_headerless():
    "Output: grid without headers"
    expected = u'\n'.join([u'+------+----------+',
                           u'| spam |  41.9999 |',
                           u'+------+----------+',
                           u'| eggs | 451      |',
                           u'+------+----------+',])
    result = tabulate(_test_table, tablefmt="grid")
    assert_equal(expected, result)


def test_pipe():
    "Output: pipe with headers"
    expected = u'\n'.join([u'| strings   |   numbers |',
                           u'|:----------|----------:|',
                           u'| spam      |   41.9999 |',
                           u'| eggs      |  451      |',])
    result = tabulate(_test_table, _test_table_headers, tablefmt="pipe")
    assert_equal(expected, result)


def test_pipe_headerless():
    "Output: pipe without headers"
    expected = u'\n'.join([u'|:-----|---------:|',
                           u'| spam |  41.9999 |',
                           u'| eggs | 451      |',])
    result = tabulate(_test_table, tablefmt="pipe")
    assert_equal(expected, result)


def test_orgtbl():
    "Output: orgtbl with headers"
    expected = u'\n'.join([u'| strings   |   numbers |',
                           u'|-----------+-----------|',
                           u'| spam      |   41.9999 |',
                           u'| eggs      |  451      |',])
    result = tabulate(_test_table, _test_table_headers, tablefmt="orgtbl")
    assert_equal(expected, result)


def test_orgtbl_headerless():
    "Output: orgtbl without headers"
    expected = u'\n'.join([u'| spam |  41.9999 |',
                           u'| eggs | 451      |',])
    result = tabulate(_test_table, tablefmt="orgtbl")
    assert_equal(expected, result)


def test_rst():
    "Output: rst with headers"
    expected = u'\n'.join([u'=========  =========',
                           u'strings      numbers',
                           u'=========  =========',
                           u'spam         41.9999',
                           u'eggs        451',
                           u'=========  =========',])
    result = tabulate(_test_table, _test_table_headers, tablefmt="rst")
    assert_equal(expected, result)


def test_rst_headerless():
    "Output: rst without headers"
    expected = u'\n'.join([u'====  ========',
                           u'spam   41.9999',
                           u'eggs  451',
                           u'====  ========',])
    result = tabulate(_test_table, tablefmt="rst")
    assert_equal(expected, result)

def test_mediawiki():
    "Output: mediawiki with headers"
    expected = u'\n'.join([u'{| class="wikitable" style="text-align: left;"',
                           u'|+ <!-- caption -->',
                           u'|-',
                           u'! strings   !! align="right"|   numbers',
                           u'|-',
                           u'| spam      || align="right"|   41.9999',
                           u'|-',
                           u'| eggs      || align="right"|  451',
                           u'|}',])
    result = tabulate(_test_table, _test_table_headers, tablefmt="mediawiki")
    assert_equal(expected, result)


def test_mediawiki_headerless():
    "Output: mediawiki without headers"
    expected = u'\n'.join([u'{| class="wikitable" style="text-align: left;"',
                           u'|+ <!-- caption -->',
                           u'|-',
                           u'| spam || align="right"|  41.9999',
                           u'|-',
                           u'| eggs || align="right"| 451',
                           u'|}',])
    result = tabulate(_test_table, tablefmt="mediawiki")
    assert_equal(expected, result)


def test_latex():
    "Output: latex with headers"
    result   = tabulate(_test_table, _test_table_headers, tablefmt="latex")
    expected = "\n".join([r"\begin{tabular}{lr}",
                          r"\hline",
                          r" strings   &   numbers \\",
                          r"\hline",
                          r" spam      &   41.9999 \\",
                          r" eggs      &  451      \\",
                          r"\hline",
                          r"\end{tabular}"])
    assert_equal(expected, result)


def test_latex_headerless():
    "Output: latex without headers"
    result   = tabulate(_test_table, tablefmt="latex")
    expected = "\n".join([r"\begin{tabular}{lr}",
                          r"\hline",
                          r" spam &  41.9999 \\",
                          r" eggs & 451      \\",
                          r"\hline",
                          r"\end{tabular}"])
    assert_equal(expected, result)


def test_floatfmt():
    "Output: floating point format"
    result = tabulate([['1.23456789'],[1.0]], floatfmt=".3f", tablefmt="plain")
    expected = u'1.235\n1.000'
    assert_equal(expected, result)


def test_missingval():
    "Output: substitution of missing values"
    result = tabulate([['Alice', 10],['Bob', None]], missingval="n/a", tablefmt="plain")
    expected = u'Alice   10\nBob    n/a'
    assert_equal(expected, result)


def test_column_alignment():
    "Output: custom alignment for text and numbers"
    expected = u'\n'.join([u'-----  ---',
                           u'Alice   1',
                           u'  Bob  333',
                           u'-----  ---',])
    result = tabulate([['Alice', 1],['Bob', 333]], stralign="right", numalign="center")
    assert_equal(expected, result)
