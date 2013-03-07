"""Pretty-print tabular data."""

from __future__ import print_function

from collections import namedtuple


__all__ = ["tabulate", "TableFormat" ]


TableFormat = namedtuple("TableFormat", ["lineabove", "linebelow",
                                         "headersline", "rowline",
                                         "colsep", "intersect", "edgeintersect",
                                         "rowbegin", "rowend",
                                         "colons_align_columns"])

_table_formats = {"plain":
                  TableFormat(lineabove=None, linebelow=None,
                              headersline=None, rowline=None,
                              colsep="  ", intersect="  ", edgeintersect="  ",
                              rowbegin="", rowend="",
                              colons_align_columns=False),
                  "simple":
                  TableFormat(lineabove=None, linebelow="-",
                              headersline="-", rowline=None,
                              colsep="  ", intersect="  ", edgeintersect="",
                              rowbegin="", rowend="",
                              colons_align_columns=False),
                  "grid":
                  TableFormat(lineabove="-", linebelow="-",
                              headersline="=", rowline="-",
                              colsep="|", intersect="+", edgeintersect="+",
                              rowbegin="|", rowend="|",
                              colons_align_columns=False),
                  "pipe":
                  TableFormat(lineabove=None, linebelow=None,
                              headersline="-", rowline=None,
                              colsep="|", intersect="|", edgeintersect="|",
                              rowbegin="|", rowend="|",
                              colons_align_columns=True),
                  "orgtbl":
                  TableFormat(lineabove=None, linebelow=None,
                              headersline="-", rowline=None,
                              colsep="|", intersect="+", edgeintersect="|",
                              rowbegin="|", rowend="|",
                              colons_align_columns=False) }


def _isconvertible(conv, string):
    try:
        n = conv(string)
        return True
    except ValueError:
        return False
    except UnicodeEncodeError:
        return False


def _isnumber(string):
    """
    >>> _isnumber("123.45")
    True
    >>> _isnumber("123")
    True
    >>> _isnumber("spam")
    False
    """
    return _isconvertible(float, string)


def _isint(string):
    """
    >>> _isint("123")
    True
    >>> _isint("123.45")
    False
    """
    return type(string) is int or \
           isinstance(string, basestring) and  _isconvertible(int, string)


def _type(string):
    "The least generic type (int, float, basestring, unicode)."
    if _isint(string):
        return int
    elif _isnumber(string):
        return float
    elif _isconvertible(str, string):
        return basestring
    else:
        return unicode


def _afterpoint(string):
    """Symbols after a decimal point, -1 if the string lacks the decimal point.

    >>> _afterpoint("123.45")
    2
    >>> _afterpoint("1001")
    -1
    >>> _afterpoint("eggs")
    -1
    >>> _afterpoint("123e45")
    2

    """
    if _isnumber(string):
        if _isint(string):
            return -1
        else:
            pos = string.rfind(".")
            pos = string.lower().rfind("e") if pos < 0 else pos
            if pos >= 0:
                return len(string) - pos - 1
            else:
                return -1  # no point
    else:
        return -1  # not a number


def _padleft(width, s):
    fmt = "{:>%ds}" % width
    return fmt.format(s)


def _padright(width, s):
    fmt = "{:<%ds}" % width
    return fmt.format(s)


def _padboth(width, s):
    fmt = "{:^%ds}" % width
    return fmt.format(s)


def _align_column(strings, alignment, minwidth=0):
    """[string] -> [padded_string]

    >>> _align_column(["12.345", "-1234.5", "1.23", "1234.5", "1e+234", "1.0e234"], "decimal")
    ['   12.345  ', '-1234.5    ', '    1.23   ', ' 1234.5    ', '    1e+234 ', '    1.0e234']

    """
    if alignment == "right":
        strings = [s.strip() for s in strings]
        padfn = _padleft
    elif alignment in "center":
        strings = [s.strip() for s in strings]
        padfn = _padboth
    elif alignment in "decimal":
        decimals = map(_afterpoint, strings)
        maxdecimals = max(decimals)
        strings = [s + (maxdecimals - decs) * " "
                   for s, decs in zip(strings, decimals)]
        padfn = _padleft
    else:
        strings = [s.strip() for s in strings]
        padfn = _padright
    maxwidth = max(max(map(len, strings)), minwidth)
    return [padfn(maxwidth, s) for s in strings]


