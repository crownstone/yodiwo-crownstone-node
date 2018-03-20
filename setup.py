#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='CrownstoneYodiwo',
    version='0.0.0',
    packages=find_packages(),
    install_requires=[
        'Yodiwo==0.0.1',
        'BluenetLib'
    ]
)