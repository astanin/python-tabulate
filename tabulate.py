# -*- coding: utf-8 -*-

"""Pretty-print tabular data."""

from __future__ import print_function
from __future__ import unicode_literals
from collections import namedtuple
from platform import python_version_tuple


if python_version_tuple()[0] < "3":
    _none_type = type(None)
    _int_type = int
    _float_type = float
    _text_type = unicode
    _binary_type = str
else:
    from functools import reduce
    _none_type = type(None)
    _int_type = int
    _float_type = float
    _text_type = str
    _binary_type = bytes


__all__ = ["tabulate"]
__version__ = "0.4.4"


Line = namedtuple("Line", ["begin", "hline", "sep", "end"])


DataRow = namedtuple("DataRow", ["begin", "sep", "end"])


TableFormat = namedtuple("TableFormat", ["lineabove", "linebelowheader",
                                         "linebetweenrows", "linebelow",
                                         "datarow", "padding", "usecolons",
                                         "with_header_hide",
                                         "without_header_hide"])


_format_defaults = {"padding": 0,
                    "usecolons": False,
                    "with_header_hide": [],
                    "without_header_hide": []}


_table_formats = {"simple":
                  TableFormat(lineabove=None,
                              linebelowheader=Line("", "-", "  ", ""),
                              linebetweenrows=None,
                              linebelow=Line("", "-", "  ", ""),
                              datarow=DataRow("", "  ", ""),
                              padding=0,
                              usecolons=False,
                              with_header_hide=["linebelow"],
                              without_header_hide=[]),
                  "plain":
                  TableFormat(None, None, None, None,
                              DataRow("", "  ", ""), **_format_defaults),
                  "grid":
                  TableFormat(lineabove=Line("+", "-", "+", "+"),
                              linebelowheader=Line("+", "=", "+", "+"),
                              linebetweenrows=Line("+", "-", "+", "+"),
                              linebelow=Line("+", "-", "+", "+"),
                              datarow=DataRow("|", "|", "|"),
                              padding=1,
                              usecolons=False,
                              with_header_hide=[],
                              without_header_hide=["linebelowheader"]),
                  "pipe":
                  TableFormat(lineabove=None,
                              linebelowheader=Line("|", "-", "|", "|"),
                              linebetweenrows=None,
                              linebelow=None,
                              datarow=DataRow("|", "|", "|"),
                              padding=1,
                              usecolons=True,
                              with_header_hide=[],
                              without_header_hide=[]),
                  "orgtbl":
                  TableFormat(lineabove=None,
                              linebelowheader=Line("|", "-", "+", "|"),
                              linebetweenrows=None,
                              linebelow=None,
                              datarow=DataRow("|", "|", "|"),
                              padding=1,
                              usecolons=False,
                              with_header_hide=[],
                              without_header_hide=["linebelowheader"]),
                  "rst":
                  TableFormat(lineabove=Line("", "=", "  ", ""),
                              linebelowheader=Line("", "=", "  ", ""),
                              linebetweenrows=None,
                              linebelow=Line("", "=", "  ", ""),
                              datarow=DataRow("", "  ", ""),
                              padding=0,
                              usecolons=False,
                              with_header_hide=[],
                              without_header_hide=["linebelowheader"])}

def simple_separated_format(separator):
    """Construct a simple TableFormat with columns separated by a separator.

    >>> tsv = simple_separated_format("\t") ; \
        tabulate([["foo", 1], ["spam", 23]], tablefmt=tsv) == u'foo \\t 1\\nspam\\t23'
    True

    """
    return TableFormat(None, None, None, None,
                       datarow=DataRow('', '\t', ''), **_format_defaults)


def _isconvertible(conv, string):
    try:
        n = conv(string)
        return True
    except ValueError:
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
           (isinstance(string, _binary_type) or isinstance(string, _text_type)) and \
           _isconvertible(int, string)


def _type(string):
    """The least generic type (type(None), int, float, str, unicode).

    >>> _type(None) is type(None)
    True
    >>> _type("foo") is type("")
    True
    >>> _type("1") is type(1)
    True

    """
    if string is None:
        return _none_type
    elif _isint(string):
        return int
    elif _isnumber(string):
        return float
    elif isinstance(string, _binary_type):
        return _binary_type
    else:
        return _text_type


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
    """Flush right.

    >>> _padleft(6, u'\u044f\u0439\u0446\u0430') == u'  \u044f\u0439\u0446\u0430'
    True

    """
    fmt = u"{0:>%ds}" % width
    return fmt.format(s)


def _padright(width, s):
    """Flush left.

    >>> _padright(6, u'\u044f\u0439\u0446\u0430') == u'\u044f\u0439\u0446\u0430  '
    True

    """
    fmt = u"{0:<%ds}" % width
    return fmt.format(s)


def _padboth(width, s):
    """Center string.

    >>> _padboth(6, u'\u044f\u0439\u0446\u0430') == u' \u044f\u0439\u0446\u0430 '
    True

    """
    fmt = u"{0:^%ds}" % width
    return fmt.format(s)


