#!/usr/bin/env python3
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Mon May 04, 2020 at 01:29 AM +0800

import numpy as np

from collections import OrderedDict as odict


def read_branch(ntp, tree, branch, idx=None):
    data = ntp[tree].array(branch)

    if not idx:
        return data
    else:
        return data[idx]


def read_branches(ntp, tree, branches, idx=None, transpose=False):
    data = ntp[tree].arrays(branches).values()

    if idx is not None:
        data = [d[idx] for d in data]

    if transpose:
        return np.column_stack(data)
    else:
        return data
