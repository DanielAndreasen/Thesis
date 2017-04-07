from __future__ import division
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from glob import glob
from utils import Readmoog


def get_data(fname):
    m = Readmoog(fname=fname)
    df = m.all_table()
    return df


def get_slope(x, y):
    return np.polyfit(x, y, deg=1)


def plot_data(fname):
    df = get_data(fname)
    a1, b1 = get_slope(df.EP, df.abund)
    a2, b2 = get_slope(df.logRWin, df.abund)

    y = df.abund
    x1, y1 = df.EP, np.poly1d((a1, b1))(df.EP)
    x2, y2 = df.logRWin, np.poly1d((a2, b2))(df.logRWin)

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax1 = fig.add_subplot(211)
    ax2 = fig.add_subplot(212, sharey=ax1)
    ax.spines['top'].set_color('none')
    ax.spines['bottom'].set_color('none')
    ax.spines['left'].set_color('none')
    ax.spines['right'].set_color('none')
    ax.tick_params(labelcolor='w', top='off', bottom='off', left='off', right='off')

    ax.set_title(d[fname])
    ax.set_ylabel('Abundance')
    ax1.set_xlabel(r'EP')
    ax2.set_xlabel(r'$\log(EW/\lambda)$')


    im = ax1.scatter(x1, y, c=np.abs(df.delavg))
    ax1.plot(x1, y1, '--', color='C3', alpha=0.5)

    ax2.scatter(x2, y, c=np.abs(df.delavg))
    ax2.plot(x2, y2, '--', color='C3', alpha=0.5)

    cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
    fig.subplots_adjust(right=0.8)
    cbar = fig.colorbar(im, cax=cbar_ax)
    cbar.set_label('Abundance deviation', rotation=270, va='bottom')
    fig.tight_layout(rect=[0, 0, 0.85, 1])

    plt.savefig('../%s' % fname.replace('.dat', '.pdf'))



if __name__ == '__main__':
    files = glob('*.dat')
    d = {'converged_05kms.dat': '+0.5km/s',
         'converged_500K.dat': '+500K',
         'converged.dat': 'Converged'}
    for file in files:
        df = plot_data(file)
