"""Pretty-print tabular data."""

__all__ = ["tabulate"]


def _isnumber(string):
    try:
        n = float(string)
        return True
    except ValueError:
        return False


def _afterpoint(string):
    "Symbols after a decimal point."
    if _isnumber(string):
        pos = string.rfind(".")
        if pos >= 0:
            return len(string) - pos - 1
        else:
            return 0  # no point
    else:
        return 0  # not a number


def _format(v, numfmt, isnum):
    "Format value if it is not a string."
    if isinstance(v, basestring) or not isnum or not numfmt:
        return unicode(v)
    else:
        return format(v, numfmt)


def tabulate(list_of_lists, headers=[], colsep=" ", numfmt=None):
    "Format a fixed width table for pretty printing."

    # format rows and columns, convert numeric values to strings
    cols = zip(*list_of_lists)
    isnums = [all(map(_isnumber, c)) for c in cols]
    cols = [[_format(v, numfmt, isnum) for v in c]
            for c, isnum in zip(cols, isnums)]
    rows = zip(*cols)

    # calculate width of every column and decimal point position
    widths = [max(map(len, c)) for c in cols]
    if headers:
        widths = [max(w, len(h)) for w, h in zip(widths, headers)]
    pointpads = [max(map(_afterpoint, c)) for c in cols]

    # add headers if necessary
    lines = []
    if headers:
        ln = []
        for s, width, isnum in zip(headers, widths, isnums):
            if isnum:
                ln.append(("{:>%ds}" % width).format(s))
            else:
                ln.append(("{:<%ds}" % width).format(s))
        lines.append(colsep.join(ln))
        lines.append(colsep.join(['-' * w for w in widths]))

    # format table rows
    for row in rows:
        ln = []
        for s, width, maxpad in zip(row, widths, pointpads):
            if _isnumber(s):
                rpad = " " * (maxpad - _afterpoint(s))
                ln.append(("{:>%ds}" % width).format(s + rpad))
            else:
                ln.append(("{:<%ds}" % width).format(s))
        lines.append(colsep.join(ln))
    return "\n".join(lines)
