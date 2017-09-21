from __future__ import division
import numpy as np
import pandas as pd
from PyAstronomy import pyasl
import matplotlib.pyplot as plt

plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
plt.rcParams['axes.spines.right'] = False
plt.rcParams['axes.spines.top'] = False
plt.rcParams['axes.linewidth'] = 2
plt.rcParams['xtick.major.width'] = 2
plt.rcParams['ytick.major.width'] = 2


def get_data():
    def get_stars():
        d = pyasl.SWEETCat()
        return d.data
    def get_planets():
        v = pyasl.ExoplanetEU2()
        return v.getAllDataPandas()

    df1 = get_stars()
    df2 = get_planets()

    df = pd.merge(df1, df2, left_on='star', right_on='star_name', how='right')
    cols = ('name', 'vmag', 'teff', 'logg', 'metal', 'mass_x', 'mass_sini',
            'orbital_period', 'detection_type')
    df = df.loc[:, cols]
    df['mass'] = df['mass_x']
    df = df[(1 < df['mass_sini']) & (df['mass_sini'] < 15)]
    df = df[(df['detection_type'] == 'Radial Velocity') |
            (df['detection_type'] == 'Primary Transit')]
    return df


if __name__ == '__main__':
    df_all = get_data()
    df = df_all[df_all['vmag'] < 13]
    df = df[(df['teff']>4000) & (df['teff']<6500)]
    df = df[(df['orbital_period']>10) & (df['orbital_period']<5*365)]

    fig, (axes) = plt.subplots(2, 2, sharex=True)
    axes = axes.flatten()
    Mranges = ([0, 999], [1.5, 999], [1, 1.5], [0, 1])
    for ax, Mrange in zip(axes, Mranges):
        idx = (Mrange[0] <= df['mass']) & (df['mass'] <= Mrange[1])
        d = df[idx]
        idx = d['mass_sini'] < 4
        ax.hist(d.loc[idx,  'metal'].dropna(), normed=True, histtype='step', lw=2)
        ax.hist(d.loc[~idx, 'metal'].dropna(), normed=True, histtype='step', lw=2)

    axes[0].set_title('All stars')
    axes[1].set_title(r'$M_\ast \geq 1.5M_\odot$')
    axes[2].set_title(r'$1.0M_\odot \leq M_\ast \leq 1.5M_\odot$')
    axes[3].set_title(r'$M_\ast \leq 1.0M_\odot$')

    axes[2].legend(
        (r'$1M_\mathrm{Jup} < M_\mathrm{pl} \leq 4M_\mathrm{Jup}$',
         r'$4M_\mathrm{Jup} < M_\mathrm{pl} < 15M_\mathrm{Jup}$' ),
         frameon=False, loc='upper left')
    axes[2].set_xlabel('[Fe/H]')
    axes[3].set_xlabel('[Fe/H]')


    plt.tight_layout()
    plt.savefig('../fehGiants.pdf')
    plt.show()
