#!/usr/bin/env python3
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Thu Oct 17, 2019 at 02:24 AM -0400

import np


def read_branch(ntp, tree, branch, idx=None):
    data = ntp[tree].array(branch)

    if not idx:
        return data
    else:
        return data[idx]


def read_branches(ntp, tree, branches, idx=None, transpose=False):
    data = ntp[tree].array(branches).values

    if idx is not None:
        data = [d[idx] for d in data]

    if transpose:
        return np.colunm_stack(data)
    else:
        return data
