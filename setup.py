#!/usr/bin/env python

import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

def get_version(filename):
    """Extract __version__ from file by parsing it."""
    with open(filename) as fp:
        for line in fp:
            if line.startswith('__version__'):
                exec(line)
                return __version__

setup(
    name='mdview',
    version=get_version('mdview/__init__.py'),
    description='Markdown viewer',
    url='https://github.com/guyru/mdview',
    author='Guy Rutenberg',
    author_email='guyrutenberg@gmail.com',
    license = 'GPLv3+',
    packages=['mdview'],
    long_description=read('README.rst'),
    package_data={'mdview': ['static/*.js', 'static/*.css']},
    install_requires = ['markdown'],

    classifiers = [
        ],
)

