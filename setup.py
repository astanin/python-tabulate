#!/usr/bin/env python

from distutils.core import setup

LICENSE = open("LICENSE").read()

# strip links from the descripton on the PyPI
LONG_DESCRIPTION = open("README.rst").read().replace("`_", "`")

setup(name='tabulate',
   version='0.7',
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
                  "Programming Language :: Python :: 3.3",
                  "Topic :: Software Development :: Libraries" ],
   py_modules = ['tabulate'])
