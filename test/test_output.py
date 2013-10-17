# -*- coding: utf-8 -*-

"""Test output of the various forms of tabular data."""

from __future__ import print_function
from __future__ import unicode_literals
from tabulate import tabulate


def test_latex():
    "Output: LaTeX with headers"
    ll = [["a","one",1],["b","two",None]]
    result   = tabulate(ll, headers="keys", tablefmt="latex")
    expected = "\n".join([
        r"\begin{tabular}{llr}",
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


def test_latex_headerless():
    "Output: LaTeX without headers"
    tbl = [["spam", 1.23],["eggs", 45.6]]
    result   = tabulate(tbl, tablefmt="latex")
    expected = "\n".join([
        r"\begin{tabular}{lr}",
        r"\hline",
        r" spam &  1.23 \\",
        r" eggs & 45.6  \\",
        r"\hline",
        r"\end{tabular}"])
    print("Expected:\n%s\n" % expected)
    print("Got:\n%s\n" % result)
    assert expected == result
