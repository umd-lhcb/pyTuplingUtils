# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Wed Apr 29, 2020 at 03:02 AM +0800

import setuptools

from distutils.core import setup

from pyTuplingUtils import version


###########
# Helpers #
###########

with open('README.md', 'r') as ld:
    long_description = ld.read()


#########
# Setup #
#########

setup(
    name='pyTuplingUtils',
    version=version,
    author='Yipeng Sun',
    author_email='syp@umd.edu',
    description='Utilities for n-tuples, such as plotting and simple debugging, with the help of uproot',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/umd-lhcb/pyTuplingUtils',
    packages=setuptools.find_packages(),
    scripts=['bin/uidcommon', 'bin/uiddump'],
    include_package_data=True,
    install_requires=[
        'uproot',
        'lz4',
        'numpy',
        'matplotlib',
        'pyparsing'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent'
    ]
)
