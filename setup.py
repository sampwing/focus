#!/usr/bin/env python

from setuptools import setup

setup(
    author='Sam Wing',
    description='disable webpage access for a period of time',
    entry_points={
        'console_scripts': ['focus=focus.cli:main']
    },
    name='focus',
    packages=['focus']
)
