#!/usr/bin/env python3
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Fri May 01, 2020 at 07:15 PM +0800

import fileinput

from argparse import ArgumentParser, Action
from pyTuplingUtils.utils import tabl as TAB


################################
# Command line argument parser #
################################

class ColAlignmentAct(Action):
    def __call__(self, parser, namespace, value, option_string=None):
        if ',' not in value:
            setattr(namespace, self.dest, [value])
        else:
            setattr(namespace, self.dest, value.split(','))


def parse_input(descr='table generator taking stdin as input.'):
    parser = ArgumentParser(description=descr)

    parser.add_argument('-f', '--format',
                        nargs='?',
                        choices=['latex',
                                 'simple',
                                 'github',
                                 'latex_booktabs',
                                 'latex_booktabs_raw',
                                 'latex_raw'],
                        default='github',
                        help='specify the output table format.'
                        )

    parser.add_argument('-a', '--alignment',
                        action=ColAlignmentAct,
                        default=None,
                        help='specify the alignment for each column (right, center, left).')

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_input()

    output = []
    for l in fileinput.input(files=('-',)):
        row = l.rstrip().split(',')
        # Strip out head and tail whitespace unconditionally
        row = [x.strip() for x in row]
        output.append(row)

    if args.alignment is not None:
        print(TAB.tabulate(output, headers='firstrow', tablefmt=args.format,
                           colalign=args.alignment))
    else:
        print(TAB.tabulate(output, headers='firstrow', tablefmt=args.format))