def _more_generic(type1, type2):
    types = { int: 1, float: 2, basestring: 3, unicode: 4 }
    invtypes = { 4: unicode, 3: basestring, 2: float, 1: int }
    moregeneric = max(types[type1], types[type2])
    return invtypes[moregeneric]


def _column_type(strings):
    """The least generic type all column values are convertible to.

    >>> _column_type(["1", "2"])
    <type 'int'>
    >>> _column_type(["1", "2.3"])
    <type 'float'>
    >>> _column_type(["1", "2.3", "four"])
    <type 'basestring'>
    >>> _column_type(["four", u'\u043f\u044f\u0442\u044c'])
    <type 'unicode'>

    """
    types = map(_type, strings)
    return reduce(_more_generic, types, int)


def _format(val, valtype, floatfmt):
    if valtype in [int, str, basestring]:
        return "{}".format(val)
    elif valtype is float:
        return format(float(val), floatfmt)
    else:
        return u"{}".format(val)


def _align_header(header, alignment, width):
    if alignment == "left":
        return _padright(width, header)
    elif alignment == "center":
        return _padboth(width, header)
    else:
        return _padleft(width, header)


def tabulate(list_of_lists, headers=[], tablefmt="simple",
             floatfmt="g", numalign="decimal", stralign="left"):
    """Format a fixed width table for pretty printing.

    >>> print(tabulate([[1, 2.34], [-56, "8.999"], ["2", "10001"]]))
    ---  ---------
      1      2.34
    -56      8.999
      2  10001
    ---  ---------

    If headers is not empty, it is used as a list of column names
    to print a nice header. Otherwise a headerless table is produced.

    `tabulate` tries to detect column types automatically, and aligns
    the values properly. By default it aligns decimal points of the
    numbers (or flushes integer numbers to the right), and flushes
    everything else to the left. Possible column alignments
    (`numalign`, `stralign`) are: right, center, left, decimal (only
    for `numalign`).

    `floatfmt` is a format specification used for columns which
    contain numeric data with a decimal point.

    Various plain-text table formats (`tablefmt`) are supported:
    'plain', 'simple', 'grid', 'pipe', and 'orgtbl'.

    "plain" format doesn't use any pseudographics to draw tables,
    it separates columns with a double space:

    >>> print(tabulate([["spam", 41.9999], ["eggs", "451.0"]],
    ...                 ["strings", "numbers"], "plain"))
    strings      numbers
    spam         41.9999
    eggs        451

    "simple" format is like Pandoc's simple_tables:

    >>> print(tabulate([["spam", 41.9999], ["eggs", "451.0"]],
    ...                 ["strings", "numbers"], "simple"))
    strings      numbers
    ---------  ---------
    spam         41.9999
    eggs        451
    ---------  ---------

    "grid" is similar to Emacs' table.el tables or Padoc's grid_tables:

    >>> print(tabulate([["spam", 41.9999], ["eggs", "451.0"]],
    ...                ["strings", "numbers"], "grid"))
    +---------+---------+
    |strings  |  numbers|
    +=========+=========+
    |spam     |  41.9999|
    +---------+---------+
    |eggs     | 451     |
    +---------+---------+

    "pipe" is like PHP Markdown Extra or Pandoc's pipe_tables:

    >>> print(tabulate([["spam", 41.9999], ["eggs", "451.0"]],
    ...                ["strings", "numbers"], "pipe"))
    |strings  |  numbers|
    |:--------|--------:|
    |spam     |  41.9999|
    |eggs     | 451     |

    "orgtbl" is like tables in Emacs orgtbl-mode. It is slightly
    different from"pipe" format by not using colons to define column alignment,
    and using a "+" sign to indicate line intersections:

    >>> print(tabulate([["spam", 41.9999], ["eggs", "451.0"]],
    ...                ["strings", "numbers"], "orgtbl"))
    |strings  |  numbers|
    |---------+---------|
    |spam     |  41.9999|
    |eggs     | 451     |

    """
    # format rows and columns, convert numeric values to strings
    cols = zip(*list_of_lists)
    coltypes = map(_column_type, cols)
    cols = [[_format(v, ct, floatfmt) for v in c]
             for c,ct in zip(cols, coltypes)]

    # align columns
    aligns = [numalign if ct in [int,float] else stralign for ct in coltypes]
    minwidths = [len(h) + 2 for h in headers] if headers else [0]*len(cols)
    cols = [_align_column(c, a, minw)
            for c, a, minw in zip(cols, aligns, minwidths)]

    if headers:
        # align headers and add headers
        minwidths = [max(minw, len(c[0])) for minw, c in zip(minwidths, cols)]
        headers = [_align_header(h, a, minw)
                   for h, a, minw in zip(headers, aligns, minwidths)]
        rows = zip(*cols)
    else:
        minwidths = [len(c[0]) for c in cols]
        rows = zip(*cols)

    tablefmt = _table_formats.get(tablefmt, _table_formats["simple"])
    return _format_table(tablefmt, headers, rows, minwidths, aligns)


