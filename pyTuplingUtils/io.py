#!/usr/bin/env python3
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Wed Oct 16, 2019 at 02:55 PM -0400

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


def gen_histo(array, bins=200, scale=1.05):
    min = array.min()
    max = array.max()

    min = min*scale if min < 0 else min/scale
    max = max/scale if max < 0 else max*scale

    return np.histogram(array, bins, (min, max))
