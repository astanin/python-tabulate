===============
python-tabulate
===============

Pretty-print tabular data in Python.

The main use cases of the library are:

* printing small tables without hassle: just one function call,
  formatting is guided by the data itself

* authoring tabular data for lightweight plain-text markup: multiple
  output formats suitable for further editing or transformation

* readable presentation of mixed textual and numeric data: smart
  column alignment, configurable number formatting, alignment by a
  decimal point


Installation
------------

::

    pip install tabulate


Usage
-----

The module provides just one function, ``tabulate``, which takes a list
of lists or a similarly shaped data structure, and outputs a nicely
formatted plain-text table::

    >>> from tabulate import tabulate

    >>> table = [["Sun",696000,1989100000],["Earth",6371,5973.6],
    ...          ["Moon",1737,73.5],["Mars",3390,641.85]]
    >>> print tabulate(table)
    -----  ------  -------------
    Sun    696000     1.9891e+09
    Earth    6371  5973.6
    Moon     1737    73.5
    Mars     3390   641.85
    -----  ------  -------------

``tabulate`` can pretty-print two-dimensional NumPy arrays too.

Examples in this file use Python2. Tabulate supports Python3 too.


Headers
~~~~~~~

If function ``tabulate`` receives two arguments, it considers the
second argument to be a list of column headers.
The list of headers may be passed also out-of-order with a named
argument ``headers=...``::

    >>> print tabulate(table, headers=["Planet","R (km)", "mass (x 10^29 kg)"])
    Planet      R (km)    mass (x 10^29 kg)
    --------  --------  -------------------
    Sun         696000           1.9891e+09
    Earth         6371        5973.6
    Moon          1737          73.5
    Mars          3390         641.85


Table format
~~~~~~~~~~~~

There is more than one way to format a table in plain text. The output
format of ``tabulate`` is defined by an optional named argument
``tablefmt``.

Supported table formats are:

- "plain"
- "simple"
- "grid"
- "pipe"
- "orgtbl"
- "rst"

``plain`` tables do not use any pseudo-graphics to draw lines::

    >>> table = [["spam",42],["eggs",451],["bacon",0]]
    >>> headers = ["item", "qty"]
    >>> print tabulate(table, headers, tablefmt="plain")
    item      qty
    spam       42
    eggs      451
    bacon       0

``simple`` is the default format (the default may change in future
versions).  It corresponds to ``simple_tables`` in `Pandoc Markdown
extensions`_::

    >>> print tabulate(table, headers, tablefmt="simple")
    item      qty
    ------  -----
    spam       42
    eggs      451
    bacon       0

``grid`` is like tables formatted by Emacs' `table.el`_
  package.  It corresponds to ``grid_tables`` in Pandoc Markdown
extensions::

    >>> print tabulate(table, headers, tablefmt="grid")
    +--------+-------+
    | item   |   qty |
    +========+=======+
    | spam   |    42 |
    +--------+-------+
    | eggs   |   451 |
    +--------+-------+
    | bacon  |     0 |
    +--------+-------+

``pipe`` follows the conventions of `PHP Markdown Extra`_ extension.  It
corresponds to ``pipe_tables`` in Pandoc. This format uses colons to
indicate column alignment::

    >>> print tabulate(table, headers, tablefmt="pipe")
    | item   |   qty |
    |:-------|------:|
    | spam   |    42 |
    | eggs   |   451 |
    | bacon  |     0 |

``orgtbl`` follows the conventions of Emacs `org-mode`_, and is editable
also in the minor `orgtbl-mode`. Hence its name::

    >>> print tabulate(table, headers, tablefmt="orgtbl")
    | item   |   qty |
    |--------+-------|
    | spam   |    42 |
    | eggs   |   451 |
    | bacon  |     0 |

