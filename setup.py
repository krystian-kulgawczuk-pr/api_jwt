# !/usr/bin/env python
__version__ = "0.0.1"

from setuptools import setup

setup(
    name='api_jwt',
    version=__version__,
    description='Common library for JWT encoding/decoding, see auth ms for usage',
    author='Hudya Team',
    author_email='admin@hudya.io',
    url='https://bitbucket.org/hudya/api_jwt/',
    packages=['api_jwt', ],
    install_requires=[
        'pyjwt>1.5'
    ],
)
