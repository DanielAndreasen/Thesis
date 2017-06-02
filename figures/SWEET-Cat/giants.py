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
    cols = ('name', 'vmag', 'teff', 'logg', 'feh', 'mass_sini',
            'orbital_period', 'detection_type')
    df = df.loc[:, cols]
    df = df[(df['mass_sini'] < 20) & (df['mass_sini'] > 1)]
    df = df[(df['detection_type'] == 'Radial Velocity') |
            (df['detection_type'] == 'Primary Transit')]
    return df


if __name__ == '__main__':
    df_all = get_data()
    df = df_all[df_all['vmag'] < 13]
    df = df[(df['teff']>4000) & (df['teff']<6500)]
    df = df[(df['orbital_period']>10) & (df['orbital_period']<5*365)]

    plt.xscale('log')
    plt.hist((df_all['mass_sini'].dropna()), bins=13)
    plt.hist((df['mass_sini'].dropna()), bins=13)
    plt.xlabel('Planet mass [Jupiter masses]')
    plt.show()
