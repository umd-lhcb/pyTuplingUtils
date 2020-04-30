#!/usr/bin/env python3
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Fri May 01, 2020 at 04:34 AM +0800

import unittest
import uproot
import os.path as osp
import numpy as np

from context import pyTuplingUtils as ptu
from context import pwd

print(pwd)

evaluator = ptu.boolean.eval.BooleanEvaluator
rb = ptu.io.read_branch


class ArithmeticTest(unittest.TestCase):
    ntp = uproot.open(osp.join(pwd, '../samples/sample.root'))
    tree = 'TupleB0/DecayTree'
    known_sym = {
        'pi': 3.14,
        'e': 2.72,
        'g': 9.8,
    }
    exe = evaluator(ntp, tree, known_sym=known_sym)

    ########
    # atom #
    ########

    def test_num(self):
        self.assertEqual(self.exe.eval('-1'), -1)
        self.assertEqual(type(self.exe.eval('-1')), int)
        self.assertEqual(type(self.exe.eval('1.85')), float)

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


class BooleanTest(unittest.TestCase):
    ntp = uproot.open(osp.join(pwd, '../samples/sample.root'))
    tree = 'TupleB0/DecayTree'
    known_sym = {
        'pi': 3.14,
        'e': 2.72,
        'g': 9.8,
    }
    exe = evaluator(ntp, tree, known_sym=known_sym)

    ##############
    # complement #
    ##############

    def test_comp(self):
        self.assertFalse(self.exe.eval('!true'))

    ##############
    # comparison #
    ##############

    def test_eq(self):
        self.assertTrue(self.exe.eval('!true == false'))

    def test_neq(self):
        self.assertFalse(self.exe.eval('!True != False'))  # case doesn't matter

    def test_gt(self):
        self.assertTrue(self.exe.eval('3 > 2'))

    def test_gte(self):
        self.assertTrue(self.exe.eval('pi >= 3'))

    ###########
    # boolean #
    ###########

    def test_andop(self):
        self.assertTrue(self.exe.eval('true & true'))
        self.assertFalse(self.exe.eval('true & false'))
        self.assertFalse(self.exe.eval('false & true'))
        self.assertFalse(self.exe.eval('false & false'))

    def test_orop(self):
        self.assertTrue(self.exe.eval('true | true'))
        self.assertTrue(self.exe.eval('true | false'))
        self.assertTrue(self.exe.eval('false | true'))
        self.assertFalse(self.exe.eval('false | false'))

    def test_andop_orop(self):
        self.assertTrue(self.exe.eval('false | true & true'))
        self.assertFalse(self.exe.eval('false | false & true'))

    def test_bool(self):
        self.assertTrue(self.exe.eval('(pi > e) & true | false'))
        self.assertFalse(self.exe.eval('(pi <= e) & (true | false)'))


if __name__ == '__main__':
    unittest.main()
