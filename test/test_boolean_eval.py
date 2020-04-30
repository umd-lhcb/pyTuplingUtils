#!/usr/bin/env python3
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Fri May 01, 2020 at 12:37 AM +0800

import unittest
import uproot

from context import pyTuplingUtils as ptu

evaluator = ptu.boolean.eval.BooleanEvaluator
rb = ptu.io.read_branch


class ArithmeticTest(unittest.TestCase):
    ntp = uproot.open('../samples/sample.root')
    tree = 'TupleB0/DecayTree'
    known_syml = {
        'pi': 3.14,
        'e': 2.72,
        'g': 9.8,
    }
    exe = evaluator(ntp, tree, known_syml=known_syml)

    ########
    # atom #
    ########

    def test_num(self):
        self.assertEqual(self.exe.eval('-1'), -1)

    def test_bool(self):
        self.assertTrue(self.exe.eval('true'))
        self.assertFalse(self.exe.eval('false'))

    def test_known_syml(self):
        self.assertEqual(self.exe.eval('g'), 9.8)
        self.assertEqual(self.exe.eval('-pi'), -3.14)

    def test_var(self):
        self.assertEqual(self.exe.eval('Y_ISOLATION_BDT3').all(),
                         rb(self.ntp, self.tree, 'Y_ISOLATION_BDT3').all())


if __name__ == '__main__':
    unittest.main()
