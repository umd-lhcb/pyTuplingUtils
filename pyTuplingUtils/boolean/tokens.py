#!/usr/bin/env python3
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Wed Apr 29, 2020 at 04:29 AM +0800

from pyparsing import Suppress, Literal, Word, alphanums, nums

LPAR = Suppress('(')
RPAR = Suppress(')')

ADD = Literal('+')
SUB = Literal('-')

VAR = Word(alphanums + '_')

INT = Word(nums)
