#!/usr/bin/env python3
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Thu Apr 30, 2020 at 03:59 AM +0800

import unittest

from context import pyTuplingUtils as ptu

parser = ptu.boolean.syntax.boolean_parser.parse


class AddSubTest(unittest.TestCase):
    def test_var(self):
        self.assertEqual(
            parser('a').pretty(),
            "var\ta\n"
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

    def test_negative_num(self):
        self.assertEqual(
            parser('-1.6').pretty(),
            "neg\n"
            "  num\t1.6\n"
        )
        self.assertEqual(
            parser('-1').pretty(),
            "neg\n"
            "  num\t1\n"
        )

    def test_add(self):
        self.assertEqual(
            parser('-1 +2.3').pretty(),
            "add\n"
            "  neg\n"
            "    num\t1\n"
            "  num\t2.3\n"
        )

    def test_add_sub(self):
        self.assertEqual(
            parser('-1 +2.3 - 10').pretty(),
            "sub\n"
            "  add\n"
            "    neg\n"
            "      num\t1\n"
            "    num\t2.3\n"
            "  num\t10\n"
        )

    def test_add_mul(self):
        self.assertEqual(
            parser('-1 +2.3 * 10').pretty(),
            "add\n"
            "  neg\n"
            "    num\t1\n"
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


if __name__ == '__main__':
    unittest.main()
