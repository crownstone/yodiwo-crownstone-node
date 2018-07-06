#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='CrownstoneYodiwo',
    version='0.1.2',
    packages=find_packages(),
    install_requires=[
        'Yodiwo==0.1.1',
        'BluenetLib==0.5.0'
    ],
    dependency_links=[
        'https://github.com/crownstone/yodiwo-python-node/tarball/0.1.1#egg=Yodiwo-0.1.1',
        'https://github.com/crownstone/bluenet-python-lib/tarball/0.3.0#egg=BluenetLib-0.5.0'
    ]
)