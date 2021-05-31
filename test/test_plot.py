#!/usr/bin/env python3
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Mon May 31, 2021 at 02:59 AM +0200

import unittest

from context import pyTuplingUtils as ptu
from context import pwd


class FilterKwargsFuncTest(unittest.TestCase):
    @staticmethod
    def test_func(a=1, b=2):
        pass

    def test_args(self):
        kwargs = {'a': 2, 'c': 3, 'd': 4}
        kw_known, kw_rest = ptu.plot.filter_kwargs_func(kwargs, self.test_func)

        assert kw_known == {'a': 2}
        assert kw_rest == {'c': 3, 'd': 4}
