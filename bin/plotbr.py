#!/usr/bin/env python
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Sat Jun 12, 2021 at 11:31 PM +0200

import mplhep as hep

from pyTuplingUtils.argparse import (
    single_branch_parser_no_output, DataPairAction)


################################
# Command line argument parser #
################################

def parse_input(descr='plot branches from ntuples.'):
    parser = single_branch_parser_no_output(descr)

    parser.add_argument('-XD', '--x-data-range',
                        nargs=2,
                        action=DataPairAction,
                        default=None,
                        help='specify x-axis range.')

    parser.add_argument('-YD', '--x-data-range',
                        nargs=2,
                        action=DataPairAction,
                        default=None,
                        help='specify y-axis range.')

    parser.add_argument('-XL' '--xlabel',
                        default=None,
                        help='specify x-axis label.')

    parser.add_argument('-YL' '--ylabel',
                        default=None,
                        help='specify y-axis label.')

    parser.add_argument('-l', '--labels',
                        required=True,
                        action='append',
                        nargs='+',
                        help='specify plot legend labels.')

    parser.add_argument('--y-axis-scale',
                        nargs='?',
                        default='linear',
                        help='y axis scale (linear or log).')

    parser.add_argument('--normalize',
                        action='store_true',
                        help='normalize plots to 1.')

    return parser.parse_args()


########
# Main #
########

if __name__ == '__main__':
    args = parse_input()
    hep.style.use('LHCb2')