def _align_column(strings, alignment, minwidth=0):
    """[string] -> [padded_string]

    >>> list(map(str,_align_column(["12.345", "-1234.5", "1.23", "1234.5", "1e+234", "1.0e234"], "decimal")))
    ['   12.345  ', '-1234.5    ', '    1.23   ', ' 1234.5    ', '    1e+234 ', '    1.0e234']

    """
    if alignment == "right":
        strings = [s.strip() for s in strings]
        padfn = _padleft
    elif alignment in "center":
        strings = [s.strip() for s in strings]
        padfn = _padboth
    elif alignment in "decimal":
        decimals = [_afterpoint(s) for s in strings]
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
    types = { _none_type: 0, int: 1, float: 2, _text_type: 4 }
    invtypes = { 4: _text_type, 2: float, 1: int, 0: _none_type }
    moregeneric = max(types.get(type1, 4), types.get(type2, 4))
    return invtypes[moregeneric]


def _column_type(strings):
    """The least generic type all column values are convertible to.

    >>> _column_type(["1", "2"]) is _int_type
    True
    >>> _column_type(["1", "2.3"]) is _float_type
    True
    >>> _column_type(["1", "2.3", "four"]) is _text_type
    True
    >>> _column_type(["four", u'\u043f\u044f\u0442\u044c']) is _text_type
    True
    >>> _column_type([None, "brux"]) is _text_type
    True
    >>> _column_type([1, 2, None]) is _int_type
    True

    """
    types = map(_type, strings)
    return reduce(_more_generic, types, int)


def _format(val, valtype, floatfmt, missingval=u""):
    """Format a value accoding to its type.

    Unicode is supported:

    >>> hrow = [u'\u0431\u0443\u043a\u0432\u0430', u'\u0446\u0438\u0444\u0440\u0430'] ; \
        tbl = [[u'\u0430\u0437', 2], [u'\u0431\u0443\u043a\u0438', 4]] ; \
        good_result = u'\\u0431\\u0443\\u043a\\u0432\\u0430      \\u0446\\u0438\\u0444\\u0440\\u0430\\n-------  -------\\n\\u0430\\u0437             2\\n\\u0431\\u0443\\u043a\\u0438           4' ; \
        tabulate(tbl, headers=hrow) == good_result
    True

    """
    if val is None:
        return missingval

    if valtype in [int, _binary_type, _text_type]:
        return u"{0}".format(val)
    elif valtype is float:
        return format(float(val), floatfmt)
    else:
        return u"{0}".format(val)


def _align_header(header, alignment, width):
    if alignment == "left":
        return _padright(width, header)
    elif alignment == "center":
        return _padboth(width, header)
    else:
        return _padleft(width, header)


