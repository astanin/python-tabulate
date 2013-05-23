# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from timeit import timeit
import tabulate
import asciitable
import prettytable
import texttable

setup_code = r"""
from csv import writer
from StringIO import StringIO
import tabulate
import asciitable
import prettytable
import texttable

table=[["some text"]+range(i,i+9) for i in range(10)]


def csv_table(table):
    buf = StringIO()
    writer(buf).writerows(table)
    return buf.getvalue()


def join_table(table):
    return "\n".join(("\t".join(map(str,row)) for row in table))


def run_prettytable(table):
    pp = prettytable.PrettyTable()
    for row in table:
        pp.add_row(row)
    return str(pp)


def run_asciitable(table):
    buf = StringIO()
    asciitable.write(table, output=buf, Writer=asciitable.FixedWidth)
    return buf.getvalue()


def run_texttable(table):
    pp = texttable.Texttable()
    pp.set_cols_align(["l"] + ["r"]*9)
    pp.add_rows(table)
    return pp.draw()

def run_tabulate(table):
    return tabulate.tabulate(table)

"""

methods = [("join with tabs and newlines", "join_table(table)"),
           ("csv to StringIO", "csv_table(table)"),
           ("asciitable (%s)" % asciitable.__version__, "run_asciitable(table)"),
           ("tabulate (%s)" % tabulate.__version__, "run_tabulate(table)"),
           ("PrettyTable (%s)" % prettytable.__version__, "run_prettytable(table)"),
           ("texttable (%s)" % texttable.__version__, "run_texttable(table)"),
           ]


def benchmark(n):
    results = [(desc, timeit(code, setup_code, number=n)/n * 1e6)
               for desc, code in methods]
    mintime = min(map(lambda x: x[1], results))
    results = [(desc, t, t/mintime) for desc, t in results]
    print tabulate.tabulate(results,
                            ["Table formatter", "time, μs", "rel. time"],
                            "rst", floatfmt=".1f")


benchmark(10000)
