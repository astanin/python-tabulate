"""API properties.

"""

from __future__ import print_function
from __future__ import unicode_literals
from tabulate import tabulate, tabulate_formats, simple_separated_format
from platform import python_version_tuple
from nose.plugins.skip import SkipTest


try:
    if python_version_tuple() >= ('3','3','0'):
        from inspect import signature, _empty
    else:
        from funcsigs import signature, _empty
except ImportError:
    signature = None
    _empty = None


def test_tabulate_formats():
    "API: tabulate_formats is a list of strings"""
    supported = tabulate_formats
    print("tabulate_formats = %r" % supported)
    assert type(supported) is list
    for fmt in supported:
        assert type(fmt) is type("")


def _check_signature(function, expected_sig):
    if not signature:
        raise SkipTest()
    actual_sig = signature(function)
    print("expected: %s\nactual: %s\n" % (expected_sig, str(actual_sig)))
    for (e, ev), (a, av) in zip(expected_sig, actual_sig.parameters.items()):
        assert e == a and ev == av.default


def test_tabulate_signature():
    "API: tabulate() type signature is unchanged"""
    assert type(tabulate) is type(lambda: None)
    expected_sig = [("tabular_data", _empty),
                    ("headers", ()),
                    ("tablefmt", "simple"),
                    ("floatfmt", "g"),
                    ("numalign", "decimal"),
                    ("stralign", "left"),
                    ("missingval", "")]
    _check_signature(tabulate, expected_sig)


def test_simple_separated_format_signature():
    "API: simple_separated_format() type signature is unchanged"""
    assert type(simple_separated_format) is type(lambda: None)
    expected_sig = [("separator", _empty)]
    _check_signature(simple_separated_format, expected_sig)
