# -*- coding: utf-8 -*-

"""Test output of the various forms of tabular data."""

from __future__ import print_function
from __future__ import unicode_literals
from tabulate import tabulate


def test_latex():
    "Testing Latex output"
    ll = [["a","one",1],["b","two",None]]
    expected = u'0    1      2\n---  ---  ---\na    one    1\nb    two'
    result   = tabulate(ll, headers="keys", tablefmt="latex")
    expected = "\n".join([
        r"\begin{tabular}{rrr}",
        r"\hline",
        r" 0   & 1   &   2 \\",
        r"\hline",
        r" a   & one &   1 \\",
        r" b   & two &     \\",
        r"\hline",
        r"\end{tabular}"])
    print("Expected:\n%s\n" % expected)
    print("Got:\n%s\n" % result)
    assert expected == result
