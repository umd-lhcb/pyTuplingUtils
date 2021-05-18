#!/usr/bin/env python3
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Tue May 18, 2021 at 04:09 AM +0200

import numpy as np
import matplotlib as mp
import matplotlib.pyplot as plt

from functools import wraps
from inspect import getfullargspec


###################
# General helpers #
###################

def decorate_output(f, tight_layout=True, pad=0.):
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


def ax_add_args_histo(label, color='blue', edgecolor=None):
    if not edgecolor:
        edgecolor = color

    return {
        'color': color,
        'edgecolor': edgecolor,
        'label': label
    }


ax_add_args_simple = ax_add_args_histo  # For backward compatibility


def ax_add_args_errorbar(label, color, yerr=None, marker='o'):
    return {
        'label': label,
        'ls': 'none',
        'color': color,
        'marker': marker,
        'markeredgecolor': 'none',
        'yerr': yerr
    }


def ax_add_args_step(label, color, where='mid'):
    return {
        'label': label,
        'color': color,
        'where': where
    }


def ax_add_args_default(num, mean, std, *args, **kwargs):
    return ax_add_args_simple(
        'tot: {:.4g} mean {:.2g} std: {:.2g}'.format(
            num, mean, std
        ),
        *args, **kwargs)


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


def filter_kwargs_plot_prepare(kwargs):
    known_kwargs = getfullargspec(plot_prepare).args

    kw_plot_prepare = {k: kwargs[k] for k in known_kwargs if k in kwargs}
    kw_rest = {k: kwargs[k] for k in kwargs if k not in kw_plot_prepare}

    return kw_plot_prepare, kw_rest


def get_ytick_position_in_ax_coordinate(ax, scale):
    y_min, y_max = ax.get_ylim()
    raw_ticks = ax.get_yticks(minor=False)

    if scale == 'linear':
        ticks = [(tick - y_min)/(y_max - y_min) for tick in raw_ticks]
    elif scale == 'log':
        crd = np.vstack((np.zeros_like(raw_ticks), raw_ticks)).T
        ticks = ax.transAxes.inverted().transform(
            ax.transData.transform(crd))[:,1]
    else:
        raise ValueError('Unknown axis scale: {}'.format(scale))

    return y_min, y_max, ticks


def ensure_no_majortick_on_topmost(ax, scale, thresh=0.9, ratio=0.19,
                                   verbose=False):
    y_min, y_max, ticks = get_ytick_position_in_ax_coordinate(ax, scale)

    if verbose:
        print('y range is: {}, {}'.format(y_min, y_max))
        print('y major ticks are: {}'.format(','.join([str(i) for i in ticks])))

    max_majortick = ticks[-2] if ticks[-1] > 1 else ticks[-1]
    if verbose:
        print('Max y tick is at: {}'.format(max_majortick))

    if max_majortick >= thresh:
        rel_tick_gap = ticks[1] - ticks[0]
        abs_tick_gap = rel_tick_gap * (y_max-y_min)
        padding = ratio * abs_tick_gap

        ax.set_ylim((y_min, y_max+padding))
        if verbose:
            print('Added y pad. Now y max is: {}'.format(y_max+padding))


################
# Data helpers #
################

def convert_bins_to_central_pos(bins):
    return bins[:-1] + (np.diff(bins)/2)


################
# Simple plots #
################

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
def plot_histo(histo, bins, histo_add_args,
               output=None, xtick_formatter=tick_formatter_short,
               show_legend=True,
               xlim=None, ylim=None,
               **kwargs):
    fig, ax = plot_prepare(xtick_formatter=xtick_formatter, **kwargs)
    ax.bar(bins[:-1], histo, width=np.diff(bins), align='edge',
           **histo_add_args)

    if show_legend:
        ax.legend()

    if xlim:
        ax.set_xlim(xlim)

    if ylim:
        ax.set_ylim(ylim)

    return output, fig, ax


@decorate_output
def plot_errorbar(x, y, errorbar_add_args,
                  output=None,
                  convert_x=True,
                  show_legend=True, legend_loc='best',
                  xlim=None, ylim=None,
                  **kwargs):
    fig, ax = plot_prepare(**kwargs)

    if convert_x:
        x = convert_bins_to_central_pos(x)

    ax.errorbar(x, y, **errorbar_add_args)

    if show_legend:
        ax.legend(numpoints=1, loc=legend_loc)

    if xlim:
        ax.set_xlim(xlim)

    if ylim:
        ax.set_ylim(ylim)

    return output, fig, ax


@decorate_output
def plot_step(x, y, step_add_args,
              output=None,
              convert_x=True,
              show_legend=True, legend_loc='best',
              xlim=None, ylim=None,
              **kwargs):
    fig, ax = plot_prepare(**kwargs)

    if convert_x:
        x = convert_bins_to_central_pos(x)

    ax.step(x, y, **step_add_args)

    if show_legend:
        ax.legend(numpoints=1, loc=legend_loc)

    if xlim:
        ax.set_xlim(xlim)

    if ylim:
        ax.set_ylim(ylim)

    return output, fig, ax


##########################
# Common composite plots #
##########################

