python-tabulate
===============

Pretty-print tabular data in Python, a library and a command-line
utility.

The main use cases of the library are:

-   printing small tables without hassle: just one function call,
    formatting is guided by the data itself
-   authoring tabular data for lightweight plain-text markup: multiple
    output formats suitable for further editing or transformation
-   readable presentation of mixed textual and numeric data: smart
    column alignment, configurable number formatting, alignment by a
    decimal point

Installation
------------

To install the Python library and the command line utility, run:

```shell
pip install tabulate
```

The command line utility will be installed as `tabulate` to `bin` on
Linux (e.g. `/usr/bin`); or as `tabulate.exe` to `Scripts` in your
Python installation on Windows (e.g. `C:\Python39\Scripts\tabulate.exe`).

You may consider installing the library only for the current user:

```shell
pip install tabulate --user
```

In this case the command line utility will be installed to
`~/.local/bin/tabulate` on Linux and to
`%APPDATA%\Python\Scripts\tabulate.exe` on Windows.

To install just the library on Unix-like operating systems:

```shell
TABULATE_INSTALL=lib-only pip install tabulate
```

On Windows:

```shell
set TABULATE_INSTALL=lib-only
pip install tabulate
```

Build status
------------

[![python-tabulate](https://github.com/astanin/python-tabulate/actions/workflows/tabulate.yml/badge.svg)](https://github.com/astanin/python-tabulate/actions/workflows/tabulate.yml)

Library usage
-------------

The module provides just one function, `tabulate`, which takes a list of
lists or another tabular data type as the first argument, and outputs a
nicely formatted plain-text table:

```pycon
>>> from tabulate import tabulate

>>> table = [["Sun",696000,1989100000],["Earth",6371,5973.6],
...          ["Moon",1737,73.5],["Mars",3390,641.85]]
>>> print(tabulate(table))
-----  ------  -------------
Sun    696000     1.9891e+09
Earth    6371  5973.6
Moon     1737    73.5
Mars     3390   641.85
-----  ------  -------------

```

The following tabular data types are supported:

-   list of lists or another iterable of iterables
-   list or another iterable of dicts (keys as columns)
-   dict of iterables (keys as columns)
-   list of dataclasses (field names as columns)
-   two-dimensional NumPy array
-   NumPy record arrays (names as columns)
-   pandas.DataFrame

Tabulate is a Python3 library.

### Headers

The second optional argument named `headers` defines a list of column
headers to be used:

```pycon
>>> print(tabulate(table, headers=["Planet","R (km)", "mass (x 10^29 kg)"]))
Planet      R (km)    mass (x 10^29 kg)
--------  --------  -------------------
Sun         696000           1.9891e+09
Earth         6371        5973.6
Moon          1737          73.5
Mars          3390         641.85

```

If `headers="firstrow"`, then the first row of data is used:

```pycon
>>> print(tabulate([["Name","Age"],["Alice",24],["Bob",19]],
...                headers="firstrow"))
Name      Age
------  -----
Alice      24
Bob        19

```

If `headers="keys"`, then the keys of a dictionary/dataframe, or column
indices are used. It also works for NumPy record arrays and lists of
dictionaries or named tuples:

```pycon
>>> print(tabulate({"Name": ["Alice", "Bob"],
...                 "Age": [24, 19]}, headers="keys"))
Name      Age
------  -----
Alice      24
Bob        19

```

When data is a list of dictionaries, a dictionary can be passed as `headers`
to replace the keys with other column labels:

```pycon
>>> print(tabulate([{1: "Alice", 2: 24}, {1: "Bob", 2: 19}],
...                headers={1: "Name", 2: "Age"}))
Name      Age
------  -----
Alice      24
Bob        19

```

### Row Indices

By default, only pandas.DataFrame tables have an additional column
called row index. To add a similar column to any other type of table,
pass `showindex="always"` or `showindex=True` argument to `tabulate()`.
To suppress row indices for all types of data, pass `showindex="never"`
or `showindex=False`. To add a custom row index column, pass
`showindex=rowIDs`, where `rowIDs` is some iterable:

```pycon
>>> print(tabulate([["F",24],["M",19]], showindex="always"))
-  -  --
0  F  24
1  M  19
-  -  --

```

### Table format

There is more than one way to format a table in plain text. The third
optional argument named `tablefmt` defines how the table is formatted.

Supported table formats are:

-   "plain"
-   "simple"
-   "github"
-   "grid"
-   "simple\_grid"
-   "rounded\_grid"
-   "heavy\_grid"
-   "mixed\_grid"
-   "double\_grid"
-   "fancy\_grid"
-   "outline"
-   "simple\_outline"
-   "rounded\_outline"
-   "heavy\_outline"
-   "mixed\_outline"
-   "double\_outline"
-   "fancy\_outline"
-   "pipe"
-   "orgtbl"
-   "asciidoc"
-   "jira"
-   "presto"
-   "pretty"
-   "psql"
-   "rst"
-   "mediawiki"
-   "moinmoin"
-   "youtrack"
-   "html"
-   "unsafehtml"
-   "latex"
-   "latex\_raw"
-   "latex\_booktabs"
-   "latex\_longtable"
-   "textile"
-   "tsv"

`plain` tables do not use any pseudo-graphics to draw lines:

```pycon
>>> table = [["spam",42],["eggs",451],["bacon",0]]
>>> headers = ["item", "qty"]
>>> print(tabulate(table, headers, tablefmt="plain"))
item      qty
spam       42
eggs      451
bacon       0

```

`simple` is the default format (the default may change in future
versions). It corresponds to `simple_tables` in [Pandoc Markdown
extensions](http://johnmacfarlane.net/pandoc/README.html#tables):

```pycon
>>> print(tabulate(table, headers, tablefmt="simple"))
item      qty
------  -----
spam       42
eggs      451
bacon       0

```

`github` follows the conventions of GitHub flavored Markdown. It
corresponds to the `pipe` format without alignment colons:

```pycon
>>> print(tabulate(table, headers, tablefmt="github"))
| item   |   qty |
|--------|-------|
| spam   |    42 |
| eggs   |   451 |
| bacon  |     0 |

```

`grid` is like tables formatted by Emacs'
[table.el](http://table.sourceforge.net/) package. It corresponds to
`grid_tables` in Pandoc Markdown extensions:

```pycon
>>> print(tabulate(table, headers, tablefmt="grid"))
+--------+-------+
| item   |   qty |
+========+=======+
| spam   |    42 |
+--------+-------+
| eggs   |   451 |
+--------+-------+
| bacon  |     0 |
+--------+-------+

```

`simple_grid` draws a grid using single-line box-drawing characters:

    >>> print(tabulate(table, headers, tablefmt="simple_grid"))
    ┌────────┬───────┐
    │ item   │   qty │
    ├────────┼───────┤
    │ spam   │    42 │
    ├────────┼───────┤
    │ eggs   │   451 │
    ├────────┼───────┤
    │ bacon  │     0 │
    └────────┴───────┘

`rounded_grid` draws a grid using single-line box-drawing characters with rounded corners:

    >>> print(tabulate(table, headers, tablefmt="rounded_grid"))
    ╭────────┬───────╮
    │ item   │   qty │
    ├────────┼───────┤
    │ spam   │    42 │
    ├────────┼───────┤
    │ eggs   │   451 │
    ├────────┼───────┤
    │ bacon  │     0 │
    ╰────────┴───────╯

`heavy_grid` draws a grid using bold (thick) single-line box-drawing characters:

    >>> print(tabulate(table, headers, tablefmt="heavy_grid"))
    ┏━━━━━━━━┳━━━━━━━┓
    ┃ item   ┃   qty ┃
    ┣━━━━━━━━╋━━━━━━━┫
    ┃ spam   ┃    42 ┃
    ┣━━━━━━━━╋━━━━━━━┫
    ┃ eggs   ┃   451 ┃
    ┣━━━━━━━━╋━━━━━━━┫
    ┃ bacon  ┃     0 ┃
    ┗━━━━━━━━┻━━━━━━━┛

`mixed_grid` draws a grid using a mix of light (thin) and heavy (thick) lines box-drawing characters:

    >>> print(tabulate(table, headers, tablefmt="mixed_grid"))
    ┍━━━━━━━━┯━━━━━━━┑
    │ item   │   qty │
    ┝━━━━━━━━┿━━━━━━━┥
    │ spam   │    42 │
    ├────────┼───────┤
    │ eggs   │   451 │
    ├────────┼───────┤
    │ bacon  │     0 │
    ┕━━━━━━━━┷━━━━━━━┙

`double_grid` draws a grid using double-line box-drawing characters:

    >>> print(tabulate(table, headers, tablefmt="double_grid"))
    ╔════════╦═══════╗
    ║ item   ║   qty ║
    ╠════════╬═══════╣
    ║ spam   ║    42 ║
    ╠════════╬═══════╣
    ║ eggs   ║   451 ║
    ╠════════╬═══════╣
    ║ bacon  ║     0 ║
    ╚════════╩═══════╝

`fancy_grid` draws a grid using a mix of single and
    double-line box-drawing characters:

```pycon
>>> print(tabulate(table, headers, tablefmt="fancy_grid"))
╒════════╤═══════╕
│ item   │   qty │
╞════════╪═══════╡
│ spam   │    42 │
├────────┼───────┤
│ eggs   │   451 │
├────────┼───────┤
│ bacon  │     0 │
╘════════╧═══════╛

```

`colon_grid` is similar to `grid` but uses colons only to define
columnwise content alignment , without whitespace padding,
similar the alignment specification of Pandoc `grid_tables`:

    >>> print(tabulate([["spam", 41.9999], ["eggs", "451.0"]],
    ...                ["strings", "numbers"], "colon_grid",
    ...                colalign=["right", "left"]))
    +-----------+-----------+
    | strings   | numbers   |
    +==========:+:==========+
    | spam      | 41.9999   |
    +-----------+-----------+
    | eggs      | 451       |
    +-----------+-----------+


`outline` is the same as the `grid` format but doesn't draw lines between rows:

    >>> print(tabulate(table, headers, tablefmt="outline"))
    +--------+-------+
    | item   |   qty |
    +========+=======+
    | spam   |    42 |
    | eggs   |   451 |
    | bacon  |     0 |
    +--------+-------+

`simple_outline` is the same as the `simple_grid` format but doesn't draw lines between rows:

    >>> print(tabulate(table, headers, tablefmt="simple_outline"))
    ┌────────┬───────┐
    │ item   │   qty │
    ├────────┼───────┤
    │ spam   │    42 │
    │ eggs   │   451 │
    │ bacon  │     0 │
    └────────┴───────┘

`rounded_outline` is the same as the `rounded_grid` format but doesn't draw lines between rows:

    >>> print(tabulate(table, headers, tablefmt="rounded_outline"))
    ╭────────┬───────╮
    │ item   │   qty │
    ├────────┼───────┤
    │ spam   │    42 │
    │ eggs   │   451 │
    │ bacon  │     0 │
    ╰────────┴───────╯

`heavy_outline` is the same as the `heavy_grid` format but doesn't draw lines between rows:

    >>> print(tabulate(table, headers, tablefmt="heavy_outline"))
    ┏━━━━━━━━┳━━━━━━━┓
    ┃ item   ┃   qty ┃
    ┣━━━━━━━━╋━━━━━━━┫
    ┃ spam   ┃    42 ┃
    ┃ eggs   ┃   451 ┃
    ┃ bacon  ┃     0 ┃
    ┗━━━━━━━━┻━━━━━━━┛

`mixed_outline` is the same as the `mixed_grid` format but doesn't draw lines between rows:

    >>> print(tabulate(table, headers, tablefmt="mixed_outline"))
    ┍━━━━━━━━┯━━━━━━━┑
    │ item   │   qty │
    ┝━━━━━━━━┿━━━━━━━┥
    │ spam   │    42 │
    │ eggs   │   451 │
    │ bacon  │     0 │
    ┕━━━━━━━━┷━━━━━━━┙

`double_outline` is the same as the `double_grid` format but doesn't draw lines between rows:

    >>> print(tabulate(table, headers, tablefmt="double_outline"))
    ╔════════╦═══════╗
    ║ item   ║   qty ║
    ╠════════╬═══════╣
    ║ spam   ║    42 ║
    ║ eggs   ║   451 ║
    ║ bacon  ║     0 ║
    ╚════════╩═══════╝

`fancy_outline` is the same as the `fancy_grid` format but doesn't draw lines between rows:

    >>> print(tabulate(table, headers, tablefmt="fancy_outline"))
    ╒════════╤═══════╕
    │ item   │   qty │
    ╞════════╪═══════╡
    │ spam   │    42 │
    │ eggs   │   451 │
    │ bacon  │     0 │
    ╘════════╧═══════╛

`presto` is like tables formatted by Presto cli:

```pycon
>>> print(tabulate(table, headers, tablefmt="presto"))
 item   |   qty
--------+-------
 spam   |    42
 eggs   |   451
 bacon  |     0

```

`pretty` attempts to be close to the format emitted by the PrettyTables
library:

```pycon
>>> print(tabulate(table, headers, tablefmt="pretty"))
+-------+-----+
| item  | qty |
+-------+-----+
| spam  | 42  |
| eggs  | 451 |
| bacon |  0  |
+-------+-----+

```

`psql` is like tables formatted by Postgres' psql cli:

```pycon
>>> print(tabulate(table, headers, tablefmt="psql"))
+--------+-------+
| item   |   qty |
|--------+-------|
| spam   |    42 |
| eggs   |   451 |
| bacon  |     0 |
+--------+-------+

```

`pipe` follows the conventions of [PHP Markdown
Extra](http://michelf.ca/projects/php-markdown/extra/#table) extension.
It corresponds to `pipe_tables` in Pandoc. This format uses colons to
indicate column alignment:

```pycon
>>> print(tabulate(table, headers, tablefmt="pipe"))
| item   |   qty |
|:-------|------:|
| spam   |    42 |
| eggs   |   451 |
| bacon  |     0 |

```

`asciidoc` formats data like a simple table of the
[AsciiDoctor](https://docs.asciidoctor.org/asciidoc/latest/syntax-quick-reference/#tables)
format:

```pycon
>>> print(tabulate(table, headers, tablefmt="asciidoc"))
[cols="8<,7>",options="header"]
|====
| item   |   qty 
| spam   |    42 
| eggs   |   451 
| bacon  |     0 
|====

```

`orgtbl` follows the conventions of Emacs
[org-mode](http://orgmode.org/manual/Tables.html), and is editable also
in the minor orgtbl-mode. Hence its name:

```pycon
>>> print(tabulate(table, headers, tablefmt="orgtbl"))
| item   |   qty |
|--------+-------|
| spam   |    42 |
| eggs   |   451 |
| bacon  |     0 |

```

`jira` follows the conventions of Atlassian Jira markup language:

```pycon
>>> print(tabulate(table, headers, tablefmt="jira"))
|| item   ||   qty ||
| spam   |    42 |
| eggs   |   451 |
| bacon  |     0 |

```

`rst` formats data like a simple table of the
[reStructuredText](http://docutils.sourceforge.net/docs/user/rst/quickref.html#tables)
format:

```pycon
>>> print(tabulate(table, headers, tablefmt="rst"))
======  =====
item      qty
======  =====
spam       42
eggs      451
bacon       0
======  =====

```

`mediawiki` format produces a table markup used in
[Wikipedia](http://www.mediawiki.org/wiki/Help:Tables) and on other
MediaWiki-based sites:

 ```pycon
>>> print(tabulate(table, headers, tablefmt="mediawiki"))
{| class="wikitable" style="text-align: left;"
|+ <!-- caption -->
|-
! item   !! style="text-align: right;"|   qty
|-
| spam   || style="text-align: right;"|    42
|-
| eggs   || style="text-align: right;"|   451
|-
| bacon  || style="text-align: right;"|     0
|}

```

`moinmoin` format produces a table markup used in
[MoinMoin](https://moinmo.in/) wikis:

```pycon
>>> print(tabulate(table, headers, tablefmt="moinmoin"))
|| ''' item   ''' ||<style="text-align: right;"> '''   qty ''' ||
||  spam    ||<style="text-align: right;">     42  ||
||  eggs    ||<style="text-align: right;">    451  ||
||  bacon   ||<style="text-align: right;">      0  ||

```

`youtrack` format produces a table markup used in Youtrack tickets:

```pycon
>>> print(tabulate(table, headers, tablefmt="youtrack"))
||  item    ||    qty  ||
|  spam    |     42  |
|  eggs    |    451  |
|  bacon   |      0  |

```

`textile` format produces a table markup used in
[Textile](http://redcloth.org/hobix.com/textile/) format:

```pycon
>>> print(tabulate(table, headers, tablefmt="textile"))
|_.  item   |_.   qty |
|<. spam    |>.    42 |
|<. eggs    |>.   451 |
|<. bacon   |>.     0 |

```

`html` produces standard HTML markup as an html.escape'd str
with a ._repr_html_ method so that Jupyter Lab and Notebook display the HTML
and a .str property so that the raw HTML remains accessible.
`unsafehtml` table format can be used if an unescaped HTML is required:

```pycon
>>> print(tabulate(table, headers, tablefmt="html"))
<table>
<thead>
<tr><th>item  </th><th style="text-align: right;">  qty</th></tr>
</thead>
<tbody>
<tr><td>spam  </td><td style="text-align: right;">   42</td></tr>
<tr><td>eggs  </td><td style="text-align: right;">  451</td></tr>
<tr><td>bacon </td><td style="text-align: right;">    0</td></tr>
</tbody>
</table>

```

`latex` format creates a `tabular` environment for LaTeX markup,
replacing special characters like `_` or `\` to their LaTeX
correspondents:

```pycon
>>> print(tabulate(table, headers, tablefmt="latex"))
\begin{tabular}{lr}
\hline
 item   &   qty \\
\hline
 spam   &    42 \\
 eggs   &   451 \\
 bacon  &     0 \\
\hline
\end{tabular}

```

`latex_raw` behaves like `latex` but does not escape LaTeX commands and
special characters.

`latex_booktabs` creates a `tabular` environment for LaTeX markup using
spacing and style from the `booktabs` package.

`latex_longtable` creates a table that can stretch along multiple pages,
using the `longtable` package.

### Column alignment

`tabulate` is smart about column alignment. It detects columns which
contain only numbers, and aligns them by a decimal point (or flushes
them to the right if they appear to be integers). Text columns are
flushed to the left.

You can override the default alignment with `numalign` and `stralign`
named arguments. Possible column alignments are: `right`, `center`,
`left`, `decimal` (only for numbers), and `None` (to disable alignment).

Aligning by a decimal point works best when you need to compare numbers
at a glance:

```pycon
>>> print(tabulate([[1.2345],[123.45],[12.345],[12345],[1234.5]]))
----------
    1.2345
  123.45
   12.345
12345
 1234.5
----------

```

Compare this with a more common right alignment:

```pycon
>>> print(tabulate([[1.2345],[123.45],[12.345],[12345],[1234.5]], numalign="right"))
------
1.2345
123.45
12.345
 12345
1234.5
------

```

For `tabulate`, anything which can be parsed as a number is a number.
Even numbers represented as strings are aligned properly. This feature
comes in handy when reading a mixed table of text and numbers from a
file:

```pycon
>>> import csv; from io import StringIO
>>> table = list(csv.reader(StringIO("spam, 42\neggs, 451\n")))
>>> table
[['spam', ' 42'], ['eggs', ' 451']]
>>> print(tabulate(table))
----  ----
spam    42
eggs   451
----  ----

```

To disable this feature use `disable_numparse=True`.

```pycon
>>> print(tabulate([["Ver1", "18.0"], ["Ver2","19.2"]], tablefmt="simple", disable_numparse=True))
----  ----
Ver1  18.0
Ver2  19.2
----  ----

```

### Custom column alignment

`tabulate` allows a custom column alignment to override the smart alignment described above.
Use `colglobalalign` to define a global setting. Possible alignments are: `right`, `center`, `left`, `decimal` (only for numbers).
Furthermore, you can define `colalign` for column-specific alignment as a list or a tuple. Possible values are `global` (keeps global setting), `right`, `center`, `left`, `decimal` (only for numbers), `None` (to disable alignment). Missing alignments are treated as `global`.

```pycon
>>> print(tabulate([[1,2,3,4],[111,222,333,444]], colglobalalign='center', colalign = ('global','left','right')))
---  ---  ---  ---
 1   2      3   4
111  222  333  444
---  ---  ---  ---

```

### Custom header alignment

Headers' alignment can be defined separately from columns'. Like for columns, you can use:
- `headersglobalalign` to define a header-specific global alignment setting. Possible values are `right`, `center`, `left`, `None` (to follow column alignment),
- `headersalign` list or tuple to further specify header-wise alignment. Possible values are `global` (keeps global setting), `same` (follow column alignment), `right`, `center`, `left`, `None` (to disable alignment). Missing alignments are treated as `global`.

```pycon
>>> print(tabulate([[1,2,3,4,5,6],[111,222,333,444,555,666]], colglobalalign = 'center', colalign = ('left',), headers = ['h','e','a','d','e','r'], headersglobalalign = 'right', headersalign = ('same','same','left','global','center')))
h     e   a      d   e     r
---  ---  ---  ---  ---  ---
1     2    3    4    5    6
111  222  333  444  555  666

```

### Number formatting

`tabulate` allows to define custom number formatting applied to all
columns of decimal numbers. Use `floatfmt` named argument:

```pycon
>>> print(tabulate([["pi",3.141593],["e",2.718282]], floatfmt=".4f"))
--  ------
pi  3.1416
e   2.7183
--  ------

```

`floatfmt` argument can be a list or a tuple of format strings, one per
column, in which case every column may have different number formatting:

```pycon
>>> print(tabulate([[0.12345, 0.12345, 0.12345]], floatfmt=(".1f", ".3f")))
---  -----  -------
0.1  0.123  0.12345
---  -----  -------

```

`intfmt` works similarly for integers

    >>> print(tabulate([["a",1000],["b",90000]], intfmt=","))
    -  ------
    a   1,000
    b  90,000
    -  ------


### Type Deduction and Missing Values

When `tabulate` sees numerical data (with our without comma separators), it
attempts to align the column on the decimal point.  However, if it observes
non-numerical data in the column, it aligns it to the left by default.  If
data is missing in a column (either None or empty values), the remaining
data in the column is used to infer the type:

```pycon
>>> from fractions import Fraction
>>> test_table = [
...    [None, "1.23423515351", Fraction(1, 3)],
...    [Fraction(56789, 1000000), 12345.1, b"abc"],
...    ["", b"", None],
...    [Fraction(10000, 3), None, ""],
... ]
>>> print(tabulate(test_table, floatfmt=",.5g", missingval="?"))
------------  -----------  ---
    ?              1.2342  1/3
    0.056789  12,345       abc
                           ?
3,333.3            ?
------------  -----------  ---

```

The deduced type (eg. str, float) influences the rendering of any types
that have alternative representations.  For example, since `Fraction` has
methods `__str__` and `__float__` defined (and hence is convertible to a
`float` and also has a `str` representation), the appropriate
representation is selected for the column's deduced type.  In order to not
lose precision accidentally, types having both an `__int__` and
`__float__` representation will be considered a `float`.

Therefore, if your table contains types convertible to int/float but you'd
*prefer* they be represented as strings, or your strings *might* all look
like numbers such as "1e23": either convert them to the desired
representation before you `tabulate`, or ensure that the column always
contains at least one other `str`.

### Text formatting

By default, `tabulate` removes leading and trailing whitespace from text
columns. To disable whitespace removal, pass `preserve_whitespace=True`.
Older versions of the library used a global module-level flag PRESERVE_WHITESPACE.

### Wide (fullwidth CJK) symbols

To properly align tables which contain wide characters (typically
fullwidth glyphs from Chinese, Japanese or Korean languages), the user
should install `wcwidth` library. To install it together with
`tabulate`:

```shell
pip install tabulate[widechars]
```

Wide character support is enabled automatically if `wcwidth` library is
already installed. To disable wide characters support without
uninstalling `wcwidth`, set the global module-level flag
`WIDE_CHARS_MODE`:

```python
import tabulate
tabulate.WIDE_CHARS_MODE = False
```

### Multiline cells

Most table formats support multiline cell text (text containing newline
characters). The newline characters are honored as line break
characters.

Multiline cells are supported for data rows and for header rows.

Further automatic line breaks are not inserted. Of course, some output
formats such as latex or html handle automatic formatting of the cell
content on their own, but for those that don't, the newline characters
in the input cell text are the only means to break a line in cell text.

Note that some output formats (e.g. simple, or plain) do not represent
row delimiters, so that the representation of multiline cells in such
formats may be ambiguous to the reader.

The following examples of formatted output use the following table with
a multiline cell, and headers with a multiline cell:

```pycon
>>> table = [["eggs",451],["more\nspam",42]]
>>> headers = ["item\nname", "qty"]

```

`plain` tables:

```pycon
>>> print(tabulate(table, headers, tablefmt="plain"))
item      qty
name
eggs      451
more       42
spam

```

`simple` tables:

```pycon
>>> print(tabulate(table, headers, tablefmt="simple"))
item      qty
name
------  -----
eggs      451
more       42
spam

```

`grid` tables:

```pycon
>>> print(tabulate(table, headers, tablefmt="grid"))
+--------+-------+
| item   |   qty |
| name   |       |
+========+=======+
| eggs   |   451 |
+--------+-------+
| more   |    42 |
| spam   |       |
+--------+-------+

```

`fancy_grid` tables:

```pycon
>>> print(tabulate(table, headers, tablefmt="fancy_grid"))
╒════════╤═══════╕
│ item   │   qty │
│ name   │       │
╞════════╪═══════╡
│ eggs   │   451 │
├────────┼───────┤
│ more   │    42 │
│ spam   │       │
╘════════╧═══════╛

```

`pipe` tables:

```pycon
>>> print(tabulate(table, headers, tablefmt="pipe"))
| item   |   qty |
| name   |       |
|:-------|------:|
| eggs   |   451 |
| more   |    42 |
| spam   |       |

```

`orgtbl` tables:

```pycon
>>> print(tabulate(table, headers, tablefmt="orgtbl"))
| item   |   qty |
| name   |       |
|--------+-------|
| eggs   |   451 |
| more   |    42 |
| spam   |       |

```

`jira` tables:

```pycon
>>> print(tabulate(table, headers, tablefmt="jira"))
|| item   ||   qty ||
|| name   ||       ||
| eggs   |   451 |
| more   |    42 |
| spam   |       |

```

`presto` tables:

```pycon
>>> print(tabulate(table, headers, tablefmt="presto"))
 item   |   qty
 name   |
--------+-------
 eggs   |   451
 more   |    42
 spam   |

```

`pretty` tables:

```pycon
>>> print(tabulate(table, headers, tablefmt="pretty"))
+------+-----+
| item | qty |
| name |     |
+------+-----+
| eggs | 451 |
| more | 42  |
| spam |     |
+------+-----+

```

`psql` tables:

```pycon
>>> print(tabulate(table, headers, tablefmt="psql"))
+--------+-------+
| item   |   qty |
| name   |       |
|--------+-------|
| eggs   |   451 |
| more   |    42 |
| spam   |       |
+--------+-------+

```

`rst` tables:

```pycon
>>> print(tabulate(table, headers, tablefmt="rst"))
======  =====
item      qty
name
======  =====
eggs      451
more       42
spam
======  =====

```

Multiline cells are not well-supported for the other table formats.

### Automating Multilines
While tabulate supports data passed in with multilines entries explicitly provided,
it also provides some support to help manage this work internally.

The `maxcolwidths` argument is a list where each entry specifies the max width for
it's respective column. Any cell that will exceed this will automatically wrap the content.
To assign the same max width for all columns, a singular int scaler can be used.

Use `None` for any columns where an explicit maximum does not need to be provided,
and thus no automate multiline wrapping will take place.

The wrapping uses the python standard [textwrap.wrap](https://docs.python.org/3/library/textwrap.html#textwrap.wrap)
function with default parameters - aside from width.

This example demonstrates usage of automatic multiline wrapping, though typically
the lines being wrapped would probably be significantly longer than this.

```pycon
>>> print(tabulate([["John Smith", "Middle Manager"]], headers=["Name", "Title"], tablefmt="grid", maxcolwidths=[None, 8]))
+------------+---------+
| Name       | Title   |
+============+=========+
| John Smith | Middle  |
|            | Manager |
+------------+---------+

```

Text is preferably wrapped on whitespaces and right after the hyphens in hyphenated words.

break_long_words (default: True)  If true, then words longer than width will be broken in order to ensure that no lines are longer than width. 
If it is false, long words will not be broken, and some lines may be longer than width.
(Long words will be put on a line by themselves, in order to minimize the amount by which width is exceeded.)

break_on_hyphens (default: True) If true, wrapping will occur preferably on whitespaces and right after hyphens in compound words, as it is customary in English. 
If false, only whitespaces will be considered as potentially good places for line breaks.

```pycon
>>> print(tabulate([["John Smith", "Middle-Manager"]], headers=["Name", "Title"], tablefmt="grid", maxcolwidths=[None, 5], break_long_words=False))
+------------+---------+
| Name       | Title   |
+============+=========+
| John Smith | Middle- |
|            | Manager |
+------------+---------+
>>> print(tabulate([["John Smith", "Middle-Manager"]], headers=["Name", "Title"], tablefmt="grid", maxcolwidths=[None, 5], break_long_words=False, break_on_hyphens=False))
+------------+----------------+
| Name       | Title          |
+============+================+
| John Smith | Middle-Manager |
+------------+----------------+
```

### Adding Separating lines
One might want to add one or more separating lines to highlight different sections in a table.

The separating lines will be of the same type as the one defined by the specified formatter as either the
linebetweenrows, linebelowheader, linebelow, lineabove or just a simple empty line when none is defined for the formatter


    >>> from tabulate import tabulate, SEPARATING_LINE

    table = [["Earth",6371],
             ["Mars",3390],
             SEPARATING_LINE,
             ["Moon",1737]]
    print(tabulate(table, tablefmt="simple"))
    -----  ----
    Earth  6371
    Mars   3390
    -----  ----
    Moon   1737
    -----  ----

### ANSI support
ANSI escape codes are non-printable byte sequences usually used for terminal operations like setting
color output or modifying cursor positions. Because multi-byte ANSI sequences are inherently non-printable,
they can still introduce unwanted extra length to strings. For example:

    >>> len('\033[31mthis text is red\033[0m')  # printable length is 16
    25

To deal with this, string lengths are calculated after first removing all ANSI escape sequences. This ensures
that the actual printable length is used for column widths, rather than the byte length. In the final, printable
table, however, ANSI escape sequences are not removed so the original styling is preserved.

Some terminals support a special grouping of ANSI escape sequences that are intended to display hyperlinks
much in the same way they are shown in browsers. These are handled just as mentioned before: non-printable
ANSI escape sequences are removed prior to string length calculation. The only difference with escaped
hyperlinks is that column width will be based on the length of the URL _text_ rather than the URL
itself (terminals would show this text). For example:

    >>> len('\x1b]8;;https://example.com\x1b\\example\x1b]8;;\x1b\\')  # display length is 7, showing 'example'
    40


Usage of the command line utility
---------------------------------

    Usage: tabulate [options] [FILE ...]

    FILE                      a filename of the file with tabular data;
                              if "-" or missing, read data from stdin.

    Options:

    -h, --help                show this message
    -1, --header              use the first row of data as a table header
    -o FILE, --output FILE    print table to FILE (default: stdout)
    -s REGEXP, --sep REGEXP   use a custom column separator (default: whitespace)
    -F FPFMT, --float FPFMT   floating point number format (default: g)
    -I INTFMT, --int INTFMT   integer point number format (default: "")
    -f FMT, --format FMT      set output table format; supported formats:
                              plain, simple, github, grid, fancy_grid, pipe,
                              orgtbl, rst, mediawiki, html, latex, latex_raw,
                              latex_booktabs, latex_longtable, tsv
                              (default: simple)

Performance considerations
--------------------------

Such features as decimal point alignment and trying to parse everything
as a number imply that `tabulate`:

-   has to "guess" how to print a particular tabular data type
-   needs to keep the entire table in-memory
-   has to "transpose" the table twice
-   does much more work than it may appear

It may not be suitable for serializing really big tables (but who's
going to do that, anyway?) or printing tables in performance sensitive
applications. `tabulate` is about two orders of magnitude slower than
simply joining lists of values with a tab, comma, or other separator.

At the same time, `tabulate` is comparable to other table
pretty-printers. Given a 10x10 table (a list of lists) of mixed text and
numeric data, `tabulate` appears to be faster than `PrettyTable` and `texttable`.
The following mini-benchmark was run in Python 3.11.9 on Windows 11 (x64):

    ==================================  ==========  ===========
    Table formatter                       time, μs    rel. time
    ==================================  ==========  ===========
    join with tabs and newlines                6.3          1.0
    csv to StringIO                            6.6          1.0
    tabulate (0.10.0)                        249.2         39.3
    tabulate (0.10.0, WIDE_CHARS_MODE)       325.6         51.4
    texttable (1.7.0)                        579.3         91.5
    PrettyTable (3.11.0)                     605.5         95.6
    ==================================  ==========  ===========


Version history
---------------

The full version history can be found at the [changelog](https://github.com/astanin/python-tabulate/blob/master/CHANGELOG).

How to contribute
-----------------

Contributions should include tests and an explanation for the changes
they propose. Documentation (examples, docstrings, README.md) should be
updated accordingly.

This project uses [pytest](https://docs.pytest.org/) testing
framework and [tox](https://tox.readthedocs.io/) to automate testing in
different environments. Add tests to one of the files in the `test/`
folder.

To run tests on all supported Python versions, make sure all Python
interpreters, `pytest` and `tox` are installed, then run `tox` in the root
of the project source tree.

On Linux `tox` expects to find executables like `python3.11`, `python3.12` etc.
On Windows it looks for `C:\Python311\python.exe`, `C:\Python312\python.exe` etc. respectively.

One way to install all the required versions of the Python interpreter is to use [pyenv](https://github.com/pyenv/pyenv).
All versions can then be easily installed with something like:

     pyenv install 3.11.7
     pyenv install 3.12.1
     ...

Don't forget to change your `PATH` so that `tox` knows how to find all the installed versions. Something like

     export PATH="${PATH}:${HOME}/.pyenv/shims"

To test only some Python environments, use `-e` option. For example, to
test only against Python 3.11 and Python 3.12, run:

```shell
tox -e py311,py312
```

in the root of the project source tree.

To enable NumPy and Pandas tests, run:

```shell
tox -e py311-extra,py312-extra
```

(this may take a long time the first time, because NumPy and Pandas will
have to be installed in the new virtual environments)

To fix code formatting:

```shell
tox -e lint
```

See `tox.ini` file to learn how to use to test
individual Python versions.

To test the "doctest" examples and their outputs in `README.md`:

```shell
python3 -m pip install pytest-doctestplus[md]
python3 -m doctest README.md
```

Contributors
------------

Sergey Astanin, Pau Tallada Crespí, Erwin Marsi, Mik Kocikowski, Bill
Ryder, Zach Dwiel, Frederik Rietdijk, Philipp Bogensberger, Greg
(anonymous), Stefan Tatschner, Emiel van Miltenburg, Brandon Bennett,
Amjith Ramanujam, Jan Schulz, Simon Percivall, Javier Santacruz
López-Cepero, Sam Denton, Alexey Ziyangirov, acaird, Cesar Sanchez,
naught101, John Vandenberg, Zack Dever, Christian Clauss, Benjamin
Maier, Andy MacKinlay, Thomas Roten, Jue Wang, Joe King, Samuel Phan,
Nick Satterly, Daniel Robbins, Dmitry B, Lars Butler, Andreas Maier,
Dick Marinus, Sébastien Celles, Yago González, Andrew Gaul, Wim Glenn,
Jean Michel Rouly, Tim Gates, John Vandenberg, Sorin Sbarnea,
Wes Turner, Andrew Tija, Marco Gorelli, Sean McGinnis, danja100,
endolith, Dominic Davis-Foster, pavlocat, Daniel Aslau, paulc,
Felix Yan, Shane Loretz, Frank Busse, Harsh Singh, Derek Weitzel,
Vladimir Vrzić, 서승우 (chrd5273), Georgy Frolov, Christian Cwienk,
Bart Broere, Vilhelm Prytz, Alexander Gažo, Hugo van Kemenade,
jamescooke, Matt Warner, Jérôme Provensal, Michał Górny, Kevin Deldycke,
Kian-Meng Ang, Kevin Patterson, Shodhan Save, cleoold, KOLANICH,
Vijaya Krishna Kasula, Furcy Pin, Christian Fibich, Shaun Duncan,
Dimitri Papadopoulos, Élie Goudout, Racerroar888, Phill Zarfos,
Keyacom, Andrew Coffey, Arpit Jain, Israel Roldan, ilya112358,
Dan Nicholson, Frederik Scheerer, cdar07 (cdar), Racerroar888,
Perry Kundert.
