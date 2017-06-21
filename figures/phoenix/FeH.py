from __future__ import division
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from simulation import extract_parameters

plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
plt.rcParams['axes.spines.right'] = False
plt.rcParams['axes.spines.top'] = False
plt.rcParams['axes.linewidth'] = 2
plt.rcParams['xtick.major.width'] = 2
plt.rcParams['ytick.major.width'] = 2


if __name__ == '__main__':
    fnames = ('simulation_fix.dat', 'simulation_free.dat')
    fig = plt.figure()
    ax0 = fig.add_subplot(111)
    ax1 = fig.add_subplot(211)
    ax2 = fig.add_subplot(212)
    axes = (ax1, ax2)
    for i, (ax, fname) in enumerate(zip(axes, fnames)):
        i += 1
        title = fname.split('_')[-1].strip('.dat')
        title = 'Parameters: {}'.format(title)
        df = pd.read_table(fname, delimiter=r'\s+')
        df = extract_parameters(df)
        dfm = df[df['model'] == 'marcs']
        dfk = df[df['model'] == 'kurucz95']
        dfk = dfk[dfk['convergence']]
        dfm = dfm[dfm['convergence']]

        ax.errorbar(dfk['teff_true'], dfk['feh'], yerr=dfk['feherr'], fmt='o', label='Kurucz')
        ax.errorbar(dfm['teff_true'], dfm['feh'], yerr=dfm['feherr'], fmt='o', label='MARCS')
        ax.set_title(title)

        ax.legend(loc='best', frameon=False)
        ax.grid()


    # Styling
    xticks = range(3500, 6001, 500)
    ax0.spines['top'].set_color('none')
    ax0.spines['bottom'].set_color('none')
    ax0.spines['left'].set_color('none')
    ax0.spines['right'].set_color('none')
    ax0.tick_params(labelcolor='w', top='off', bottom='off', left='off', right='off')
    ax1.set_xticks(xticks)
    ax1.set_xticklabels(['']*len(xticks))
    ax2.set_xticks(xticks)
    ax2.set_xticklabels(xticks)
    ax2.set_xlabel(r'T$_\mathrm{eff}$ [K]')
    ax0.set_ylabel('[Fe/H] [dex]\n')

    # plt.savefig('../FeH_simulated.pdf')
    plt.show()
