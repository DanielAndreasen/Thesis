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

    plt.subplot(221)
    plt.plot(df.teff, df.teffs, 'o')
    plt.plot([4500, 7300], [4500, 7300], '--k')
    plt.title(r'$T_\mathrm{eff}$ [K]')
    plt.subplot(222)
    plt.plot(df.logg, df.loggs, 'o')
    plt.plot([3.56, 5], [3.56, 5], '--k')
    plt.title(r'$\log g$ [dex]')
    plt.subplot(223)
    plt.plot(df.feh, df.fehs, 'o')
    plt.plot([-1.15, 0.63], [-1.15, 0.63], '--k')
    plt.title('[Fe/H] [dex]')
    plt.subplot(224)
    plt.plot(df.vt, df.vts, 'o')
    plt.plot([0, 2.8], [0, 2.8], '--k')
    plt.title(r'$\xi_\mathrm{micro}$ [km/s]')

    plt.tight_layout()
    # plt.savefig('../FASMAtest.pdf')
    plt.show()
