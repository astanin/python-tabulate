#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


from platform import python_implementation
import os
import re

# strip links from the description on the PyPI
LONG_DESCRIPTION = open("README.md", "r", encoding="utf-8").read()

# strip Build Status from the PyPI package
try:
    status_re = "^Build status\n(.*\n){7}"
    LONG_DESCRIPTION = re.sub(status_re, "", LONG_DESCRIPTION, flags=re.M)
except TypeError:
    if python_implementation() == "IronPython":
        # IronPython doesn't support flags in re.sub (IronPython issue #923)
        pass
    else:
        raise

install_options = os.environ.get("TABULATE_INSTALL", "").split(",")
libonly_flags = set(["lib-only", "libonly", "no-cli", "without-cli"])
if libonly_flags.intersection(install_options):
    console_scripts = []
else:
    console_scripts = ["tabulate = tabulate:_main"]


setup(
    name="tabulate",
    version="0.8.10",
    description="Pretty-print tabular data",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    author="Sergey Astanin",
    author_email="s.astanin@gmail.com",
    url="https://github.com/astanin/python-tabulate",
    license="MIT",
    python_requires=">=3.7",
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Software Development :: Libraries",
    ],
    py_modules=["tabulate"],
    entry_points={"console_scripts": console_scripts},
    extras_require={"widechars": ["wcwidth"]},
)
