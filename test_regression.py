# -*- coding: utf-8 -*-

"""Regression tests."""

from __future__ import print_function
from __future__ import unicode_literals
from tabulate import tabulate



def test_ansi_color_in_table_cells():
    "ANSI color in table cells (issue #5)."
    colortable = [('test', '\x1b[31mtest\x1b[0m', '\x1b[32mtest\x1b[0m')]
    colorlessheaders = ('test', 'test', 'test')
    formattedtable = tabulate(colortable, colorlessheaders, 'pipe')
    correcttable = u'| test   | test   | test   |\n|:-------|:-------|:-------|\n| test   | \x1b[31mtest\x1b[0m   | \x1b[32mtest\x1b[0m   |'
    print("expected: %r\n\ngot:      %r\n" % (correcttable, formattedtable))
    assert correcttable == formattedtable
