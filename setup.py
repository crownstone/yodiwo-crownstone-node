#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='CrownstoneYodiwo',
    version='0.0.0',
    packages=find_packages(),
    install_requires=[
        'Yodiwo==0.0.1',
        'BluenetLib'
    ],
    dependency_links=[
        'https://github.com/crownstone/yodiwo-python-node/tarball/master#egg=Yodiwo-0.0.1',
        'https://github.com/crownstone/bluenet-python-lib/tarball/master#egg=BluenetLib-0.0.2'
    ]
)