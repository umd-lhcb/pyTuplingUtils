#!/usr/bin/env python3
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Mon Mar 08, 2021 at 01:29 AM +0100

import numpy as np

ARRAY_TYPE = 'np'


def read_branch(ntp, tree, branch, idx=None):
    data = ntp[tree][branch].array(library=ARRAY_TYPE)

    return data if not idx else data[idx]


def read_branches_dict(ntp, tree, branches):
    return {k: v for k, v
            in ntp[tree].arrays(branches, library=ARRAY_TYPE).items()}


def read_branches(ntp, tree, branches, idx=None, transpose=False):
    data = ntp[tree].arrays(branches, library=ARRAY_TYPE).values()

    if idx is not None:
        data = [d[idx] for d in data]

    return np.column_stack(data) if transpose else list(data)
