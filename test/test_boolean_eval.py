#!/usr/bin/env python3
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Fri May 01, 2020 at 12:11 AM +0800

import unittest

from context import pyTuplingUtils as ptu

evaluator = ptu.boolean.eval.BooleanEvaluator


class ArithmeticTest(unittest.TestCase):
    ntp = '../samples/sample.root'
    tree = 'TupleB0/DecayTree'
    known_syml = {
        'pi': 3.14,
        'e': 2.72,
        'g': 9.8,
    }
    exe = evaluator(ntp, tree, known_syml=known_syml)

    def test_num(self):
        self.assertEqual(self.exe.eval('-1'), -1)

    def test_known_syml(self):
        self.assertEqual(self.exe.eval('g'), 9.8)
        self.assertEqual(self.exe.eval('-pi'), -3.14)


if __name__ == '__main__':
    unittest.main()
