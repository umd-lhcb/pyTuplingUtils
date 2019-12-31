#!/usr/bin/env python3
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Tue Dec 31, 2019 at 02:44 AM -0500

import numpy as np
import matplotlib as mp
import matplotlib.pyplot as plt

from functools import wraps


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

def plot_style(text_usetex=False,
               font_family='monospace', font_weight='normal', font_size=12,
               style='classic'):
    plt.style.use(style)
    plt.rcParams.update({'text.usetex': text_usetex})
    plt.rcParams.update({'font.family': font_family})
    plt.rcParams.update({'font.weight': font_weight})
    plt.rcParams.update({'font.size': int(font_size)})


def tick_formatter_short(x, p):
    X = str(x)
    if len(X) > 4:
        return '{:2g}'.format(x)
    else:
        return x


def ax_add_args_simple(label, color='blue', edgecolor=None):
    if not edgecolor:
        edgecolor = color

    return {
        'color': color,
        'edgecolor': edgecolor,
        'label': label
    }


def ax_add_args_default(num, mean, std, *args, **kwargs):
    return ax_add_args_simple(
        'tot: {:.4g} mean {:.2g} std: {:.2g}'.format(
            num, mean, std
        ),
        *args, **kwargs)


################
# Simple plots #
################

def plot_prepare(figure=None, axis=None, title=None,
                 xtick_formatter=None, ytick_formatter=None,
                 xlabel=None, ylabel=None,
                 xscale='linear', yscale='linear'):
    fig = plt.figure() if not figure else figure

    if not axis:
        ax = fig.add_subplot()
        ax.set_xscale(xscale)
        ax.set_yscale(yscale)
    else:
        ax = axis

    if title:
        ax.set_title(title)

    if xtick_formatter:
        ax.get_xaxis().set_major_formatter(
            mp.ticker.FuncFormatter(xtick_formatter)
        )
    if ytick_formatter:
        ax.get_yaxis().set_major_formatter(
            mp.ticker.FuncFormatter(ytick_formatter)
        )

    if xlabel:
        ax.set_xlabel(xlabel)
    if ylabel:
        ax.set_ylabel(ylabel)

    return fig, ax


@decorate_output
def plot_pts(pts, bins, pts_add_args,
             marker='_', output=None, **kwargs):
    fig, ax = plot_prepare(**kwargs)
    ax.scatter(bins[:-1]+(np.diff(bins)/2), pts, marker=marker,
               **pts_add_args)

    return output, fig, ax


@decorate_output
def plot_histo(histo, bins, histo_add_args,
               output=None, xtick_formatter=tick_formatter_short,
               show_legend=True,
               **kwargs):
    fig, ax = plot_prepare(xtick_formatter=xtick_formatter, **kwargs)
    ax.bar(bins[:-1], histo, width=np.diff(bins), align='edge',
           **histo_add_args)

    if show_legend:
        ax.legend()

    return output, fig, ax


@decorate_output
def plot_hexbin(x, y, gridsize, hexbin_add_args,
                output=None, cmap='inferno', bins='log', colorbar_label=None,
                **kwargs):
    fig, ax = plot_prepare(**kwargs)
    hb = ax.hexbin(x, y,
                   gridsize=gridsize, cmap=cmap, bins=bins, **hexbin_add_args)
    cb = fig.colorbar(hb, ax=ax)

    if colorbar_label:
        cb.set_label(colorbar_label)

    return output, fig, ax


@decorate_output
def plot_two_histos(histo1, bins1, histo2, bins2,
                    histo1_add_args, histo2_add_args,
                    output=None, figure=None, **kwargs):
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
                           ax1_yscale='linear', ax2_yscale='linear',
                           xtick_formatter=None,
                           top_ytick_formatter=None, bot_ytick_formatter=None,
                           height_ratios=[5, 1]):
    fig = plt.figure(constrained_layout=True)
    spec = fig.add_gridspec(ncols=1, nrows=2, height_ratios=height_ratios)

    ax1 = fig.add_subplot(spec[0, 0])
    plot_histo(histo1, bins1, histo1_add_args,
               figure=fig, axis=ax1,
               show_legend=False,
               xtick_formatter=xtick_formatter,
               ytick_formatter=top_ytick_formatter)
    plot_histo(histo2, bins2, histo2_add_args,
               figure=fig, axis=ax1,
               show_legend=False,
               xtick_formatter=xtick_formatter,
               ytick_formatter=top_ytick_formatter,
               xlabel=ax1_xlabel, ylabel=ax1_ylabel, yscale=ax1_yscale)
    ax1.legend()

    ax2 = fig.add_subplot(spec[1, 0], sharex=ax1)
    plot_pts(pts, width, pts_add_args,
             figure=fig, axis=ax2,
             xtick_formatter=xtick_formatter,
             ytick_formatter=bot_ytick_formatter,
             xlabel=ax2_xlabel, ylabel=ax2_ylabel, yscale=ax2_ylabel)

    fig.savefig(output)
