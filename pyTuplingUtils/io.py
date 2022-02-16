#!/usr/bin/env python3
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Wed Feb 16, 2022 at 01:24 PM -0500

import numpy as np

from uproot import concatenate

ARRAY_TYPE = 'np'


def regulate_input(ntp, tree):
    if isinstance(ntp, str):
        return f'{ntp}:{tree}'
    if isinstance(ntp, list):
        return [regulate_input(i, tree) for i in ntp]
    return ntp[tree]


def read_branch(ntp, tree, branch, idx=None):
    data = list(concatenate(
        regulate_input(ntp, tree), branch, library=ARRAY_TYPE).values())[0]

    return data if not idx else data[idx]


def read_branches_dict(ntp, tree, branches):
    return concatenate(regulate_input(ntp, tree), branches, library=ARRAY_TYPE)


def read_branches(ntp, tree, branches, idx=None, transpose=False):
    data = list(read_branches_dict(ntp, tree, branches).values())

    if idx is not None:
        data = [d[idx] for d in data]

    return np.column_stack(data) if transpose else data
