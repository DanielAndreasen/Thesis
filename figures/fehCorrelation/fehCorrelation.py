from __future__ import division
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
plt.rcParams['axes.spines.right'] = False
plt.rcParams['axes.spines.top'] = False
plt.rcParams['axes.linewidth'] = 2
plt.rcParams['xtick.major.width'] = 2
plt.rcParams['ytick.major.width'] = 2


def read_data(fname):
    names = ['star', 'teff', 'tefferr', 'logg', 'loggerr', 'vt', 'vterr',
             'feh', 'feherr', 'n1', 'n2', 'mass', 'logghip',
             'lum', 'lumerr', 'vmag', 'host']
    df = pd.read_table(fname, names=names, delimiter=r'\s+')
    df['host'] = df['host'] == 'yes'
    return df


if __name__ == '__main__':
    # Data from Sousa+ 2008
    # http://cdsarc.u-strasbg.fr/viz-bin/qcat?J/A+A/487/373
    df = read_data('table2.dat')

    plt.hist(df.loc[df.host, 'feh'], histtype='step', lw=2, label='Planet host', normed=True)
    plt.hist(df.loc[~df.host, 'feh'], histtype='step', lw=2, label='No planet host', normed=True)
    plt.legend(loc=2, frameon=False)
    plt.xlabel('[Fe/H]')
    plt.tight_layout()

    # plt.savefig('../fehCorrelation.pdf')
    plt.show()
