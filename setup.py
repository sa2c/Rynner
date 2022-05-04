#!/usr/bin/env python

from distutils.core import setup

setup(
        name='Rynner',
        version='0.0.1',
        url='https://github.com/sa2c/Rynner',
        py_modules=['rynner','tests'],
        install_requires=['parsl', 'paramiko']  # todo improve setup
    )
