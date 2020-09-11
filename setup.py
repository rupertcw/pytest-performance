#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import codecs
from setuptools import setup


def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return codecs.open(file_path, encoding='utf-8').read()


setup(
    name='pytest-performance',
    version='0.1.0',
    author='Rupert Cobbe-Warburton',
    author_email='rupertcw10@gmail.com',
    maintainer='Rupert Cobbe-Warburton',
    maintainer_email='rupertcw10@gmail.com',
    license='MIT',
    url='https://github.com/rupertcw/pytest-performance',
    description='A simple plugin to ensure the execution of '
                'critical sections of code has not been impacted',
    long_description=read('README.rst'),
    py_modules=['pytest_performance'],
    python_requires='>=3.7',
    install_requires=['pytest>=3.7.0', 'pint>=0.15,<1.0', 'numpy'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Framework :: Pytest',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: Implementation :: CPython',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
    ],
    entry_points={
        'pytest11': [
            'performance = pytest_performance',
        ],
    },
)
