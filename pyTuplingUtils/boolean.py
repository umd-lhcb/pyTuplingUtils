#!/usr/bin/env python3
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Wed Apr 29, 2020 at 03:36 PM +0800

from pyparsing import Suppress, Literal, Word
from pyparsing import alphanums, nums
from pyparsing import infixNotation, opAssoc, oneOf


##########
# Tokens #
##########

# LPAR = Suppress('(')
# RPAR = Suppress(')')

# ADD = Literal('+')
# SUB = Literal('-')

VAR = Word(alphanums + '_') | Word(alphanums)

INT = Word(nums)

TERMINAL = VAR | INT


##########
# Syntax #
##########

EXPR = infixNotation(
    TERMINAL,
    [
        (oneOf('* /'), 2, opAssoc.LEFT),
        (oneOf('+ -'), 2, opAssoc.LEFT)
    ]
)