def tabulate(list_of_lists, headers=[], tablefmt="simple",
             floatfmt="g", numalign="decimal", stralign="left",
             missingval=u""):
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

    `None` values are replaced with a `missingval` string:

    >>> print(tabulate([["spam", 1, None],
    ...                 ["eggs", 42, 3.14],
    ...                 ["other", None, 2.7]], missingval="?"))
    -----  --  ----
    spam    1  ?
    eggs   42  3.14
    other   ?  2.7
    -----  --  ----

    Various plain-text table formats (`tablefmt`) are supported:
    'plain', 'simple', 'grid', 'pipe', and 'orgtbl'.

    "plain" format doesn't use any pseudographics to draw tables,
    it separates columns with a double space:

    >>> print(tabulate([["spam", 41.9999], ["eggs", "451.0"]],
    ...                 ["strings", "numbers"], "plain"))
    strings      numbers
    spam         41.9999
    eggs        451

    >>> print(tabulate([["spam", 41.9999], ["eggs", "451.0"]], tablefmt="plain"))
    spam   41.9999
    eggs  451

    "simple" format is like Pandoc simple_tables:

    >>> print(tabulate([["spam", 41.9999], ["eggs", "451.0"]],
    ...                 ["strings", "numbers"], "simple"))
    strings      numbers
    ---------  ---------
    spam         41.9999
    eggs        451

    >>> print(tabulate([["spam", 41.9999], ["eggs", "451.0"]], tablefmt="simple"))
    ----  --------
    spam   41.9999
    eggs  451
    ----  --------

    "grid" is similar to tables produced by Emacs table.el package or
    Pandoc grid_tables:

    >>> print(tabulate([["spam", 41.9999], ["eggs", "451.0"]],
    ...                ["strings", "numbers"], "grid"))
    +-----------+-----------+
    | strings   |   numbers |
    +===========+===========+
    | spam      |   41.9999 |
    +-----------+-----------+
    | eggs      |  451      |
    +-----------+-----------+

    >>> print(tabulate([["spam", 41.9999], ["eggs", "451.0"]], tablefmt="grid"))
    +------+----------+
    | spam |  41.9999 |
    +------+----------+
    | eggs | 451      |
    +------+----------+

    "pipe" is like tables in PHP Markdown Extra extension or Pandoc
    pipe_tables:

    >>> print(tabulate([["spam", 41.9999], ["eggs", "451.0"]],
    ...                ["strings", "numbers"], "pipe"))
    | strings   |   numbers |
    |:----------|----------:|
    | spam      |   41.9999 |
    | eggs      |  451      |

    >>> print(tabulate([["spam", 41.9999], ["eggs", "451.0"]], tablefmt="pipe"))
    |:-----|---------:|
    | spam |  41.9999 |
    | eggs | 451      |

    "orgtbl" is like tables in Emacs org-mode and orgtbl-mode. They
    are slightly different from "pipe" format by not using colons to
    define column alignment, and using a "+" sign to indicate line
    intersections:

    >>> print(tabulate([["spam", 41.9999], ["eggs", "451.0"]],
    ...                ["strings", "numbers"], "orgtbl"))
    | strings   |   numbers |
    |-----------+-----------|
    | spam      |   41.9999 |
    | eggs      |  451      |


    >>> print(tabulate([["spam", 41.9999], ["eggs", "451.0"]], tablefmt="orgtbl"))
    | spam |  41.9999 |
    | eggs | 451      |

    "rst" is like a simple table format from reStructuredText; please
    note that reStructuredText accepts also "grid" tables:

    >>> print(tabulate([["spam", 41.9999], ["eggs", "451.0"]],
    ...                ["strings", "numbers"], "rst"))
    =========  =========
    strings      numbers
    =========  =========
    spam         41.9999
    eggs        451
    =========  =========

    >>> print(tabulate([["spam", 41.9999], ["eggs", "451.0"]], tablefmt="rst"))
    ====  ========
    spam   41.9999
    eggs  451
    ====  ========

    """
    # format rows and columns, convert numeric values to strings
    cols = list(zip(*list_of_lists))
    coltypes = list(map(_column_type, cols))
    cols = [[_format(v, ct, floatfmt, missingval) for v in c]
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
        rows = list(zip(*cols))
    else:
        minwidths = [len(c[0]) for c in cols]
        rows = list(zip(*cols))

    if not isinstance(tablefmt, TableFormat):
        tablefmt = _table_formats.get(tablefmt, _table_formats["simple"])

    return _format_table(tablefmt, headers, rows, minwidths, aligns)


def _build_row(cells, padding, begin, sep, end):
    "Return a string which represents a row of data cells."
    pad = u" "*padding
    padded_cells = [pad + cell + pad for cell in cells]
    return (begin + sep.join(padded_cells) + end).rstrip()


def _build_line(colwidths, padding, begin, fill, sep,  end):
    "Return a string which represents a horizontal line."
    cells = [fill*(w + 2*padding) for w in colwidths]
    return _build_row(cells, 0, begin, sep, end)


def _line_segment_with_colons(linefmt, align, colwidth):
    """Return a segment of a horizontal line with optional colons which
    indicate column's alignment (as in `pipe` output format)."""
    fill = linefmt.hline
    w = colwidth
    if align in ["right", "decimal"]:
        return (fill[0] * (w - 1)) + ":"
    elif align == "center":
        return ":" + (fill[0] * (w - 2)) + ":"
    elif align == "left":
        return ":" + (fill[0] * (w - 1))
    else:
        return fill[0] * w


def _format_table(fmt, headers, rows, colwidths, colaligns):
    """Produce a plain-text representation of the table."""
    lines = []
    hidden = fmt.with_header_hide if headers else fmt.without_header_hide
    pad = fmt.padding

    if fmt.lineabove and "lineabove" not in hidden:
        lines.append(_build_line(colwidths, pad, *fmt.lineabove))

    if headers:
        lines.append(_build_row(headers, pad, *fmt.datarow))

    if fmt.linebelowheader and "linebelowheader" not in hidden:
        begin, fill, sep, end = fmt.linebelowheader
        if fmt.usecolons:
            segs = [_line_segment_with_colons(fmt.linebelowheader, a, w + 2*pad)
                    for w,a in zip(colwidths, colaligns)]
            lines.append(_build_row(segs, 0, begin, sep, end))
        else:
            lines.append(_build_line(colwidths, pad, *fmt.linebelowheader))

    if rows and fmt.linebetweenrows and "linebetweenrows" not in hidden:
        # initial rows with a line below
        for row in rows[:-1]:
            lines.append(_build_row(row, pad, *fmt.datarow))
            lines.append(_build_line(colwidths, pad, *fmt.linebetweenrows))
        # the last row without a line below
        lines.append(_build_row(rows[-1], pad, *fmt.datarow))
    else:
        for row in rows:
            lines.append(_build_row(row, pad, *fmt.datarow))

    if fmt.linebelow and "linebelow" not in hidden:
        lines.append(_build_line(colwidths, pad, *fmt.linebelow))

    return "\n".join(lines)
