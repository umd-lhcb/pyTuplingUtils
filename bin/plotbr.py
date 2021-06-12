#!/usr/bin/env python
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Sun Jun 13, 2021 at 01:42 AM +0200

import uproot

import mplhep as hep
import matplotlib.pyplot as plt

from pyTuplingUtils.argparse import (
    single_branch_parser_no_output, DataPairAction, split_ntp_tree)

from pyTuplingUtils.io import read_branches
from pyTuplingUtils.utils import gen_histo
from pyTuplingUtils.plot import plot_histo, plot_errorbar
from pyTuplingUtils.plot import ax_add_args_histo, ax_add_args_errorbar


################################
# Command line argument parser #
################################

def parse_input(descr='plot branches from ntuples.'):
    parser = single_branch_parser_no_output(descr)

    parser.add_argument('-o', '--output',
                        required=True,
                        help='specify output file.')

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

    parser.add_argument('-XL', '--xlabel',
                        default=None,
                        help='specify x-axis label.')

    parser.add_argument('-YL', '--ylabel',
                        default='Number of candidates',
                        help='specify y-axis label.')

    parser.add_argument('--title',
                        default=None,
                        help='specify title.')

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

    parser.add_argument('--yscale',
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
    figure = None
    axis = None

    if not args.x_data_range:
        xmin = xmax = 0
    else:
        xmin, xmax = args.x_data_range
    if not args.y_data_range and args.yscale == 'linear':
        ymin = ymax = 0
    if not args.y_data_range and args.yscale == 'log':
        ymin = ymax = 1
    else:
        ymin, ymax = args.y_data_range

    if not args.colors:
        args.colors = [['cornflowerblue', 'black', 'darkgoldenrod', 'oliverab']]

    for ntp_tree, branches, colors, labels, in zip(
            args.ref, args.ref_branch, args.colors, args.labels):
        ntp, tree = split_ntp_tree(ntp_tree)
        loaded_branches = read_branches(uproot.open(ntp), tree, branches)

        if args.debug:
            print('Working on: {}, tree: {}'.format(ntp, tree))

        for br_name, br, clr, lbl in zip(
                branches, loaded_branches, colors, labels):
            if args.debug:
                print('  with branch: {}, color: {}, label: {}.'.format(
                    br_name, clr, lbl))

            histo, bins = gen_histo(br, args.bins, data_range=args.x_data_range)

            if not args.x_data_range:
                if bins[0] < xmin:
                    xmin = bins[0]
                if bins[-1] > xmax:
                    xmax = bins[-1]

            if not args.y_data_range:
                if ymax < histo.max():
                    ymax = 1.1*histo.max()

            if args.debug:
                print('xmin: {}, xmax: {}'.format(xmin, xmax))
                print('ymin: {}, ymax: {}'.format(ymin, ymax))

            if first_plot:
                first_plot = False
                histo_args = ax_add_args_histo(lbl, clr)
                figure, axis = plot_histo(
                    histo, bins, histo_args,
                    figure=figure, axis=axis,
                    xlabel=args.xlabel, ylabel=args.ylabel, title=args.title,
                    yscale=args.yscale,
                    xlim=(xmin, xmax), ylim=(ymin, ymax), show_legend=False)

            else:
                pts_args = ax_add_args_errorbar(
                    lbl, clr, marker='+', markeredgecolor=clr,
                    markeredgewidth=3)
                figure, axis = plot_errorbar(
                    bins, histo, pts_args,
                    figure=figure, axis=axis,
                    yscale=args.yscale,
                    xlim=(xmin, xmax), ylim=(ymin, ymax), show_legend=False)

    axis.legend()
    plt.tight_layout(pad=0.)
    figure.savefig(args.output)
    plt.close(figure)
