#!/usr/bin/env python3
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Fri May 01, 2020 at 01:33 AM +0800

import unittest
import uproot
import numpy as np

from context import pyTuplingUtils as ptu

evaluator = ptu.boolean.eval.BooleanEvaluator
rb = ptu.io.read_branch


class ArithmeticTest(unittest.TestCase):
    ntp = uproot.open('samples/sample.root')
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
        self.assertTrue(np.array_equal(
            self.exe.eval('Y_ISOLATION_BDT3'),
            rb(self.ntp, self.tree, 'Y_ISOLATION_BDT3')))

    ###########
    # product #
    ###########

    def test_mul(self):
        self.assertEqual(self.exe.eval('3*pi'), 3*3.14)

    def test_div(self):
        self.assertEqual(self.exe.eval('g/pi'), 9.8/3.14)

    def test_mul_div(self):
        self.assertEqual(self.exe.eval('3*(g/pi)'), 3*(9.8/3.14))

    #######
    # sum #
    #######

    def test_add(self):
        self.assertEqual(self.exe.eval('-3+pi'), -3+3.14)

    def test_sub(self):
        self.assertEqual(self.exe.eval('3-pi'), 3-3.14)

    def test_arith(self):
        self.assertEqual(self.exe.eval('3*(pi+3)/(g-2)'), 3*(3.14+3)/(9.8-2))


if __name__ == '__main__':
    unittest.main()
