#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


from platform import python_version_tuple, python_implementation
import os
import re

# strip links from the descripton on the PyPI
if python_version_tuple()[0] >= '3':
    LONG_DESCRIPTION = open("README.rst", "r", encoding="utf-8").read().replace("`_", "`")
else:
    LONG_DESCRIPTION = open("README.rst", "r").read().replace("`_", "`")

# strip Build Status from the PyPI package
try:
    if python_version_tuple()[:2] >= ('2', '7'):
        status_re = "^Build status\n(.*\n){7}"
        LONG_DESCRIPTION = re.sub(status_re, "", LONG_DESCRIPTION, flags=re.M)
except TypeError:
    if python_implementation() == "IronPython":
        # IronPython doesn't support flags in re.sub (IronPython issue #923)
        pass
    else:
        raise

install_options = os.environ.get("TABULATE_INSTALL","").split(",")
libonly_flags = set(["lib-only", "libonly", "no-cli", "without-cli"])
if libonly_flags.intersection(install_options):
    console_scripts = []
else:
    console_scripts = ['tabulate = tabulate:_main']


setup(name='tabulate',
      version='0.8.0',
      description='Pretty-print tabular data',
      long_description=LONG_DESCRIPTION,
      author='Sergey Astanin',
      author_email='s.astanin@gmail.com',
      url='https://bitbucket.org/astanin/python-tabulate',
      license='MIT',
      classifiers= [ "Development Status :: 4 - Beta",
                     "License :: OSI Approved :: MIT License",
                     "Operating System :: OS Independent",
                     "Programming Language :: Python :: 2",
                     "Programming Language :: Python :: 2.7",
                     "Programming Language :: Python :: 3.3",
                     "Programming Language :: Python :: 3.4",
                     "Programming Language :: Python :: 3",
                     "Programming Language :: Python :: 3.5",
                     "Programming Language :: Python :: 3.6",
                     "Topic :: Software Development :: Libraries" ],
      py_modules = ['tabulate'],
      entry_points = {'console_scripts': console_scripts},
      extras_require = {'widechars': ['wcwidth']},
      test_suite = 'nose.collector')
