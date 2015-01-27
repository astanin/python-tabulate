"""Command-line interface.

"""


from __future__ import print_function
from __future__ import unicode_literals
import os


import subprocess
import tempfile


from common import assert_equal


def write_sample_input(tmpfile):
    table = "\n".join([
        'Sun 696000 1.9891e9',
        'Earth 6371 5973.6',
        'Moon 1737 73.5',
        'Mars 3390 641.85'])
    tmpfile.write(table)
    tmpfile.file.seek(0)


def get_stdout_and_stderr(cmd):
    x = subprocess.Popen(cmd,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)
    out, _ = x.communicate()
    out = out.decode("utf-8")
    return out


class TemporaryTextFile(object):
    def __init__(self):
        self.tmpfile = None
    def __enter__(self):
        self.tmpfile = tempfile.NamedTemporaryFile("w+", prefix="tabulate-test-tmp-", delete=False)
        return self.tmpfile
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.tmpfile:
            self.tmpfile.close()
            os.unlink(self.tmpfile.name)


def test_script_from_file_to_stdout():
    """CLI: read from file, print to stdout"""
    with TemporaryTextFile() as tmpfile:
        write_sample_input(tmpfile)
        cmd = ["python", "tabulate.py", tmpfile.name]
        out = get_stdout_and_stderr(cmd)
        expected = "\n".join([
                '-----  ------  -------------',
                'Sun    696000     1.9891e+09',
                'Earth    6371  5973.6',
                'Moon     1737    73.5',
                'Mars     3390   641.85',
                '-----  ------  -------------'])
        print("got:     ",repr(out))
        print("expected:",repr(expected))
        assert_equal(out.rstrip().splitlines(), expected.rstrip().splitlines())
