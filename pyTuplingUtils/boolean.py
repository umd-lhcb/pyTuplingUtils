#!/usr/bin/env python3
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Wed Apr 29, 2020 at 07:41 PM +0800

from pyparsing import Word, Combine
from pyparsing import alphanums, nums
from pyparsing import infixNotation, opAssoc, oneOf, ZeroOrMore

##########
# Tokens #
##########

VAR = Word(alphanums + '_')
INT = Word(nums).setParseAction(lambda x: int(x[0]))
FLOAT = Combine(ZeroOrMore(Word(nums))+'.'+Word(nums)).setParseAction(
    lambda x: float(x[0]))

TERMINAL = FLOAT | INT | VAR


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
        (oneOf('+ -'), 1, opAssoc.RIGHT, UnOp),
        (oneOf('* /'), 2, opAssoc.LEFT,  BinOp),
        (oneOf('+ -'), 2, opAssoc.LEFT,  BinOp)
    ]
)
