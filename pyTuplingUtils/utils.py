#!/usr/bin/env python3
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Fri May 01, 2020 at 07:11 PM +0800

import numpy as np
import tabulate as tabl

from functools import partial
from .io import read_branch


# Disable LaTeX character escaping
tabl._table_formats["latex_booktabs_raw"] = tabl.TableFormat(
    lineabove=partial(tabl._latex_line_begin_tabular, booktabs=True),
    linebelowheader=tabl.Line("\\midrule", "", "", ""),
    linebetweenrows=None,
    linebelow=tabl.Line("\\bottomrule\n\\end{tabular}", "", "", ""),
    headerrow=partial(tabl._latex_row, escrules={}),
    datarow=partial(tabl._latex_row, escrules={}),
    padding=1,
    with_header_hide=None,
)


def extract_uid(ntp, tree, run_branch='runNumber', event_branch='eventNumber'):
    run = read_branch(ntp, tree, run_branch)
    event = read_branch(ntp, tree, event_branch)

    run = np.char.mod('%d', run)
    event = np.char.mod('%d', event)

    run = np.char.add(run, '-')
    ids = np.char.add(run, event)

    uid, idx, count = np.unique(ids, return_index=True, return_counts=True)
    uid = uid[count == 1]
    idx = idx[count == 1]

    total_size = ids.size
    uniq_size = uid.size
    dupl_size = total_size - uniq_size

    return uid, idx, total_size, uniq_size, dupl_size


def find_common_uid(ntp1, ntp2, tree1, tree2, **kwargs):
    uid1, idx1, _, _, _ = extract_uid(ntp1, tree1, **kwargs)
    uid2, idx2, _, _, _ = extract_uid(ntp2, tree2, **kwargs)
    uid_comm, uid_comm_idx1, uid_comm_idx2 = np.intersect1d(
        uid1, uid2, assume_unique=True, return_indices=True)

    return uid_comm, idx1[uid_comm_idx1], idx2[uid_comm_idx2]


def gen_histo(array, bins=200, scale=1.05, range=None):
    if range is None:
        min = array.min()
        max = array.max()

        min = min*scale if min < 0 else min/scale
        max = max/scale if max < 0 else max*scale

        return np.histogram(array, bins, (min, max))
    else:
        return np.histogram(array, bins, range)
