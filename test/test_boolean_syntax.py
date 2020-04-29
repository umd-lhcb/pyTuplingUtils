#!/usr/bin/env python3
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Wed Apr 29, 2020 at 05:18 PM +0800

import unittest

from context import pyTuplingUtils as ptu


class AddSubTest(unittest.TestCase):
    def test_add(self):
        result = ptu.boolean.EXPR.parseString('a + 3').asList()

        self.assertEqual(result[0].operator, '+')
        self.assertEqual(result[0].operands, ['a', '3'])


if __name__ == '__main__':
    unittest.main()