@decorate_output
def plot_two_histos(histo1, bins1, histo2, bins2,
                    histo1_add_args, histo2_add_args,
                    output=None,
                    **kwargs):
    kw_plot_prepare, kw_rest = filter_kwargs_plot_prepare(kwargs)
    fig, ax = plot_prepare(**kw_plot_prepare)

    _, ax1 = plot_histo(histo1, bins1, histo1_add_args, figure=fig, axis=ax,
                        show_legend=False, **kw_rest)
    _, ax2 = plot_histo(histo2, bins2, histo2_add_args, figure=fig, axis=ax1,
                        **kw_rest)

    return output, fig, ax1, ax2


@decorate_output
def plot_two_errorbar(x1, y1, x2, y2, errorbar1_add_args, errorbar2_add_args,
                      output=None,
                      **kwargs):
    kw_plot_prepare, kw_rest = filter_kwargs_plot_prepare(kwargs)
    fig, ax = plot_prepare(**kw_plot_prepare)

    _, ax1 = plot_errorbar(x1, y1, errorbar1_add_args, figure=fig, axis=ax,
                           show_legend=False, **kw_rest)
    _, ax2 = plot_errorbar(x2, y2, errorbar2_add_args, figure=fig, axis=ax1,
                           **kw_rest)

    return output, fig, ax1, ax2


##############
# Grid plots #
##############

def plot_top_histo_bot_errorbar(histo1, bins1, histo2, bins2, x_ratio, y_ratio,
                                histo1_add_args, histo2_add_args,
                                output,
                                ratio_add_args=ax_add_args_errorbar(
                                    'Ratio', 'black'),
                                title=None,
                                xlabel=None,
                                ax1_ylabel=None, ax2_ylabel=None,
                                ax1_yscale='linear', ax2_yscale='linear',
                                height_ratios=[3, 1],
                                **kwargs):
    fig = plt.figure()
    fig.set_tight_layout({'pad': 0.})

    spec = fig.add_gridspec(ncols=1, nrows=2, height_ratios=height_ratios)
    spec.update(hspace=0.)

    ax1 = fig.add_subplot(spec[0, 0])
    ax1.set_yscale(ax1_yscale)
    plot_two_histos(histo1, bins1, histo2, bins2,
                    histo1_add_args, histo2_add_args,
                    figure=fig, axis=ax1,
                    ylabel=ax1_ylabel, title=title,
                    **kwargs)

    ax2 = fig.add_subplot(spec[1, 0], sharex=ax1)
    ax2.set_yscale(ax2_yscale)
    plot_errorbar(x_ratio, y_ratio, ratio_add_args,
                  figure=fig, axis=ax2,
                  xlabel=xlabel, ylabel=ax2_ylabel, show_legend=False)

    # Remove the horizontal labels for the top plot
    for tick in ax1.xaxis.get_major_ticks():
        tick.label1.set_visible(False)

    # No offset (like +1 on top of the axis)
    if ax2_yscale == 'linear':
        ax2.ticklabel_format(axis='y', useOffset=False)

    # Add some padding if the TOPMOST ylabel of bot is too close to the top
    ensure_no_majortick_on_topmost(ax2, ax2_yscale)

    # Align y labels
    fig.align_ylabels()

    fig.savefig(output)


def plot_top_errorbar_bot_errorbar(x1, y1, x2, y2, x_ratio, y_ratio,
                                   errorbar1_add_args, errorbar2_add_args,
                                   output,
                                   ratio_add_args=ax_add_args_errorbar(
                                       'Ratio', 'black'),
                                   title=None,
                                   xlabel=None,
                                   ax1_ylabel=None, ax2_ylabel=None,
                                   ax1_yscale='linear', ax2_yscale='linear',
                                   hline_pos=None,
                                   height_ratios=[3, 1],
                                   **kwargs):
    fig = plt.figure()
    fig.set_tight_layout({'pad': 0.})  # Remove surrounding padding

    spec = fig.add_gridspec(ncols=1, nrows=2, height_ratios=height_ratios)
    spec.update(hspace=0.)  # Remove gaps between subplots

    ax1 = fig.add_subplot(spec[0, 0])
    ax1.set_yscale(ax1_yscale)
    plot_two_errorbar(x1, y1, x2, y2, errorbar1_add_args, errorbar2_add_args,
                      figure=fig, axis=ax1,
                      ylabel=ax1_ylabel, title=title, **kwargs)

    ax2 = fig.add_subplot(spec[1, 0], sharex=ax1)
    ax2.set_yscale(ax2_yscale)
    plot_errorbar(x_ratio, y_ratio, ratio_add_args,
                  figure=fig, axis=ax2,
                  xlabel=xlabel, ylabel=ax2_ylabel, show_legend=False)

    # Add a horizontal line
    if not hline_pos:
        hline_pos = y_ratio[y_ratio != 0].mean()
    ax2.axhline(hline_pos, color='gray')

    # Remove the horizontal labels for the top plot
    for tick in ax1.xaxis.get_major_ticks():
        tick.label1.set_visible(False)

    # No offset (like +1 on top of the axis)
    if ax2_yscale == 'linear':
        ax2.ticklabel_format(axis='y', useOffset=False)

    # Add some padding if the TOPMOST ylabel of bot is too close to the top
    ensure_no_majortick_on_topmost(ax2, ax2_yscale)

    # Align y labels
    fig.align_ylabels()

    fig.savefig(output)
