# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from timeit import timeit
from tabulate import tabulate

setup_code = r"""
from csv import writer
from StringIO import StringIO
from tabulate import tabulate
from prettytable import PrettyTable
from asciitable import write, FixedWidth
from texttable import Texttable

table=[["some text"]+range(i,i+9) for i in range(10)]


def csv_table(table):
    buf = StringIO()
    writer(buf).writerows(table)
    return buf.getvalue()


def join_table(table):
    return "\n".join(("\t".join(map(str,row)) for row in table))


def prettytable(table):
    pp = PrettyTable()
    for row in table:
        pp.add_row(row)
    return str(pp)


def asciitable(table):
    buf = StringIO()
    write(table, output=buf, Writer=FixedWidth)
    return buf.getvalue()


def texttable(table):
    pp = Texttable()
    pp.set_cols_align(["l"] + ["r"]*9)
    pp.add_rows(table)
    return pp.draw()

"""

methods = [("join with tabs and newlines", "join_table(table)"),
           ("csv to StringIO", "csv_table(table)"),
           ("asciitable (0.8)", "asciitable(table)"),
           ("tabulate (0.4.2)", "tabulate(table)"),
           ("PrettyTable (0.7.1)", "prettytable(table)"),
           ("texttable (0.8.1)", "texttable(table)"),
           ]


def benchmark(n):
    results = [(desc, timeit(code, setup_code, number=n)/n * 1e6)
               for desc, code in methods]
    mintime = min(map(lambda x: x[1], results))
    results = [(desc, t, t/mintime) for desc, t in results]
    print tabulate(results, ["Table formatter", "time, μs", "rel. time"], "rst", floatfmt=".1f")


benchmark(1000)
