"""API properties.

"""

from tabulate import tabulate, tabulate_formats, simple_separated_format
from common import skip


try:
    from inspect import signature, _empty
except ImportError:
    signature = None
    _empty = None


def test_tabulate_formats():
    "API: tabulate_formats is a list of strings" ""
    supported = tabulate_formats
    print("tabulate_formats = %r" % supported)
    assert type(supported) is list
    for fmt in supported:
        assert type(fmt) is str  # noqa


def _check_signature(function, expected_sig):
    if not signature:
        skip("")
    actual_sig = signature(function)
    print(f"expected: {expected_sig}\nactual: {str(actual_sig)}\n")

    assert len(actual_sig.parameters) == len(expected_sig)

    for (e, ev), (a, av) in zip(expected_sig, actual_sig.parameters.items()):
        assert e == a and ev == av.default


def test_tabulate_signature():
    "API: tabulate() type signature is unchanged" ""
    assert type(tabulate) is type(lambda: None)  # noqa
    expected_sig = [
        ("tabular_data", _empty),
        ("headers", ()),
        ("tablefmt", "simple"),
        ("floatfmt", "g"),
        ("intfmt", ""),
        ("numalign", "default"),
        ("stralign", "default"),
        ("missingval", ""),
        ("showindex", "default"),
        ("disable_numparse", False),
        ("colglobalalign", None),
        ("colalign", None),
        ("maxcolwidths", None),
        ("headersglobalalign", None),
        ("headersalign", None),
        ("rowalign", None),
        ("maxheadercolwidths", None),
    ]
    _check_signature(tabulate, expected_sig)


def test_simple_separated_format_signature():
    "API: simple_separated_format() type signature is unchanged" ""
    assert type(simple_separated_format) is type(lambda: None)  # noqa
    expected_sig = [("separator", _empty)]
    _check_signature(simple_separated_format, expected_sig)
