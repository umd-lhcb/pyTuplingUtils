#!/usr/bin/env python
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Sun Jun 13, 2021 at 12:52 AM +0200

import mplhep as hep

from pyTuplingUtils.argparse import (
    single_branch_parser_no_output, DataPairAction, split_ntp_tree)


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

    parser.add_argument('-YD', '--y-data-range',
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

    parser.add_argument('-c', '--colors',
                        default=None,
                        action='append',
                        nargs='+',
                        help='specify plot colors.')

    parser.add_argument('--y-axis-scale',
                        nargs='?',
                        default='linear',
                        help='y axis scale (linear or log).')

    parser.add_argument('--normalize',
                        action='store_true',
                        help='normalize plots to 1.')

    parser.add_argument('--debug',
                        action='store_true',
                        help='enable debug mode.')

    return parser.parse_args()


########
# Main #
########

if __name__ == '__main__':
    args = parse_input()
    hep.style.use('LHCb2')

    first_plot = True
    if not args.x_data_range:
        xmin = xmax = 0
    if not args.y_data_range:
        ymin = ymax = 0
    if not args.colors:
        args.colors = [['cornflowerblue', 'black', 'darkgoldenrod', 'oliverab']]

    for ntp_tree, branches, colors, labels, in zip(
            args.ref, args.ref_branch, args.labels, args.colors):
        ntp, tree = split_ntp_tree(ntp_tree)
        if args.debug:
            print('Working on: {}, tree: {}'.format(ntp, tree))

        for br, clr, lbl in zip(branches, colors, labels):
            if args.debug:
                print('  with branch: {}, color: {}, label: {}.'.format(
                    br, clr, lbl))
