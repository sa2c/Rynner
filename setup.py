#!/usr/bin/env python

from distutils.core import setup

from setuptools import find_packages

install_requires = [
    "paramiko",
    "parsl",
]

setup(
    name="rynner",
    version="0.0.1",
    url="https://github.com/sa2c/Rynner",
    packages=find_packages(),
    install_requires=install_requires,
    py_modules=["rynner"],
)
