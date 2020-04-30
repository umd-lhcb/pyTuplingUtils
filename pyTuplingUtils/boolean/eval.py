#!/usr/bin/env python3
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Fri May 01, 2020 at 03:49 AM +0800

from lark import Transformer, v_args

from numpy import logical_and as AND, logical_or as OR, logical_not as NOT
from pyTuplingUtils.io import read_branch
from pyTuplingUtils.boolean.syntax import boolean_parser


class TransForTupling(Transformer):
    def __init__(self, ntp, tree, known_sym=dict()):
        self.ntp = ntp
        self.tree = tree
        self.cache = {}
        self.cache.update(known_sym)

    ########
    # atom #
    ########

    @v_args(inline=True)
    def num(self, val):
        try:
            return int(val)
        except ValueError:
            return float(val)

    @v_args(inline=True)
    def bool(self, val):
        return True if val.lower() == 'true' else False

    @v_args(inline=True)
    def var(self, val):
        try:
            return self.cache[val.value]
        except KeyError:
            result = read_branch(self.ntp, self.tree, val.value)
            self.cache[val.value] = result
            return result

    @v_args(inline=True)
    def neg(self, val):
        return -val

    ###########
    # product #
    ###########

    @v_args(inline=True)
    def mul(self, arg1, arg2):
        return arg1 * arg2

    @v_args(inline=True)
    def div(self, arg1, arg2):
        return arg1 / arg2

    #######
    # sum #
    #######

    @v_args(inline=True)
    def add(self, arg1, arg2):
        return arg1 + arg2

    @v_args(inline=True)
    def sub(self, arg1, arg2):
        return arg1 - arg2

    ##############
    # complement #
    ##############

    @v_args(inline=True)
    def comp(self, cond):
        return NOT(cond)

    ##############
    # comparison #
    ##############

    @v_args(inline=True)
    def eq(self, lhs, rhs):
        return lhs == rhs

    @v_args(inline=True)
    def neq(self, lhs, rhs):
        return lhs != rhs

    @v_args(inline=True)
    def gt(self, lhs, rhs):
        return lhs > rhs

    @v_args(inline=True)
    def gte(self, lhs, rhs):
        return lhs >= rhs

    @v_args(inline=True)
    def lt(self, lhs, rhs):
        return lhs < rhs

    @v_args(inline=True)
    def lte(self, lhs, rhs):
        return lhs <= rhs

    ###########
    # boolean #
    ###########

    @v_args(inline=True)
    def andop(self, cond1, cond2):
        return AND(cond1, cond2)

    @v_args(inline=True)
    def orop(self, cond1, cond2):
        return OR(cond1, cond2)


class BooleanEvaluator(object):
    def __init__(self, *args, transformer=TransForTupling, **kwargs):
        self.parser = boolean_parser.parse
        self.transformer = transformer(*args, **kwargs)

    def parse(self, s):
        return self.parser(s)

    def eval(self, s):
        tree = self.parse(s)
        return self.transformer.transform(tree)
