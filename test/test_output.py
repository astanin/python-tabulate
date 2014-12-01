# -*- coding: utf-8 -*-

"""Test output of the various forms of tabular data."""

from __future__ import print_function
from __future__ import unicode_literals
from tabulate import tabulate, simple_separated_format
from common import assert_equal


# _test_table shows
#  - coercion of a string to a number,
#  - left alignment of text,
#  - decimal point alignment of numbers
_test_table = [["spam", 41.9999], ["eggs", "451.0"]]
_test_table_headers = ["strings", "numbers"]


def test_plain():
    "Output: plain with headers"
    expected = "\n".join(['strings      numbers',
                          'spam         41.9999',
                          'eggs        451',])
    result = tabulate(_test_table, _test_table_headers, tablefmt="plain")
    assert_equal(expected, result)


def test_plain_headerless():
    "Output: plain without headers"
    expected = "\n".join(['spam   41.9999',
                          'eggs  451',])
    result = tabulate(_test_table, tablefmt="plain")
    assert_equal(expected, result)


def test_simple():
    "Output: simple with headers"
    expected = "\n".join(['strings      numbers',
                          '---------  ---------',
                          'spam         41.9999',
                          'eggs        451',])
    result = tabulate(_test_table, _test_table_headers, tablefmt="simple")
    assert_equal(expected, result)


def test_simple_headerless():
    "Output: simple without headers"
    expected = "\n".join(['----  --------',
                          'spam   41.9999',
                          'eggs  451',
                          '----  --------',])
    result = tabulate(_test_table, tablefmt="simple")
    assert_equal(expected, result)


def test_grid():
    "Output: grid with headers"
    expected = '\n'.join(['+-----------+-----------+',
                          '| strings   |   numbers |',
                          '+===========+===========+',
                           '| spam      |   41.9999 |',
                          '+-----------+-----------+',
                           '| eggs      |  451      |',
                          '+-----------+-----------+',])
    result = tabulate(_test_table, _test_table_headers, tablefmt="grid")
    assert_equal(expected, result)


def test_grid_headerless():
    "Output: grid without headers"
    expected = '\n'.join(['+------+----------+',
                          '| spam |  41.9999 |',
                          '+------+----------+',
                          '| eggs | 451      |',
                          '+------+----------+',])
    result = tabulate(_test_table, tablefmt="grid")
    assert_equal(expected, result)


def test_fancy_grid():
    "Output: fancy_grid with headers"
    expected = '\n'.join([
        '╒═══════════╤═══════════╕',
        '│ strings   │   numbers │',
        '╞═══════════╪═══════════╡',
        '│ spam      │   41.9999 │',
        '├───────────┼───────────┤',
        '│ eggs      │  451      │',
        '╘═══════════╧═══════════╛',])
    result = tabulate(_test_table, _test_table_headers, tablefmt="fancy_grid")
    assert_equal(expected, result)


def test_fancy_grid_headerless():
    "Output: fancy_grid without headers"
    expected = '\n'.join([
        '╒══════╤══════════╕',
        '│ spam │  41.9999 │',
        '├──────┼──────────┤',
        '│ eggs │ 451      │',
        '╘══════╧══════════╛',])
    result = tabulate(_test_table, tablefmt="fancy_grid")
    assert_equal(expected, result)


def test_pipe():
    "Output: pipe with headers"
    expected = '\n'.join(['| strings   |   numbers |',
                          '|:----------|----------:|',
                          '| spam      |   41.9999 |',
                          '| eggs      |  451      |',])
    result = tabulate(_test_table, _test_table_headers, tablefmt="pipe")
    assert_equal(expected, result)


def test_pipe_headerless():
    "Output: pipe without headers"
    expected = '\n'.join(['|:-----|---------:|',
                          '| spam |  41.9999 |',
                          '| eggs | 451      |',])
    result = tabulate(_test_table, tablefmt="pipe")
    assert_equal(expected, result)


def test_orgtbl():
    "Output: orgtbl with headers"
    expected = '\n'.join(['| strings   |   numbers |',
                          '|-----------+-----------|',
                          '| spam      |   41.9999 |',
                          '| eggs      |  451      |',])
    result = tabulate(_test_table, _test_table_headers, tablefmt="orgtbl")
    assert_equal(expected, result)


def test_orgtbl_headerless():
    "Output: orgtbl without headers"
    expected = '\n'.join(['| spam |  41.9999 |',
                          '| eggs | 451      |',])
    result = tabulate(_test_table, tablefmt="orgtbl")
    assert_equal(expected, result)

def test_psql():
    "Output: psql with headers"
    expected = '\n'.join(['+-----------+-----------+',
                          '| strings   |   numbers |',
                          '|-----------+-----------|',
                          '| spam      |   41.9999 |',
                          '| eggs      |  451      |',
                          '+-----------+-----------+',])
    result = tabulate(_test_table, _test_table_headers, tablefmt="psql")
    assert_equal(expected, result)

def test_psql_headerless():
    "Output: psql without headers"
    expected = '\n'.join(['+------+----------+',
                          '| spam |  41.9999 |',
                          '| eggs | 451      |',
                          '+------+----------+',])
    result = tabulate(_test_table, tablefmt="psql")
    assert_equal(expected, result)

