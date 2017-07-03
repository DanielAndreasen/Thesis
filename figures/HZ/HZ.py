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

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


"""Habitable zones from:
http://xxx.lanl.gov/abs/1301.6674
"""


def hz(teff, lum, model=1):
    if model == 1:  # Recent Venus
        p = [1.7753, 1.4316E-4, 2.9875E-9, -7.5702E-12, -1.1635E-15]
    elif model == 2:  # Runaway greenhouse
        p = [1.0512, 1.3242E-4, 1.5418E-9, -7.9895E-12, -1.8328E-15]
    elif model == 3:  # Moist greenhouse
        p = [1.0140, 8.1774E-5, 1.7063E-9, -4.3241E-12, -6.6462E-16]
    elif model == 4:  # Maximum greenhouse
        p = [0.3438, 5.8942E-5, 1.6558E-9, -3.0045E-12, -5.2983E-16]
    elif model == 5:  # Early Mars
        p = [0.3179, 5.4513E-5, 1.5313E-9, -2.7786E-12, -4.8997E-16]

    Seff_sun = p[0]
    ts = teff-5780
    a, b, c, d = p[1], p[2], p[3], p[4]
    Seff = Seff_sun + a*ts + b*ts**2 + c*ts**3 + d*ts**4
    dist = np.sqrt(lum/Seff)
    return dist


def radTorres(teff, erteff, logg, erlogg, feh, erfeh):
    ntrials = 100
    randomteff = teff + erteff*np.random.randn(ntrials)
    randomlogg = logg + erlogg*np.random.randn(ntrials)
    randomfeh = feh + erfeh*np.random.randn(ntrials)

    # Parameters for the Torres calibration:
    b1, b2, b3 = 2.4427, 0.6679, 0.1771
    b4, b5, b6 = 0.705, -0.21415, 0.02306
    b7 = 0.04173

    logR = np.zeros(ntrials)
    for i in xrange(ntrials):
        X = np.log10(randomteff[i]) - 4.1
        logR[i] = b1 + b2*X + b3*X**2 + b4*X**3 + b5*randomlogg[i]**2 + b6*randomlogg[i]**3 + b7*randomfeh[i]

    meanRadlog = np.mean(logR)
    sigRadlog = np.sqrt(np.sum((logR-meanRadlog)**2))/(ntrials-1)
    sigRadlogTot = np.sqrt(0.014**2 + sigRadlog**2)

    meanRad = 10**meanRadlog
    sigRad = 10**(meanRadlog + sigRadlogTot) - meanRad
    return meanRad, sigRad


def _readSC():
    """Read and prepare the new SC"""
    df = pd.read_csv('../SWEET-Cat-radius/SC.csv', comment='#')
    df = df[df.convergence]
    df.linelist = df.linelist.str.strip()
    params = zip(df.teff, df.tefferr, df.logg, df.loggerr, df.feh, df.feherr)
    r = [radTorres(t, et, l, el, f, ef) for t, et, l, el, f, ef in params]
    df['radius'] = pd.Series(np.asarray(r)[:, 0])
    df['lum'] = (df.teff/5777)**4 * df.radius**2
    return df


if __name__ == '__main__':
    df = _readSC()
    # Formula only for MS stars
    df = df[df['logg'] >= 4.2]

    dfe = pyasl.ExoplanetEU()
    dfe = pd.DataFrame(dfe.getAllData())
    df = pd.merge(df, dfe, left_on='linelist', right_on='stName')
    p = ['plName', 'teff', 'logg', 'feh', 'lum', 'radius', 'period', 'detType', 'mag_v', 'sma']
    for i in range(5):
        name = 'HZ{}'.format(i+1)
        df[name] = [hz(teff, lum, model=i+1) for teff, lum in df[['teff', 'lum']].values]

    for teff, sma, radius, hz1, hz2 in df[['teff', 'sma', 'plRadius', 'HZ2', 'HZ4']].values:
        if (hz1 <= sma) and (sma <= hz2):
            plt.plot([hz1, hz2], [teff, teff], '-oC0', lw=5, alpha=0.5)
        else:
            plt.plot([hz1, hz2], [teff, teff], '-oC1', lw=1, alpha=0.4, ms=2)

    idx = (df['HZ2'] <= df['sma']) & (df['sma'] <= df['HZ4'])
    print df.loc[idx, p[:-1]+['HZ2', 'sma', 'HZ4', 'plRadius', 'plMass']]
    plt.scatter(df.sma[idx],  df.teff[idx],  alpha=0.9, c='C2', s=30)
    plt.scatter(df.sma[~idx], df.teff[~idx], alpha=0.4, c='C3', s=5)

    plt.xlabel('Semi-major axis [AU]')
    plt.ylabel('Teff [K]')
    # plt.savefig('../HZ.pdf')
    plt.show()
