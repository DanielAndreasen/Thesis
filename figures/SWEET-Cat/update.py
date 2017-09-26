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


if __name__ == '__main__':
    df1 = pd.read_csv('SCnewtable.csv')
    df2 = pd.read_csv('SColdtable.csv')
    df = pd.merge(df1, df2, left_on='star', right_on='star')

    keys = ('teff', 'logg', 'feh', 'vt')
    parameters = {'teff': r'T$_\mathrm{eff}$',
                  'logg': r'$\log g$',
                  'feh': '[Fe/H]',
                  'vt': r'$\xi_\mathrm{micro}$'}
    fig, (axes) = plt.subplots(2, 2)
    for parameter, ax in zip(keys, axes.flatten()):
        ax.plot(df['{}_x'.format(parameter)], df['{}_y'.format(parameter)], '.')
        ax.set_title(parameters[parameter])
        x1, x2 = ax.get_xlim()
        ax.plot([x1, x2], [x1, x2], '--k', alpha=0.7)

    plt.tight_layout()
    plt.savefig('../SCupdate.pdf')
    plt.show()
