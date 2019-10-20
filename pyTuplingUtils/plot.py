#!/usr/bin/env python3
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Sun Oct 20, 2019 at 03:43 AM -0400

import numpy as np
import matplotlib as mp

from functools import wraps
from matplotlib import pyplot as plt


###################
# General helpers #
###################

def decorate_output(f, tight_layout=True, pad=0.1):
    @wraps(f)
    def wrapper(*args, **kwargs):
        result = f(*args, **kwargs)
        output = result[0]
        data = result[1:]

        if not output:
            return data
        else:
            fig = data[0]
            if tight_layout:
                plt.tight_layout(pad=pad)
            fig.savefig(output)
            fig.clf()
            plt.close(fig)

    return wrapper


################
# Plot helpers #
################

def plot_style(text_usetex=True,
               font_family='serif', font_weight='normal', font_size=12,
               style='classic'):
    plt.rcParams.update({'text.usetex': text_usetex})
    plt.rcParams.update({'font.family': font_family})
    plt.rcParams.update({'font.weight': font_weight})
    plt.rcParams.update({'font.size': int(font_size)})
    plt.style.use(style)


def tick_formatter_simple(x, p):
    return x


def tick_formatter_short(x, p):
    X = str(x)
    if len(X) > 4:
        return '{:2g}'.format(x)
    else:
        return x


def ax_add_args_default(num, mean, std, color='blue', edgecolor=None):
    if not edgecolor:
        edgecolor = color

    return {
        'color': color,
        'edgecolor': edgecolor,
        'label': 'tot: {:.4g} mean {:.2g} std: {:.2g}'.format(
            num, mean, std
        )
    }


def ax_add_args_simple(label, color='blue', edgecolor=None):
    if not edgecolor:
        edgecolor = color

    return {
        'color': color,
        'edgecolor': edgecolor,
        'label': label
    }


################
# Simple plots #
################

@decorate_output
def plot_pts(pts, width, pts_add_args,
             marker='_',
             output=None,
             figure=None, axis=None,
             title=None,
             xtick_formatter=tick_formatter_simple,
             yscale='linear',
             ):
    fig = plt.figure() if not figure else figure

    if not axis:
        ax = fig.add_subplot()
        ax.set_yscale(yscale)
    else:
        ax = axis

    ax.scatter(width[:-1]+(np.diff(width)/2), pts, marker=marker,
               **pts_add_args)

    if not title:
        ax.set_title(title)

    ax.get_xaxis().set_major_formatter(
        mp.ticker.FuncFormatter(xtick_formatter)
    )

    return output, fig, ax


@decorate_output
def plot_histo(histo, bins, histo_add_args,
               output=None,
               figure=None, axis=None,
               title=None,
               xtick_formatter=tick_formatter_short,
               yscale='linear',
               ):
    fig = plt.figure() if not figure else figure

    if not axis:
        ax = fig.add_subplot()
        ax.set_yscale(yscale)
    else:
        ax = axis

    ax.bar(bins[:-1], histo, width=np.diff(bins), align='edge',
           **histo_add_args)

    if not title:
        ax.set_title(title)

    ax.get_xaxis().set_major_formatter(
        mp.ticker.FuncFormatter(xtick_formatter)
    )

    return output, fig, ax


@decorate_output
def plot_two_histos(histo1, bins1, histo2, bins2,
                    histo1_add_args, histo2_add_args,
                    output=None,
                    figure=None,
                    **kwargs):
    fig = plt.figure() if not figure else figure

    _, ax1 = plot_histo(histo1, bins1, output, histo1_add_args,
                        figure=fig,
                        **kwargs)
    _, ax2 = plot_histo(histo2, bins2, output, histo2_add_args,
                        figure=fig, axis=ax1,
                        **kwargs)

    return output, fig, ax1, ax2


##############
# Grid plots #
##############

def plot_top_histo_bot_pts(histo1, bins1, histo2, bins2, pts, width,
                           histo1_add_args, histo2_add_args, pts_add_args,
                           ax1_xlabel, ax1_ylabel,
                           ax2_xlabel, ax2_ylabel,
                           output,
                           ax1_yscale='linear',
                           ax2_yscale='linear',
                           xtick_formatter=tick_formatter_simple,
                           height_ratios=[5, 1]):
    fig = plt.figure(constrained_layout=True)
    spec = fig.add_gridspec(ncols=1, nrows=2, height_ratios=height_ratios)

    ax1 = fig.add_subplot(spec[0, 0])
    ax1.set_yscale(ax1_yscale)
    ax1.set_xlabel(ax1_xlabel)
    ax1.set_ylabel(ax1_ylabel)

    plot_histo(histo1, bins1, histo1_add_args, figure=fig, axis=ax1,
               xtick_formatter=xtick_formatter)
    plot_histo(histo2, bins2, histo2_add_args, figure=fig, axis=ax1,
               xtick_formatter=xtick_formatter)

    ax1.legend()

    ax2 = fig.add_subplot(spec[1, 0], sharex=ax1)
    ax2.set_yscale(ax2_yscale)
    ax2.set_xlabel(ax2_xlabel)
    ax2.set_ylabel(ax2_ylabel)

    plot_pts(pts, width, pts_add_args, xtick_formatter=xtick_formatter)

    fig.savefig(output)
