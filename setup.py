#!/usr/bin/env python

from distutils.core import setup

setup(name='backupper',
    version='0.1',
    description='A utility to automatically create full and incremental backups.',
    author='Alex Seiler',
    author_email='seileralex@gmail.com',
    url='www.google.ch',
    packages=['backupper'],
    scripts=['backupper.py'])
