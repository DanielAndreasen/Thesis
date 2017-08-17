from __future__ import division
import numpy as np
import pandas as pd
import matplotlib.cm as cm
from PyAstronomy import pyasl
import matplotlib.pyplot as plt
from astropy import constants as c

plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
plt.rcParams['axes.spines.right'] = False
plt.rcParams['axes.spines.top'] = False
plt.rcParams['axes.linewidth'] = 2
plt.rcParams['xtick.major.width'] = 2
plt.rcParams['ytick.major.width'] = 2

def absolute_magnitude(parallax, m):
    d = 1 / parallax
    mu = 5 * np.log10(d) - 5
    M = m - mu
    return M


def radius(logg, m):
    G = c.G.value
    M = c.M_sun.value
    R = c.R_sun.value
    r = np.sqrt((G*m*M) / (10**logg)) * 1/R
    return r

def readSC():
    df = pd.read_table('sweet-cat.tsv')
    df.drop('tmp', axis=1, inplace=True)
    df['Vabs'] = absolute_magnitude(df.par, df.Vmag)
    df['R'] = radius(df.logg, df.mass)
    return df


if __name__ == '__main__':
    df = readSC()
    df = df[df.teff < 8000]

    # Page 506-507 in Gray
    spts = {'F0': 7178, 'F5': 6528, 'G0': 5943, 'K0': 5282, 'K5': 4623, 'M2': 4076}

    plt.scatter(df.teff, df.Vabs, c=df.teff, s=df.R*10, cmap=cm.inferno)
    for spt, teff in spts.iteritems():
        plt.vlines(teff, 11, 29, linestyle='--', alpha=0.6)
    plt.xticks(spts.values(), spts.keys())
    plt.xlim(plt.xlim()[::-1])
    plt.ylim(plt.ylim()[::-1])
    plt.xlabel(r'T$_\mathrm{eff}$ [K]')
    plt.ylabel('Absolute magnitude')
    plt.tight_layout()

    # plt.savefig('../hostDistribution.pdf')
    plt.show()
