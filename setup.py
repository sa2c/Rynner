#!/usr/bin/env python

from distutils.core import setup

setup(
        name='Rynner',
        version='0.0.0',
        url='https://github.com/M4rkD/Rynner/',
        py_modules=['rynner'],
        install_requires =['libsubmit','pathlib','python-box','paramiko'],
        dependency_links=[
            "git+ssh://git@github.com/M4rkD/libsubmit.git"
        ]
    )
