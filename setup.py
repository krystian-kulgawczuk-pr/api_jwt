# !/usr/bin/env python
__version__ = "1.2.0"

from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()


setup(
    name='api_jwt',
    version=__version__,
    description='Library for JWT encoding/decoding specifically adapted to use in microservices APIs',
    long_description=readme(),
    author='Greger Wedel',
    author_email='greger@greger.io',
    license='APACHE2',
    url='https://bitbucket.org/hudya/api_jwt/',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: APACHE2 License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Topic :: System :: Distributed Computing',
    ],
    py_modules=['api_jwt', ],
    install_requires=[
        'pyjwt>=1.6.1',
        'cryptography',
    ],
    include_package_data=True
)
