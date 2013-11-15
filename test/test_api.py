"""API properties.

"""

from __future__ import print_function
from __future__ import unicode_literals
from tabulate import tabulate, tabulate_formats, simple_separated_format
from nose.tools import assert_raises


def test_tabulate_formats():
    "Check if tabulate_formats is a list of strings"""
    supported = tabulate_formats
    print("tabulate_formats = %r" % supported)
    assert type(supported) is list
    for fmt in supported:
        assert type(fmt) is type(u"")


def test_tabulate_signature():
    "Check if tabulate() type signature is unchanged"""
    assert type(tabulate) is type(lambda: None)
    fn = tabulate.func_code
    assert fn.co_varnames[:fn.co_argcount] == \
        ('tabular_data', 'headers', 'tablefmt',
         'floatfmt', 'numalign', 'stralign', 'missingval')
    # one and only one required argument
    assert_raises(TypeError, tabulate)
    assert u"\n" == tabulate([])

def test_simple_separated_format_signature():
    "Check if simple_separated_format() type signature is unchanged"""
    assert type(simple_separated_format) is type(lambda: None)
    fn = simple_separated_format.func_code
    assert fn.co_varnames[:fn.co_argcount] == ('separator',)
