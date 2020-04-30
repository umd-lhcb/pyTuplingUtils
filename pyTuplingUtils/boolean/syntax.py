#!/usr/bin/env python3
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Thu Apr 30, 2020 at 06:28 PM +0800

from lark import Lark


boolean_grammar = '''
    ?start: cond

    ?cond: expr
        | cond "==" cond    -> eq
        | cond "!=" cond    -> neq
        | cond ">"  cond    -> gt
        | cond ">=" cond    -> gte
        | cond "<"  cond    -> lt
        | cond "<=" cond    -> lte

    ?expr: sum
        | "!" sum           -> comp  // logical complement

    ?sum: product
        | sum "+" product   -> add
        | sum "-" product   -> sub

    ?product: atom
        | product "*" atom  -> mul
        | product "/" atom  -> div

    ?atom: NUMBER           -> num
        | "-" atom          -> neg
        | NAME              -> var
        | "(" sum ")"

    %import common.SIGNED_NUMBER -> NUMBER
    %import common.WS_INLINE
    %import common.CNAME -> NAME

    %ignore WS_INLINE
'''

boolean_parser = Lark(boolean_grammar, parser='lalr')
