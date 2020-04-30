#!/usr/bin/env python3
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Thu Apr 30, 2020 at 11:38 PM +0800

from lark import Transformer, v_args

from pyTuplingUtils.io import read_branch
from pyTuplingUtils.boolean.syntax import boolean_parser


class TransForTupling(Transformer):
    def __init__(self, ntp, tree, known_syml=dict()):
        self.ntp = ntp
        self.tree = tree
        self.cache = {}
        self.cache.update(known_syml)

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
            return self.cache[val]
        except KeyError:
            result = read_branch(self.ntp, self.tree, val)
            self.cache[val] = result
            return result


class BooleanEvaluator(object):
    def __init__(self, *args, transformer=TransForTupling, **kwargs):
        self.parser = boolean_parser.parse
        self.transformer = transformer(*args, **kwargs)

    def parse(self, s):
        return self.parser(s)

    def eval(self, s):
        tree = self.parse(s)
        return self.transformer.transform(tree)
