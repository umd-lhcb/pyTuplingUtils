#!/usr/bin/env python3
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Wed Apr 29, 2020 at 07:46 PM +0800

import unittest

from context import pyTuplingUtils as ptu


class AddSubTest(unittest.TestCase):
    def test_add(self):
        result = ptu.boolean.EXPR.parseString('a + 3').asList()

        self.assertEqual(result[0].operator, '+')
        self.assertEqual(result[0].operands, ['a', 3])

    def test_mul(self):
        result = ptu.boolean.EXPR.parseString('a * 3').asList()

        self.assertEqual(result[0].operator, '*')
        self.assertEqual(result[0].operands, ['a', 3])

    def test_add_mul_precedence1(self):
        result = ptu.boolean.EXPR.parseString('a * 3+b').asList()

        self.assertEqual(result[0].operator, '+')
        self.assertEqual(result[0].operands[1], 'b')
        self.assertEqual(result[0].operands[0].operator, '*')
        self.assertEqual(result[0].operands[0].operands, ['a', 3])

    def test_add_mul_precedence2(self):
        result = ptu.boolean.EXPR.parseString('a * (3+b)').asList()

        self.assertEqual(result[0].operator, '*')
        self.assertEqual(result[0].operands[0], 'a')
        self.assertEqual(result[0].operands[1].operator, '+')
        self.assertEqual(result[0].operands[1].operands, [3, 'b'])


if __name__ == '__main__':
    unittest.main()
