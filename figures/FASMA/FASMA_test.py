# -*- coding: utf8 -*-
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
    df1 = pd.read_csv('FASMAtest.csv', delimiter='\t')
    df1['linelist'] = df1['linelist'].str.replace(' ', '')

    df2 = pd.read_csv('Sergio.csv', delimiter=r'\s+')
    df = pd.merge(df1, df2, left_on='linelist', right_on='star')
    df = df[df.convergence]

    plt.subplot(221)
    plt.errorbar(df.teff, df.teffs, xerr=df.tefferr_x, yerr=df.tefferr_y, fmt='.', alpha=0.3)
    plt.plot([4500, 7300], [4500, 7300], '--k')
    plt.xlim(4300, 7500)
    plt.title(r'$T_\mathrm{eff}$ [K]')
    plt.subplot(222)
    plt.errorbar(df.logg, df.loggs, xerr=df.loggerr_x, yerr=df.loggerr_y, fmt='.', alpha=0.3)
    plt.plot([3.56, 5], [3.56, 5], '--k')
    plt.xlim(plt.ylim())
    plt.title(r'$\log g$ [dex]')
    plt.subplot(223)
    plt.errorbar(df.feh, df.fehs, xerr=df.feherr_x, yerr=df.feherr_y, fmt='.', alpha=0.3)
    plt.plot([-1.15, 0.63], [-1.15, 0.63], '--k')
    plt.title('[Fe/H] [dex]')
    plt.subplot(224)
    plt.errorbar(df.vt, df.vts, xerr=df.vterr_x, yerr=df.vterr_y, fmt='.', alpha=0.3)
    plt.plot([0, 2.8], [0, 2.8], '--k')
    plt.xlim(-0.14, 2.94)
    plt.ylim(-0.14, 3.01)
    plt.title(r'$\xi_\mathrm{micro}$ [km/s]')

    plt.tight_layout()
    # plt.savefig('../FASMAtest.pdf')
    plt.show()
