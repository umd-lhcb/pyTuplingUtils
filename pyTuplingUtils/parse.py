#!/usr/bin/env python3
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Mon Jun 07, 2021 at 03:19 AM +0200

from argparse import ArgumentParser


def single_ntuple_parser_no_output(descr, parser=None):
    parser = ArgumentParser(description=descr) if parser is None else parser

    parser.add_argument('-n', '--ref',
                        required=True,
                        help='''
path to reference ntuple.''')

    parser.add_argument('-t', '--ref-tree',
                        required=True,
                        help='''
tree name for the reference ntuple.''')

    parser.add_argument('--bins',
                        type=int,
                        default=25,
                        help='''
specify binning.''')

    return parser


def single_ntuple_parser(descr, parser=None):
    parser = single_ntuple_parser_no_output(descr) if parser is None else parser

    parser.add_argument('-o', '--output',
                        required=True,
                        help='''
path to output file.''')

    parser.add_argument('-b', '--ref-branch',
                        required=True,
                        help='''
branch name(s) in reference ntuple. may be separated by ",".''')

    parser.add_argument('-l', '--ref-label',
                        required=True,
                        help='''
specify label for reference branch.''')

    parser.add_argument('--xlabel',
                        default=None,
                        help='''
specify xlabel.''')

    parser.add_argument('--ylabel',
                        default='Number of candidates',
                        help='''
specify ylabel.''')

    return parser


def double_ntuple_parser_no_output(descr, parser=None):
    parser = single_ntuple_parser_no_output(descr) if parser is None else parser

    parser.add_argument('-N', '--comp',
                        required=True,
                        help='''
path to comparison ntuple.''')

    parser.add_argument('-T', '--comp-tree',
                        required=True,
                        help='''
tree name for the comparison ntuple.''')

    return parser


def double_ntuple_parser(descr, parser=None):
    if parser is None:
        parser = double_ntuple_parser_no_output(descr)
        parser = single_ntuple_parser(descr, parser)

    parser.add_argument('-B', '--comp-branch',
                        required=True,
                        help='''
branch name(s) in comparison ntuple. may be separated by ",".''')

    parser.add_argument('-L', '--comp-label',
                        required=True,
                        help='''
specify label for comparison branch.''')

    return parser
