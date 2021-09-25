# -*- coding: utf-8 -*-

import os
import sys

import setuptools
from setuptools import find_packages, setup


def read(fname):
    with open(fname, 'r', encoding='UTF-8') as fp:
        content = fp.read()
    return content


if sys.version_info < (3, 5):
    sys.exit('Sorry, Python < 3.5 is not supported')

setup(
    name='lgbc',
    version='0.0.1',
    author='Ray Yang',
    author_email='yangruipis@163.com',
    description=('A machine learning algorithm implementation'),
    license='MIT',
    url='https://yangruipis.github.io/lgb-convertor/',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    packages=setuptools.find_packages(),
    # packages=[
    #     'lgb_convertor', 'lgb_convertor.cli', 'lgb_convertor.base',
    #     'lgb_convertor.lang'
    # ],
    package_data={'': ['*.md', '*.txt', '*.data']},
    include_package_data=True,
    install_requires=[],
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Microsoft',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    scripts=['cli/lgbc'],
    entry_points={'console_scripts': ['command-name = cli.lgbc',],},
)
