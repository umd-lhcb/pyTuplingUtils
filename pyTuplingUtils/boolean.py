#!/usr/bin/env python3
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Wed Apr 29, 2020 at 04:37 PM +0800

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

VAR = Word(alphanums + '_')

INT = Word(nums)

TERMINAL = VAR | INT


#############
# Operators #
#############

class OpNode:
    def __init__(self):
        self.operator = None
        self.operands = None

    def __repr__(self):
        return "{}({}) : {!r}".format(self.__class__.__name__,
                                      self.operator, self.operands)


class UnOp(OpNode):
    def __init__(self, tokens):
        self.operator = tokens[0][0]
        self.operands = [tokens[0][1]]


class BinOp(OpNode):
    def __init__(self, tokens):
        self.operator = tokens[0][1]
        self.operands = tokens[0][::2]


##########
# Syntax #
##########
# These objects can be used as: <obj>.parseString(<string>).asList()

EXPR = infixNotation(
    TERMINAL,
    [
        (oneOf('* /'), 2, opAssoc.LEFT, BinOp),
        (oneOf('+ -'), 2, opAssoc.LEFT, BinOp)
    ]
)