def test_rst():
    "Output: rst with headers"
    expected = '\n'.join(['=========  =========',
                          'strings      numbers',
                          '=========  =========',
                          'spam         41.9999',
                          'eggs        451',
                          '=========  =========',])
    result = tabulate(_test_table, _test_table_headers, tablefmt="rst")
    assert_equal(expected, result)


def test_rst_headerless():
    "Output: rst without headers"
    expected = '\n'.join(['====  ========',
                          'spam   41.9999',
                          'eggs  451',
                          '====  ========',])
    result = tabulate(_test_table, tablefmt="rst")
    assert_equal(expected, result)

def test_mediawiki():
    "Output: mediawiki with headers"
    expected = '\n'.join(['{| class="wikitable" style="text-align: left;"',
                          '|+ <!-- caption -->',
                          '|-',
                          '! strings   !! align="right"|   numbers',
                          '|-',
                          '| spam      || align="right"|   41.9999',
                          '|-',
                          '| eggs      || align="right"|  451',
                          '|}',])
    result = tabulate(_test_table, _test_table_headers, tablefmt="mediawiki")
    assert_equal(expected, result)


def test_mediawiki_headerless():
    "Output: mediawiki without headers"
    expected = '\n'.join(['{| class="wikitable" style="text-align: left;"',
                          '|+ <!-- caption -->',
                          '|-',
                          '| spam || align="right"|  41.9999',
                          '|-',
                          '| eggs || align="right"| 451',
                          '|}',])
    result = tabulate(_test_table, tablefmt="mediawiki")
    assert_equal(expected, result)


def test_html():
    "Output: html with headers"
    expected = '\n'.join([
        '<table>',
        '<tr><th>strings  </th><th style="text-align: right;">  numbers</th></tr>',
        '<tr><td>spam     </td><td style="text-align: right;">  41.9999</td></tr>',
        '<tr><td>eggs     </td><td style="text-align: right;"> 451     </td></tr>',
        '</table>',])
    result = tabulate(_test_table, _test_table_headers, tablefmt="html")
    assert_equal(expected, result)


def test_html_headerless():
    "Output: html without headers"
    expected = '\n'.join([
        '<table>',
        '<tr><td>spam</td><td style="text-align: right;"> 41.9999</td></tr>',
        '<tr><td>eggs</td><td style="text-align: right;">451     </td></tr>',
        '</table>',])
    result = tabulate(_test_table, tablefmt="html")
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

def test_latex_booktabs():
    "Output: latex with headers, using the booktabs format"
    result   = tabulate(_test_table, _test_table_headers, tablefmt="latex_booktabs")
    expected = "\n".join([r"\begin{tabular}{lr}",
                          r"\toprule",
                          r" strings   &   numbers \\",
                          r"\midrule",
                          r" spam      &   41.9999 \\",
                          r" eggs      &  451      \\",
                          r"\bottomrule",
                          r"\end{tabular}"])
    assert_equal(expected, result)


def test_latex_booktabs_headerless():
    "Output: latex without headers, using the booktabs format"
    result   = tabulate(_test_table, tablefmt="latex_booktabs")
    expected = "\n".join([r"\begin{tabular}{lr}",
                          r"\toprule",
                          r" spam &  41.9999 \\",
                          r" eggs & 451      \\",
                          r"\bottomrule",
                          r"\end{tabular}"])
    assert_equal(expected, result)


def test_no_data():
    "Output: table with no data"
    expected = "\n".join(['strings    numbers',
                          '---------  ---------'])
    result = tabulate(None, _test_table_headers, tablefmt="simple")
    assert_equal(expected, result)


def test_empty_data():
    "Output: table with empty data"
    expected = "\n".join(['strings    numbers',
                          '---------  ---------'])
    result = tabulate([], _test_table_headers, tablefmt="simple")
    assert_equal(expected, result)


def test_no_data_without_headers():
    "Output: table with no data and no headers"
    expected = "\n"
    result = tabulate(None, tablefmt="simple")
    assert_equal(expected, result)


def test_empty_data_without_headers():
    "Output: table with empty data and no headers"
    expected = "\n"
    result = tabulate([], tablefmt="simple")
    assert_equal(expected, result)


def test_floatfmt():
    "Output: floating point format"
    result = tabulate([['1.23456789'],[1.0]], floatfmt=".3f", tablefmt="plain")
    expected = '1.235\n1.000'
    assert_equal(expected, result)


def test_missingval():
    "Output: substitution of missing values"
    result = tabulate([['Alice', 10],['Bob', None]], missingval="n/a", tablefmt="plain")
    expected = 'Alice   10\nBob    n/a'
    assert_equal(expected, result)


def test_column_alignment():
    "Output: custom alignment for text and numbers"
    expected = '\n'.join(['-----  ---',
                          'Alice   1',
                          '  Bob  333',
                          '-----  ---',])
    result = tabulate([['Alice', 1],['Bob', 333]], stralign="right", numalign="center")
    assert_equal(expected, result)


def test_unaligned_separated():
    "Output: non-aligned data columns"
    expected = '\n'.join(['name|score',
                          'Alice|1',
                          'Bob|333'])
    fmt = simple_separated_format("|")
    result = tabulate([['Alice', 1],['Bob', 333]],
                      ["name", "score"],
                      tablefmt=fmt, stralign=None, numalign=None)
    assert_equal(expected, result)

