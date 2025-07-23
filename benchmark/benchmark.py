from timeit import timeit
import tabulate
import prettytable
import texttable
import sys

setup_code = r"""
from csv import writer
from io import StringIO
import tabulate
import prettytable
import texttable


table=[["some text"]+list(range(i,i+9)) for i in range(10)]


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


def run_texttable(table):
    pp = texttable.Texttable()
    pp.set_cols_align(["l"] + ["r"]*9)
    pp.add_rows(table)
    return pp.draw()


def run_tabletext(table):
    return tabletext.to_text(table)


def run_tabulate(table, widechars=False):
    tabulate.WIDE_CHARS_MODE = tabulate.wcwidth is not None and widechars
    return tabulate.tabulate(table)


"""

methods = [
    ("join with tabs and newlines", "join_table(table)"),
    ("csv to StringIO", "csv_table(table)"),
    ("tabulate (%s)" % tabulate.__version__, "run_tabulate(table)"),
    (
        "tabulate (%s, WIDE_CHARS_MODE)" % tabulate.__version__,
        "run_tabulate(table, widechars=True)",
    ),
    ("PrettyTable (%s)" % prettytable.__version__, "run_prettytable(table)"),
    ("texttable (%s)" % texttable.__version__, "run_texttable(table)"),
]


if tabulate.wcwidth is None:
    del methods[4]


def benchmark(n):
    global methods
    if "--onlyself" in sys.argv[1:]:
        methods = [m for m in methods if m[0].startswith("tabulate")]

    results = [
        (desc, timeit(code, setup_code, number=n) / n * 1e6) for desc, code in methods
    ]
    mintime = min(map(lambda x: x[1], results))
    results = [
        (desc, t, t / mintime) for desc, t in sorted(results, key=lambda x: x[1])
    ]
    table = tabulate.tabulate(
        results, ["Table formatter", "time, μs", "rel. time"], "rst", floatfmt=".1f"
    )

    print(table)


if __name__ == "__main__":
    if sys.argv[1:]:
        n = int(sys.argv[1])
    else:
        n = 10000
    benchmark(n)
