#!/usr/bin/env python3
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Thu Apr 30, 2020 at 07:53 PM +0800

import unittest

from context import pyTuplingUtils as ptu

parser = ptu.boolean.syntax.boolean_parser.parse


class ArithmeticTest(unittest.TestCase):
    def test_var(self):
        self.assertEqual(
            parser('a').pretty(),
            "var\ta\n"
        )
        self.assertEqual(
            parser('-a').pretty(),
            "neg\n"
            "  var\ta\n"
        )
        self.assertEqual(
            parser('a1').pretty(),
            "var\ta1\n"
        )
        self.assertEqual(
            parser('a_1b').pretty(),
            "var\ta_1b\n"
        )

    def test_num(self):
        self.assertEqual(
            parser('1').pretty(),
            "num\t1\n"
        )
        self.assertEqual(
            parser('+1').pretty(),
            "num\t+1\n"
        )

    def test_negative_num(self):
        self.assertEqual(
            parser('-1.6').pretty(),
            "num\t-1.6\n"
        )
        self.assertEqual(
            parser('+1').pretty(),
            "num\t+1\n"
        )

    def test_add(self):
        self.assertEqual(
            parser('-1 +2.3').pretty(),
            "add\n"
            "  num\t-1\n"
            "  num\t2.3\n"
        )

    def test_add_sub(self):
        self.assertEqual(
            parser('-1 +2.3 - 10').pretty(),
            "sub\n"
            "  add\n"
            "    num\t-1\n"
            "    num\t2.3\n"
            "  num\t10\n"
        )

    def test_add_mul(self):
        self.assertEqual(
            parser('-1 +2.3 * 10').pretty(),
            "add\n"
            "  num\t-1\n"
            "  mul\n"
            "    num\t2.3\n"
            "    num\t10\n"
        )

    def test_add_mul_par(self):
        self.assertEqual(
            parser('-(1 +2.3) * 10').pretty(),
            "mul\n"
            "  neg\n"
            "    add\n"
            "      num\t1\n"
            "      num\t2.3\n"
            "  num\t10\n"
        )


class BooleanTest(unittest.TestCase):
    def test_comp(self):
        self.assertEqual(
            parser('!(-a_2 +2.3) ').pretty(),
            "comp\n"
            "  add\n"
            "    neg\n"
            "      var\ta_2\n"
            "    num\t2.3\n"
        )

    def test_eq(self):
        self.assertEqual(
            parser('a == b').pretty(),
            "eq\n"
            "  var\ta\n"
            "  var\tb\n"
        )
        self.assertEqual(
            parser('a == 1').pretty(),
            "eq\n"
            "  var\ta\n"
            "  num\t1\n"
        )
        self.assertEqual(
            parser('a <= -1+x').pretty(),
            "lte\n"
            "  var\ta\n"
            "  add\n"
            "    num\t-1\n"
            "    var\tx\n"
        )

    def test_bool(self):
        self.assertEqual(
            parser('a & 1').pretty(),
            "and\n"
            "  var\ta\n"
            "  num\t1\n"
        )
        self.assertEqual(
            parser('True | False').pretty(),
            "or\n"
            "  bool\tTrue\n"
            "  bool\tFalse\n"
        )
        self.assertEqual(
            parser('True | False & True').pretty(),
            "or\n"
            "  bool\tTrue\n"
            "  and\n"
            "    bool\tFalse\n"
            "    bool\tTrue\n"
        )

    def test_comb(self):
        self.assertEqual(
            parser('a >= !(-1+x)*3').pretty(),
            "gte\n"
            "  var\ta\n"
            "  comp\n"
            "    mul\n"
            "      add\n"
            "        num\t-1\n"
            "        var\tx\n"
            "      num\t3\n"
        )


if __name__ == '__main__':
    unittest.main()