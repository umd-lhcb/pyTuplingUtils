#!/usr/bin/env python3
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Mon Jun 08, 2020 at 11:10 PM +0800

from argparse import ArgumentParser


def single_ntuple_parser_no_output(descr, parser=None):
    parser = ArgumentParser(description=descr) if parser is None else parser

    parser.add_argument('-n', '--ref',
                        nargs='?',
                        required=True,
                        help='''
path to reference ntuple.''')

    parser.add_argument('-t', '--ref-tree',
                        nargs='?',
                        required=True,
                        help='''
tree name for the reference ntuple.''')

    return parser


def single_ntuple_parser(descr, parser=None):
    parser = single_ntuple_parser_no_output(descr) if parser is None else parser

    parser.add_argument('-o', '--output',
                        nargs='?',
                        required=True,
                        help='''
path to output file.''')

    parser.add_argument('-b', '--ref-branch',
                        nargs='?',
                        required=True,
                        help='''
branch name(s) in reference ntuple. may be separated by ",".''')

    return parser


def double_ntuple_parser_no_output(descr, parser=None):
    parser = single_ntuple_parser_no_output(descr) if parser is None else parser

    parser.add_argument('-N', '--comp',
                        nargs='?',
                        required=True,
                        help='''
path to comparison ntuple.''')

    parser.add_argument('-T', '--comp-tree',
                        nargs='?',
                        required=True,
                        help='''
tree name for the comparison ntuple.''')

    return parser


def double_ntuple_parser(descr, parser=None):
    if parser is None:
        parser = double_ntuple_parser_no_output(descr)
        parser = single_ntuple_parser(descr, parser)

    parser.add_argument('-B', '--comp-branch',
                        nargs='?',
                        required=True,
                        help='''
branch name(s) in comparison ntuple. may be separated by ",".''')

    return parser
