"""Command-line interface for tabulate."""

import re
import sys
import textwrap
from functools import partial

try:
    from . import (
        _DEFAULT_FLOATFMT,
        _DEFAULT_INTFMT,
        _is_file,
        tabulate,
        tabulate_formats,
    )
except ImportError:  # pragma: no cover
    # running as a script: python tabulate/cli.py
    import sys as _sys
    import os as _os
    _sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))
    from tabulate import (
        _DEFAULT_FLOATFMT,
        _DEFAULT_INTFMT,
        _is_file,
        tabulate,
        tabulate_formats,
    )


def _main():
    """\
    Usage: tabulate [options] [FILE ...]

    Pretty-print tabular data. Use Python module for more features.

    FILE                      a filename of the file with tabular data;
                              if "-" or missing, read data from stdin.

    Options:

    -h, --help                show this message

    INPUT:
    -r, --read FILEFORMAT     parse input FILEs as:
                              rsv (REGEXP-separated values, default),
                              csv (comma-separated valued, Excel dialect),
                              jsonl (one JSON object per line)
    -s REGEXP, --sep REGEXP   column separator for rsv data (default: whitespace)

    FORMAT:
    --headers HEADERS         HEADERS can be one of:
                              "firstrow" (for csv and rsv data),
                              "keys" (for jsonl data),
                              "HEADER1,HEADER2,..." (for csv and rsv data),
                              "KEY1:HEADER1,KEY2:HEADER2,..." (for jsonl data)
    -1                        use the first row of input data as a table header
                              (the same as --headers firstrow)
    -F FPFMT, --float FPFMT   floating point number format (default: g)
    -I INTFMT, --int INTFMT   integer point number format (default: "")
    -f FMT, --format FMT      set output table format (default: simple)

    Supported output formats: asciidoc, colon_grid, double_grid, double_outline,
    fancy_grid, fancy_outline, github, grid, heavy_grid, heavy_outline, html, jira,
    latex, latex_booktabs, latex_longtable, latex_raw, mediawiki, mixed_grid, mixed_outline,
    moinmoin, orgtbl, outline, pipe, plain, presto, pretty, psql, rounded_grid,
    rounded_outline, rst, simple, simple_grid, simple_outline, textile, tsv, unsafehtml.

    OUTPUT:
    -o FILE, --output FILE    print table to FILE (default: stdout)

    """
    import getopt

    usage = textwrap.dedent(_main.__doc__)
    try:
        opts, args = getopt.getopt(
            sys.argv[1:],
            "h1H:r:o:s:F:I:f:",
            [
                "help",
                "header",  # deprecated in CLI > 0.10
                "headers=", # CLI > 0.10
                "read=",   # CLI > 0.10
                "output=",
                "sep=",
                "float=",
                "int=",
                "colalign=",
                "format=",
            ],
        )
    except getopt.GetoptError as e:
        print(e, file=sys.stderr)
        print(usage)
        sys.exit(2)
    headers = []
    floatfmt = _DEFAULT_FLOATFMT
    intfmt = _DEFAULT_INTFMT
    colalign = None
    tablefmt = "simple"
    fileformat = "rsv"
    sep = r"\s+"
    outfile = "-"
    special_headers_values = ["firstrow", "keys"]
    for opt, value in opts:
        if opt in ["-1", "--header"]:
            # "header" option is for backwards compatibility with CLI <= 0.10
            # CLI >= 0.11 should user --headers
            headers = "firstrow"
        if opt in ["-H", "--headers"]:
            if value in special_headers_values:
                headers = value
            else:
                headers = value  # may need to be processed
        elif opt in ["-o", "--output"]:
            outfile = value
        elif opt in ["-F", "--float"]:
            floatfmt = value
        elif opt in ["-I", "--int"]:
            intfmt = value
        elif opt in ["-C", "--colalign"]:
            colalign = value.split()
        elif opt in ["-r", "--read"]:
            fileformat = value.lower()
        elif opt in ["-f", "--format"]:
            if value not in tabulate_formats:
                print(f"{value} is not a supported output format", file=sys.stderr)
                print(usage)
                sys.exit(3)
            tablefmt = value
        elif opt in ["-s", "--sep"]:
            sep = value
        elif opt in ["-h", "--help"]:
            print(usage)
            sys.exit(0)
    # choose a reader and parse headers option
    if fileformat == "rsv":
        reader = partial(_read_rsv_file, sep=sep)
        if type(headers) is str and headers not in special_headers_values:
            # parse as CSV values
            headers = headers.split(",")
    elif fileformat == "csv":
        reader = _read_csv_file
        if type(headers) is str and headers not in special_headers_values:
            # parse as CSV values
            headers = headers.split(",")
    elif fileformat == "jsonl":
        reader = _read_jsonl_file
        if not headers:
            headers = "keys"  # reasonable default
        if type(headers) is str and headers not in special_headers_values:
            # "," and ":" in header titles are not supported in CLI
            try:
                headers2 = dict(tuple(hh.split(":",2)) for hh in headers.split(","))
            except:
                print(f"cannot parse headers parameter: {headers}", file=sys.stderr)
                headers2 = []
            headers = headers2
    else:
        print(f"{fileformat} is not a supported file format")
        sys.exit(3)
    # format all input files
    files = [sys.stdin] if not args else args
    with sys.stdout if outfile == "-" else open(outfile, "w") as out:
        for f in files:
            if f == "-":
                f = sys.stdin
            _open_and_pprint_file(reader, f,
                    headers=headers,
                    tablefmt=tablefmt,
                    floatfmt=floatfmt,
                    intfmt=intfmt,
                    file=out,
                    colalign=colalign,
                )


def _read_rsv_file(fobject, sep):
    rows = fobject.readlines()
    table = [re.split(sep, r.rstrip()) for r in rows if r.strip()]
    return table


def _read_jsonl_file(fobject):
    import json
    rows:list[str] = fobject.readlines()
    table = [json.loads(row) for row in rows]
    return table


def _read_csv_file(fobject):
    import csv
    reader = csv.reader(fobject, dialect="excel")
    table = [list(row) for row in reader]
    return table


def _open_and_pprint_file(reader, f, *args, **kwargs):
    if _is_file(f):
        _pprint_file(reader, f, *args, **kwargs)
    else:
        with open(f) as fobj:
            _pprint_file(reader, fobj, *args, **kwargs)


def _pprint_file(reader, fobject, headers, tablefmt, floatfmt, intfmt, file, colalign):
    table = reader(fobject)
    print(
        tabulate(
            table,
            headers,
            tablefmt,
            floatfmt=floatfmt,
            intfmt=intfmt,
            colalign=colalign,
        ),
        file=file,
    )


if __name__ == "__main__":  # pragma: no cover
    _main()
