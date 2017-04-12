from __future__ import division
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from utils import Readmoog


def get_data(fname):
    m = Readmoog(fname=fname)
    df = m.all_table()
    return df


def get_slope(x, y):
    return np.polyfit(x, y, deg=1)


def plot_data(fname, row, fig=None):
    df = get_data(fname)
    a1, b1 = get_slope(df.EP, df.abund)
    a2, b2 = get_slope(df.logRWin, df.abund)

    y = df.abund
    x1, y1 = df.EP, np.poly1d((a1, b1))(df.EP)
    x2, y2 = df.logRWin, np.poly1d((a2, b2))(df.logRWin)

    if fig is None:
        fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111)
    ax.spines['top'].set_color('none')
    ax.spines['bottom'].set_color('none')
    ax.spines['left'].set_color('none')
    ax.spines['right'].set_color('none')
    ax.tick_params(labelcolor='w', top='off', bottom='off', left='off', right='off')

    # Left side (EP)
    ax1 = fig.add_subplot(321)
    ax2 = fig.add_subplot(323, sharex=ax1)
    ax3 = fig.add_subplot(325, sharex=ax1)
    # Right side (RW)
    ax4 = fig.add_subplot(322, sharey=ax1)
    ax5 = fig.add_subplot(324, sharex=ax4, sharey=ax2)
    ax6 = fig.add_subplot(326, sharex=ax4, sharey=ax3)

    # Use the right axes depending on the row
    if row == 1:
        ax1 = ax1
        ax2 = ax4
    elif row == 2:
        ax1 = ax2
        ax2 = ax5
    elif row == 3:
        ax1 = ax3
        ax2 = ax6
        ax.set_ylabel('Abundance')
        ax1.set_xlabel(r'EP [eV]')
        ax2.set_xlabel(r'$\log(EW/\lambda)$')

    ax2.yaxis.set_label_position('right')
    ax2.set_ylabel(d[fname], rotation=270, va='bottom')

    im = ax1.scatter(x1, y, c=np.abs(df.delavg))
    ax1.plot(x1, y1, '--', color='C3', alpha=0.5)

    ax2.scatter(x2, y, c=np.abs(df.delavg))
    ax2.plot(x2, y2, '--', color='C3', alpha=0.5)

    cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
    fig.subplots_adjust(right=0.8)
    cbar = fig.colorbar(im, cax=cbar_ax)
    cbar.set_label('Abundance deviation', rotation=270, va='bottom')
    fig.tight_layout(rect=[0, 0, 0.85, 1])

    return fig




if __name__ == '__main__':
    d = {'converged_05kms.dat': '+0.5km/s',
         'converged_500K.dat': '+500K',
         'converged.dat': 'Converged'}
    fig = None
    for i, fname in enumerate(d.keys()):
        fig = plot_data(fname, row=i+1, fig=fig)

    # plt.savefig('../EP_RW_vs_abundance.pdf')
    plt.show()