``rst`` formats data like a simple table of the `reStructuredText`_ format::

    >>> print tabulate(table, headers, tablefmt="rst")
    ======  =====
    item      qty
    ======  =====
    spam       42
    eggs      451
    bacon       0
    ======  =====


.. _Pandoc Markdown extensions: http://johnmacfarlane.net/pandoc/README.html#tables
.. _PHP Markdown Extra: http://michelf.ca/projects/php-markdown/extra/#table
.. _table.el: http://table.sourceforge.net/
.. _org-mode: http://orgmode.org/manual/Tables.html
.. _reStructuredText: http://docutils.sourceforge.net/docs/user/rst/quickref.html#tables


Column alignment
~~~~~~~~~~~~~~~~

``tabulate`` is smart about column alignment. It detects columns which
contain only numbers, and aligns them by a decimal point (or flushes
them to the right if they appear to be integers). Text columns are
flushed to the left.

You can override the default alignment with ``numalign`` and
``stralign`` named arguments. Possible column alignments are: ``right``,
``center``, ``left``, ``decimal`` (only for numbers).

Aligning by a decimal point works best when you need to compare
numbers at a glance::

    >>> print tabulate([[1.2345],[123.45],[12.345],[12345],[1234.5]])
    ----------
        1.2345
      123.45
       12.345
    12345
     1234.5
    ----------

Compare this with a more common right alignment::

    >>> print tabulate([[1.2345],[123.45],[12.345],[12345],[1234.5]], numalign="right")
    ------
    1.2345
    123.45
    12.345
     12345
    1234.5
    ------

For ``tabulate``, anything which can be parsed as a number is a
number. Even numbers represented as strings are aligned properly. This
feature comes in handy when reading a mixed table of text and numbers
from a file:

::

    >>> import csv ; from StringIO import StringIO
    >>> table = list(csv.reader(StringIO("spam, 42\neggs, 451\n")))
    >>> table
    [['spam', ' 42'], ['eggs', ' 451']]
    >>> print tabulate(table)
    ----  ----
    spam    42
    eggs   451
    ----  ----



Number formatting
~~~~~~~~~~~~~~~~~

``tabulate`` allows to define custom number formatting applied to all
columns of decimal numbers. Use ``floatfmt`` named argument::


    >>> print tabulate([["pi",3.141593],["e",2.718282]], floatfmt=".4f")
    --  ------
    pi  3.1416
    e   2.7183
    --  ------


Performance considerations
--------------------------

Such features as decimal point alignment and trying to parse everything
as a number imply that ``tabulate``:

* needs to keep the entire table in-memory
* has to "transpose" the table twice
* does much more work than it may appear

It may not be suitable for serializing really big tables (but who's
going to do that, anyway?) or printing tables in performance sensitive
applications. ``tabulate`` is about two orders of magnitude slower
than simply joining lists of values with a tab, coma or other
separator.

In the same time ``tabulate`` is comparable to other table
pretty-printers. Given a 10x10 table (a list of lists) of mixed text
and numeric data, ``tabulate`` appears to be slightly slower than
``asciitable``, and much faster than ``PrettyTable`` and
``texttable``

::

    ===========================  ==========  ===========
    Table formatter                time, μs    rel. time
    ===========================  ==========  ===========
    join with tabs and newlines        22.8          1.0
    csv to StringIO                    32.8          1.4
    asciitable (0.8)                  852.5         37.4
    tabulate (0.4.2)                 1098.9         48.3
    PrettyTable (0.7.1)              3781.5        166.1
    texttable (0.8.1)                4173.0        183.3
    ===========================  ==========  ===========


Version history
---------------

- 0.4.3: Bug fix, None as a missing value
- 0.4.2: Fix manifest file
- 0.4.1: Update license and documentation.
- 0.4: Unicode support, Python3 support, ``rst`` tables
- 0.3: Initial PyPI release. Table formats: ``simple``, ``plain``,
  ``grid``, ``pipe``, and ``orgtbl``.
