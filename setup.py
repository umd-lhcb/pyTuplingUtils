# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Thu Oct 17, 2019 at 02:40 AM -0400

import setuptools

from distutils.core import setup

VERSION = 0.1


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
    version=VERSION,
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
        'uproot'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent'
    ]
)
