#!/usr/bin/env python

from distutils.core import setup

LICENSE = open("LICENSE").read()

setup(name='tabulate',
   version='0.2',
   description='Pretty-print tabular data',
   author='Sergey Astanin',
   author_email='s.astanin@gmail.com',
   url='https://bitbucket.org/astanin/python-tabulate',
   license=LICENSE,
   classifiers= [ "Development Status :: 4 - Beta",
                  "License :: OSI Approved :: MIT License",
                  "Operating System :: OS Independent",
                  "Programming Language :: Python :: 2",
                  "Topic :: Software Development :: Libraries" ],
   py_modules = ['tabulate'])
