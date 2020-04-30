#!/usr/bin/env python3
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Fri May 01, 2020 at 12:03 AM +0800

import unittest

from context import pyTuplingUtils as ptu

evaluator = ptu.boolean.eval.BooleanEvaluator


class ArithmeticTest(unittest.TestCase):
    ntp = '../samples/sample.root'
    tree = 'TupleB0/DecayTree'
    exe = evaluator(ntp, tree)

    def test_num(self):
        self.assertEqual(
            self.exe.eval('-1'),
            -1
        )


if __name__ == '__main__':
    unittest.main()