def _format_table(fmt, headers, rows, colwidths, colaligns):
    """Produce a plain-text representation of the table."""
    lines = []

    def build_line(cells, sep, begin="", end=""):
        return (begin + sep.join(cells) + end).rstrip()

    def fill_cells(fill):
        cells = [fill*w for w in colwidths]
        return cells

    def fill_cell_with_colons(fill, align, colwidth):
        if align in ["right", "decimal"]:
            return (fill * (colwidth - 1)) + ":"
        elif align == "center":
            return ":" + (fill * (colwidth - 2)) + ":"
        elif align == "left":
            return ":" + (fill * (colwidth - 1))
        else:
            return fill * colwidth

    if fmt.lineabove:
        lines.append(build_line(fill_cells(fmt.lineabove), fmt.intersect,
                                fmt.edgeintersect, fmt.edgeintersect))

    if headers:
        lines.append(build_line(headers, fmt.colsep, fmt.rowbegin, fmt.rowend))

    if fmt.headersline:
        fill = fmt.headersline
        if fmt.colons_align_columns:
            cells = [fill_cell_with_colons(fill, a, w)
                     for w, a in zip(colwidths, colaligns)]
        else:
            cells = fill_cells(fill)
        lines.append(build_line(cells, fmt.intersect,
                                fmt.edgeintersect, fmt.edgeintersect))

    if rows and fmt.rowline:  # with lines between rows
        # initial rows with a lines below
        for row in rows[:-1]:
            lines.append(build_line(row, fmt.colsep, fmt.rowbegin, fmt.rowend))
            lines.append(build_line(fill_cells(fmt.rowline), fmt.intersect,
                                    fmt.edgeintersect, fmt.edgeintersect))
        # the last row without a line below
        lines.append(build_line(rows[-1], fmt.colsep, fmt.rowbegin, fmt.rowend))
    else:  # no lines between rows of data
        for row in rows:
            lines.append(build_line(row, fmt.colsep, fmt.rowbegin, fmt.rowend))

    if fmt.linebelow:
        lines.append(build_line(fill_cells(fmt.linebelow), fmt.intersect,
                                fmt.edgeintersect, fmt.edgeintersect))

    return "\n".join(lines)
