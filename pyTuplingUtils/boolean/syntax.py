#!/usr/bin/env python3
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Fri May 01, 2020 at 01:58 AM +0800

from lark import Lark


boolean_grammar = '''
    ?start: boolor

    ?boolor: booland
        | boolor "|" booland -> orop

    ?booland: cond  // '&' binds tigher than '|'
        | booland "&" cond   -> andop

    ?cond: expr
        | cond "==" expr     -> eq
        | cond "!=" expr     -> neq
        | cond ">"  expr     -> gt
        | cond ">=" expr     -> gte
        | cond "<"  expr     -> lt
        | cond "<=" expr     -> lte

    ?expr: sum
        | "!" sum            -> comp  // logical complement

    ?sum: product
        | sum "+" product    -> add
        | sum "-" product    -> sub

    ?product: atom
        | product "*" atom   -> mul
        | product "/" atom   -> div

    ?atom: NUMBER            -> num
        | "-" atom           -> neg
        | BOOL               -> bool
        | NAME               -> var
        | "(" boolor ")"

    %import common.SIGNED_NUMBER -> NUMBER
    %import common.WS_INLINE
    %import common.CNAME -> NAME

    %ignore WS_INLINE

    BOOL.2: "True" | "False" | "true" | "false"  // These keywords have higher priority
'''

boolean_parser = Lark(boolean_grammar, parser='lalr')
