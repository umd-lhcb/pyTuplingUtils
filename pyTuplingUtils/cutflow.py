#!/usr/bin/env python3
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Fri May 01, 2020 at 02:38 PM +0800

import uproot

from dataclasses import dataclass
from typing import Union, Optional
from numpy import sum
from pyTuplingUtils.boolean.eval import BooleanEvaluator


@dataclass
class CutflowRule:
    cond: str = 'true'
    name: Optional[str] = None
    compare_to: Union[str, int] = 'r:-1'
    explicit: bool = False


class CutflowGen(object):
    def __init__(self, ntp_path, tree, rules, init_num,
                 result=dict(), **kwargs):
        self.rules = rules
        self.init_num = init_num
        self.result = result

        self.exe = BooleanEvaluator(uproot.open(ntp_path), tree, **kwargs)
        self.prev_conds = []

    def do(self):
        for idx, r in enumerate(self.rules):
            prev_idx = self.find_idx(idx, r.compare_to)

            try:
                prev_output = self.result[self.rules[prev_idx].cond]['output']
            except Exception:
                prev_output = self.init_num

            if not r.explicit:
                self.prev_conds.append(r.cond)
                cond = '&'.join(self.prev_conds)
            else:
                cond = r.cond

            output = sum(self.exe.eval(cond))
            cut_result = {'input': prev_output, 'output': output}

            if r.name:
                cut_result['name'] = r.name

            self.result[r.cond] = cut_result

        return self.result

    @staticmethod
    def find_idx(ref_idx, raw_idx):
        if isinstance(raw_idx, str):  # relative index
            _, idx = raw_idx.split(':')
            idx = ref_idx + int(idx)
        else:
            idx = int(raw_idx)

        return idx
