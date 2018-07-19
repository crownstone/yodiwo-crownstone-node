#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='CrownstoneYodiwo',
    version='0.2.0',
    packages=find_packages(),
    install_requires=[
        'Yodiwo==0.2.0',
        'BluenetLib==0.5.1'
    ],
    dependency_links=[
        'https://github.com/crownstone/yodiwo-python-node/tarball/0.2.0#egg=Yodiwo-0.2.0',
        'https://github.com/crownstone/bluenet-python-lib/tarball/0.5.1#egg=BluenetLib-0.5.1'
    ]
)