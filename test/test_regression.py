# -*- coding: utf-8 -*-

"""Regression tests."""

from __future__ import print_function
from __future__ import unicode_literals
from tabulate import tabulate



def test_ansi_color_in_table_cells():
    "Regression: ANSI color in table cells (issue #5)."
    colortable = [('test', '\x1b[31mtest\x1b[0m', '\x1b[32mtest\x1b[0m')]
    colorlessheaders = ('test', 'test', 'test')
    formatted = tabulate(colortable, colorlessheaders, 'pipe')
    expected = u"\n".join([u'| test   | test   | test   |',
                           u'|:-------|:-------|:-------|',
                           u'| test   | \x1b[31mtest\x1b[0m   | \x1b[32mtest\x1b[0m   |'])
    print("expected: %r\n\ngot:      %r\n" % (expected, formatted))
    assert expected == formatted


def test_alignment_of_colored_cells():
    "Regression: Align ANSI-colored values as if they were colorless."
    colortable = [('test', 42, '\x1b[31m42\x1b[0m'), ('test', 101, '\x1b[32m101\x1b[0m')]
    colorheaders = ('test', '\x1b[34mtest\x1b[0m', 'test')
    formatted = tabulate(colortable, colorheaders, 'grid')
    expected = u'\n'.join([u'+--------+--------+--------+',
                           u'| test   |   \x1b[34mtest\x1b[0m |   test |',
                           u'+========+========+========+',
                           u'| test   |     42 |     \x1b[31m42\x1b[0m |',
                           u'+--------+--------+--------+',
                           u'| test   |    101 |    \x1b[32m101\x1b[0m |',
                           u'+--------+--------+--------+'])
    print("expected: %r\n\ngot:      %r\n" % (expected, formatted))
    assert expected == formatted


def test_iter_of_iters_with_headers():
    "Regression: Generator of generators with a generator of headers (issue #9)."

    def mk_iter_of_iters():
        def mk_iter():
            for i in range(3):
                yield i
        for r in range(3):
            yield mk_iter()

    def mk_headers():
        for h in ["a", "b", "c"]:
            yield h

    formatted = tabulate(mk_iter_of_iters(), headers=mk_headers())
    expected = u'\n'.join([u'  a    b    c',
                           u'---  ---  ---',
                           u'  0    1    2',
                           u'  0    1    2',
                           u'  0    1    2'])
    print("expected: %r\n\ngot:      %r\n" % (expected, formatted))
    assert expected == formatted


def test_datetime_values():
    "Regression: datetime, date, and time values in cells (issue #10)."
    import datetime
    dt = datetime.datetime(1991,2,19,17,35,26)
    d = datetime.date(1991,2,19)
    t = datetime.time(17,35,26)
    formatted = tabulate([[dt, d, t]])
    expected = u'\n'.join([u'-------------------  ----------  --------',
                           u'1991-02-19 17:35:26  1991-02-19  17:35:26',
                           u'-------------------  ----------  --------'])
    print("expected: %r\n\ngot:      %r\n" % (expected, formatted))
    assert expected == formatted


def test_simple_separated_format():
    "Regression: simple_separated_format() accepts any separator (issue #12)"
    from tabulate import simple_separated_format
    fmt = simple_separated_format(u"!")
    expected = u'spam!eggs'
    formatted = tabulate([[u"spam", u"eggs"]], tablefmt=fmt)
    print("expected: %r\n\ngot:      %r\n" % (expected, formatted))
    assert expected == formatted
