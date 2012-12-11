"""Pretty-print tabular data."""

from __future__ import print_function


__all__ = ["tabulate", "ALIGN_LEFT", "ALIGN_RIGHT",
           "ALIGN_CENTER", "ALIGN_DECIMAL"]


ALIGN_LEFT, ALIGN_RIGHT, ALIGN_CENTER, ALIGN_DECIMAL = range(4)


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
    if alignment in [ALIGN_RIGHT, "right"]:
        strings = [s.strip() for s in strings]
        padfn = _padleft
    elif alignment in [ALIGN_CENTER, "center"]:
        strings = [s.strip() for s in strings]
        padfn = _padboth
    elif alignment in [ALIGN_DECIMAL, "decimal"]:
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
    if alignment in [ALIGN_LEFT, "left"]:
        return _padright(width, header)
    elif alignment in [ALIGN_CENTER, "center"]:
        return _padboth(width, header)
    else:
        return _padleft(width, header)


def tabulate(list_of_lists, headers=[], colsep="  ",
             floatfmt="g", numalign="decimal", stralign="left"):
    """Format a fixed width table for pretty printing.

    >>> print(tabulate([[1, 2.34], [-56.7, "8.999"], ["2", "10001"]]))
      1        2.34
    -56.7      8.999
      2    10001

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
        hlines = ["-" * minw for minw in minwidths]
        rows = [headers, hlines] + zip(*cols)
    else:
        rows = zip(*cols)

    lines = [colsep.join(r).rstrip() for r in rows]
    return "\n".join(lines)
