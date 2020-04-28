#!/usr/bin/env python3
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Wed Apr 29, 2020 at 03:25 AM +0800

from pyparsing import Group

from pyTuplingUtils.boolean.tokens import VAR, INT
from pyTuplingUtils.boolean.tokens import ADD, SUB


EXPR = Group((VAR | INT) + (ADD | SUB) + (VAR | INT))
