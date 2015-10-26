#!/usr/bin/env python

from distutils.core import setup

setup(name='backupper',
    version='0.1.3',
    description='A utility to automatically create full and incremental backups.',
    author='Alex Seiler',
    author_email='seileralex@gmail.com',
    url='https://github.com/goggle/backupper',
    packages=['Backupper'],
    scripts=['backupper'],
    data_files=[('/etc', ['backupper.conf'])]
    )
