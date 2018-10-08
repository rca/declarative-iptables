#!/usr/bin/env python
from setuptools import find_packages, setup

SRC_PREFIX = 'src'

packages = find_packages(SRC_PREFIX)

def readme():
    with open('README.md') as f:
        return f.read()


setup(
    name='declarative-iptables',
    url='https://github.com/rca/declarative-iptables',
    author='Roberto Aguilar',
    author_email='roberto.c.aguilar@gmail.com',
    version='0.0.0',
    description='work with iptables in a declarative manner',
    long_description=readme(),
    long_description_content_type='text/markdown',
    package_dir={'':'src'},
    packages=packages
)
