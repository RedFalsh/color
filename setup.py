#!/usr/bin/env python

from configparser import ConfigParser
from setuptools import setup

import sys
import os

config = ConfigParser()
config.read(os.path.join(os.getcwd(), 'setup.cfg'))
metadata = config['metadata']
packages = config['files']

readme = os.path.join(os.path.dirname(__file__), metadata['description-file'])

setup(
    name=metadata['name'],
    version=metadata['version'],
    license=metadata['license'],
    author=metadata['author'],
    url=metadata['home-page'],
    description=metadata['summary'],
    long_description=open(readme).read(),
    keywords=metadata['keywords'],
    classifiers=metadata['classifiers'].split('\n')[1:],
    install_requires=['distribute'],
    packages=packages['packages'].split('\n')[1:],
    include_package_data=True,
    zip_safe=True
)
