from __future__ import division
import numpy as np
import pandas as pd
from PyAstronomy import pyasl
import matplotlib.pyplot as plt
from astropy import constants as c
from joblib import Parallel, delayed

plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
plt.rcParams['axes.spines.right'] = False
plt.rcParams['axes.spines.top'] = False
plt.rcParams['axes.linewidth'] = 2
plt.rcParams['xtick.major.width'] = 2
plt.rcParams['ytick.major.width'] = 2


def _readSC():
    """Read and prepare the old SC"""
    names = ['star', 'hd', 'ra', 'dec', 'vmag', 'ervmag', 'par', 'erpar',
             'parsource', 'teff', 'tefferr', 'logg', 'loggerr', 'logglc',
             'erlogglc', 'vt', 'vterr', 'feh', 'feherr', 'mass', 'ermass',
             'author', 'link', 'source', 'update', 'comment', 'z1']
    df = pd.read_csv('WEBSITE_online.rdb', delimiter='\t', names=names, na_values=['NULL', '0'])
    df.star = df.star.str.strip()
    df.source.fillna(value=0, inplace=True)
    df.source = df.source.astype(bool)
    return df


def _readNew():
    """Read and prepare the new SC"""
    df = pd.read_csv('SC.csv', comment='#')
    df = df[df.convergence]
    df.linelist = df.linelist.str.strip()
    df.rename(columns={'teff': 'teffnew', 'tefferr': 'tefferrnew',
                       'logg': 'loggnew', 'loggerr': 'loggerrnew',
                       'feh': 'fehnew', 'feherr': 'feherrnew',
                       'vt': 'vtnew', 'vterr': 'vterrnew'},
              inplace=True)
    return df


def _merge(SC, new):
    df = pd.merge(left=SC, right=new, left_on='star', right_on='linelist', how='inner')
    df = df[~df.source]

    columns = ['star', 'vmag', 'teff', 'teffnew', 'tefferr', 'tefferrnew',
               'logg', 'loggnew', 'loggerr', 'loggerrnew',
               'feh', 'fehnew', 'feherr', 'feherrnew',
               'vt', 'vtnew', 'vterr', 'vterrnew', 'link', 'source']
    df = df.loc[:, columns]
    df.set_index('star', inplace=True)
    df.feherr.fillna(0.01, inplace=True)  # For HIP 11915
    df.teff = df.teff.astype(int)
    df.tefferr = df.tefferr.astype(int)
    return df


def _addCols(df):
    l = ['teff', 'tefferr', 'logg', 'loggerr', 'feh', 'feherr']
    r = [i+'new' for i in l]

    # Apply correction from Mortier+ 2014
    df.rename(columns={'loggnew': 'loggSpec'}, inplace=True)
    idx = (df.teffnew >= 4500) & (df.teffnew <= 7050) & (df.loggSpec > 4.2)
    df.loc[idx, 'loggnew'] = df.loggSpec[idx] - 3.89E-4*df.teffnew[idx] + 2.10
    df.loc[~idx, 'loggnew'] = df.loggSpec[~idx]
    df.loc[df.loggnew < 4.2, 'loggnew'] = df.loggSpec[df.loggnew < 4.2]

    # Get R and M from Torres+
    df['R'] = np.array(Parallel(n_jobs=4)(delayed(radTorres)(*df.loc[star, l].values) for star in df.index))[:, 0]
    df['Rnew'] = np.array(Parallel(n_jobs=4)(delayed(radTorres)(*df.loc[star, r].values) for star in df.index))[:, 0]
    df['Rperc'] = (df.Rnew-df.R)/df.R * 100
    # df['M'] = np.array(Parallel(n_jobs=4)(delayed(massTorres)(*df.loc[star, l].values) for star in df.index))[:, 0]
    # df['Mnew'] = np.array(Parallel(n_jobs=4)(delayed(massTorres)(*df.loc[star, r].values) for star in df.index))[:, 0]
    # df['Mperc'] = (df.Mnew-df.M)/df.M * 100
    # df['loggPerc'] = (df.logg-df.loggnew)/df.logg * 100

    df.R = df.R.apply(round, args=(3,))
    df.Rnew = df.Rnew.apply(round, args=(3,))
    df.Rperc = df.Rperc.apply(round, args=(1,))
    # df.Mnew = df.Mnew.apply(round, args=(3,))
    # df.M = df.M.apply(round, args=(3,))
    # df.Mperc = df.Mperc.apply(round, args=(1,))
    # df.loggPerc = df.loggPerc.apply(round, args=(1,))
    # df.loggnew = df.loggnew.apply(round, args=(2,))
    return df


def radTorres(teff, erteff, logg, erlogg, feh, erfeh, *kwargs):
    ntrials = 10000
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


def massTorres(teff, erteff, logg, erlogg, feh, erfeh, *kwargs):
    """Calculate a mass using the Torres calibration"""
    ntrials = 10000
    randomteff = teff + erteff * np.random.randn(ntrials)
    randomlogg = logg + erlogg * np.random.randn(ntrials)
    randomfeh = feh + erfeh * np.random.randn(ntrials)

    # Parameters for the Torres calibration:
    a1, a2, a3 = 1.5689, 1.3787, 0.4243
    a4, a5, a6 = 1.139, -0.1425, 0.01969
    a7 = 0.1010

    logM = np.zeros(ntrials)
    for i in xrange(ntrials):
        X = np.log10(randomteff[i]) - 4.1
        logM[i] = a1 + a2*X + a3*X**2 + a4*X**3 + a5*randomlogg[i]**2 + a6*randomlogg[i]**3 + a7*randomfeh[i]

    meanMasslog = np.mean(logM)
    sigMasslog = np.sqrt(np.sum(logM-meanMasslog)**2)/(ntrials-1)
    sigMasslogTot = np.sqrt(0.027**2 + sigMasslog**2)

    meanMass = 10**meanMasslog
    sigMass = 10**(meanMasslog + sigMasslogTot) - meanMass
    return meanMass, sigMass


if __name__ == '__main__':

    # Merge SC and new parameters
    df = _merge(_readSC(), _readNew())
    df['space'] = '    '

    # Add corrected logg, R, and M
    df = _addCols(df)

    z = 1/df.loggSpec.values
    size = (z-z.min())/(z.max()-z.min())*100
    color = z

    plt.figure()
    plt.plot([0, 25], [0, 25], '--k', alpha=0.3)
    plt.scatter(df.R, df.Rnew, s=size, c=1/z)
    plt.axis((0, 25, 0, 25))
    plt.xlabel(r'Literature radius $R_\odot$')
    plt.ylabel(r'New radius $R_\odot$')
    cbar = plt.colorbar()
    cbar.set_label(r'$\log(g)$ [cgs]', rotation=270, va='bottom')
    plt.grid(True)
    plt.tight_layout()

    # plt.savefig('../radiusVSradius.pdf')
    plt.show()
