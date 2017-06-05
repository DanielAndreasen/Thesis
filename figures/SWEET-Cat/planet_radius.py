from __future__ import division
import numpy as np
import pandas as pd
from PyAstronomy import pyasl
import astropy.constants as c
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
    df['radius'] = df['radius'] * (c.R_jup.value/c.R_earth.value)  # Earth radii
    df = df[df['radius'] <= 3.5]
    return df


if __name__ == '__main__':
    df = get_data()
    i1 = df['radius'] <= 2.0
    i2 = df['metal'] >= 0.0

    bins = np.logspace(-1.0, 0.55, 13)


    plt.figure()
    plt.hist(df['radius'].dropna(), bins=bins)
    plt.vlines(2, 0, 300)
    plt.xlabel('Planet radius [Earth radii]')
    plt.xscale('log')

    plt.figure()
    plt.plot(df[i1]['metal'], df[i1]['radius'], '.', alpha=0.5)
    plt.plot(df[~i1]['metal'], df[~i1]['radius'], '.', alpha=0.5)
    plt.xlabel('[Fe/H]')
    plt.ylabel('Planet radius [Earth radii]')

    plt.figure()
    plt.subplot(211)
    plt.hist(df[i2]['radius'].dropna(), bins=bins)
    plt.ylabel('Metal-rich')
    plt.xscale('log')
    plt.subplot(212)
    plt.hist(df[~i2]['radius'].dropna(), bins=bins)
    plt.ylabel('Metal-poor')
    plt.xscale('log')

    plt.show()
