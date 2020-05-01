#!/usr/bin/env python3
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Fri May 01, 2020 at 05:53 PM +0800

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


def yaml_gen(data, indent='', indent_increment=' '*4):
    result = ''
    for key, items in data.items():
        result += '{}{}:'.format(indent, key)
        if type(items) in [dict, odict]:
            result += '\n'
            result += yaml_gen(items, indent=indent+indent_increment)
        else:
            result += ' {}\n'.format(items)
    return result
