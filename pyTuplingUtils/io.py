#!/usr/bin/env python3
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Wed Jun 24, 2020 at 08:35 PM +0800

import numpy as np

from collections import OrderedDict as odict


def read_branch(ntp, tree, branch, idx=None):
    data = ntp[tree].array(branch)

    if not idx:
        return data
    else:
        return data[idx]


def read_branches_dict(ntp, tree, branches):
    return {k.decode('utf-8'): v for k, v in ntp[tree].arrays(branches).items()}


def read_branches(ntp, tree, branches, idx=None, transpose=False):
    data = ntp[tree].arrays(branches).values()

    if idx is not None:
        data = [d[idx] for d in data]

    if transpose:
        return np.column_stack(data)
    else:
        return list(data)
