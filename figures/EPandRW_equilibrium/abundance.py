from __future__ import division
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from utils import Readmoog
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'


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
    ax2 = fig.add_subplot(323, sharey=ax1)
    ax3 = fig.add_subplot(325, sharey=ax1)
    # Right side (RW)
    ax4 = fig.add_subplot(322, sharey=ax1)
    ax5 = fig.add_subplot(324, sharey=ax1)
    ax6 = fig.add_subplot(326, sharey=ax1)

    # Use the right axes depending on the row
    if row == 1:
        ax1 = ax1
        ax2 = ax4
        ax1.tick_params('x', labelcolor='w')
        ax2.tick_params('both', labelcolor='w')
        ax1.spines['top'].set_color('none')
        ax1.spines['right'].set_color('none')
        ax2.spines['top'].set_color('none')
        ax2.spines['right'].set_color('none')
    elif row == 2:
        ax1 = ax2
        ax2 = ax5
        ax1.tick_params('x', labelcolor='w')
        ax2.tick_params('both', labelcolor='w')
        ax1.spines['top'].set_color('none')
        ax1.spines['right'].set_color('none')
        ax2.spines['top'].set_color('none')
        ax2.spines['right'].set_color('none')
    elif row == 3:
        ax1 = ax3
        ax2 = ax6
        ax2.tick_params('y', labelcolor='w')
        ax1.spines['top'].set_color('none')
        ax1.spines['right'].set_color('none')
        ax2.spines['top'].set_color('none')
        ax2.spines['right'].set_color('none')
        ax.set_ylabel('Abundance\n ')
        ax1.set_xlabel(r'EP [eV]')
        ax2.set_xlabel(r'$\log(EW/\lambda)$')

    ax1.set_ylim(6.5, 9.0)
    ax2.set_ylim(6.5, 9.0)
    ax2.yaxis.set_label_position('right')
    ax2.set_ylabel(d[fname], rotation=270, va='bottom')
    ax2.set_title(d[fname])

    ax1.plot(x1, y ,'o', alpha=0.6, color='C0')
    ax1.plot(x1, y1, '--', color='C3', alpha=0.5)
    ax1.text(0.5, 8.25, r'$a_\mathrm{EP}$=%.3f' % a1)

    ax2.plot(x2, y ,'o', alpha=0.6, color='C2')
    ax2.plot(x2, y2, '--', color='C3', alpha=0.5)
    ax2.text(-6.2, 8.25, r'$a_\mathrm{RW}$=%.3f' % a2)

    if row == 3:
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
