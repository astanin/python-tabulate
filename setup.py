#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


from platform import python_version_tuple
import os
import re


LICENSE = open("LICENSE").read()


# strip links from the descripton on the PyPI
if python_version_tuple()[0] >= '3':
    LONG_DESCRIPTION = open("README.rst", "r", encoding="utf-8").read().replace("`_", "`")
else:
    LONG_DESCRIPTION = open("README.rst", "r").read().replace("`_", "`")

# strip Build Status from the PyPI package
if python_version_tuple()[:2] >= ('2', '7'):
    LONG_DESCRIPTION = re.sub("^Build status\n(.*\n){7}", "", LONG_DESCRIPTION, flags=re.M)


install_options = os.environ.get("TABULATE_INSTALL","").split(",")
libonly_flags = set(["lib-only", "libonly", "no-cli", "without-cli"])
if libonly_flags.intersection(install_options):
    console_scripts = []
else:
    console_scripts = ['tabulate = tabulate:_main']


setup(name='tabulate',
      version='0.7.4',
      description='Pretty-print tabular data',
      long_description=LONG_DESCRIPTION,
      author='Sergey Astanin',
      author_email='s.astanin@gmail.com',
      url='https://bitbucket.org/astanin/python-tabulate',
      license=LICENSE,
      classifiers= [ "Development Status :: 4 - Beta",
                     "License :: OSI Approved :: MIT License",
                     "Operating System :: OS Independent",
                     "Programming Language :: Python :: 2.6",
                     "Programming Language :: Python :: 2.7",
                     "Programming Language :: Python :: 3.2",
                     "Programming Language :: Python :: 3.3",
                     "Programming Language :: Python :: 3.4",
                     "Topic :: Software Development :: Libraries" ],
      py_modules = ['tabulate'],
      entry_points = {'console_scripts': console_scripts},
      test_suite = 'nose.collector')
