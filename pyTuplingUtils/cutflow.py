#!/usr/bin/env python3
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Fri May 01, 2020 at 04:03 AM +0800

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
        for r in self.rules:
            idx = self.find_idx(r.compare_to)

            try:
                prev_output = self.result[self.rules[idx].cond].output
            except Exception:
                prev_output = self.init_num

            if not r.explicit:
                self.prev_conds.append(r.cond)
                cond = '&'.join(self.prev_conds)
            else:
                cond = r.cond

            output = sum(self.exe.eval(cond))
            cut_result = {'input': prev_output, 'output': output}

            if cond.name:
                cut_result['name'] = cond.name

            self.result[cond] = cut_result

        return result

    @staticmethod
    def find_idx(raw_idx):
        if isinstance(raw_idx, str):  # relative index
            _, idx = raw_idx.split(':')
        else:
            idx = raw_idx

        return int(idx)
