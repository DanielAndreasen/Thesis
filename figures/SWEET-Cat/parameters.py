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

labels = {'teff': r'$T_\mathrm{eff}$ [K]',
          'tefferr': r'$\sigma T_\mathrm{eff}$ [K]',
          'logg': r'$\log(g)$ [cgs]',
          'loggerr': r'$\sigma \log(g)$ [cgs]',
          'feh': '[Fe/H]',
          'feherr': r'$\sigma$ [Fe/H]',
          'vt': r'$\xi_\mathrm{micro}$ [km/s]',
          'vterr': r'$\sigma\xi_\mathrm{micro}$ [km/s]',
          'lum': r'$L_\odot$',
          'mass': r'$M_\odot$',
          'masserr': r'$\sigma M_\odot$',
          'radius': r'$R_\odot$',
          'radiuserr': r'$\sigma R_\odot$',
          'age': r'Age $[Gyr]$'}


def massTorres(teff, erteff, logg, erlogg, feh, erfeh):
    """Calculate a mass using the Torres calibration"""
    ntrials = 100
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
        print randomteff[i]
        print X
        logM[i] = a1 + a2*X + a3*X**2 + a4*X**3 + a5*randomlogg[i]**2 + a6*randomlogg[i]**3 + a7*randomfeh[i]

    meanMasslog = np.mean(logM)
    sigMasslog = np.sqrt(np.sum(logM-meanMasslog)**2)/(ntrials-1)
    sigMasslogTot = np.sqrt(0.027**2 + sigMasslog**2)

    meanMass = 10**meanMasslog
    sigMass = 10**(meanMasslog + sigMasslogTot) - meanMass
    return meanMass, sigMass


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


def read_data(converged=None):
    df = pd.read_csv('SWEETCAT.csv', delimiter=r'\s+')
    if converged:
        # df = df[df['convergence']]
        pass
    params = zip(df.teff, df.tefferr, df.logg, df.loggerr, df.feh, df.feherr)
    # m = [massTorres(t, et, l, el, f, ef) for t, et, l, el, f, ef in params]
    r = [radTorres(t, et, l, el, f, ef) for t, et, l, el, f, ef in params]
    # df['mass'] = pd.Series(np.asarray(m)[:, 0])
    # df['masserr'] = pd.Series(np.asarray(m)[:, 1])
    df['radius'] = pd.Series(np.asarray(r)[:, 0])
    df['radiuserr'] = pd.Series(np.asarray(r)[:, 1])
    df['lum'] = (df.teff/5777)**4 * df.radius**2
    return df


def plot_data(df, x=None, y=None, z=None, xinverse=False, yinverse=False,
              xlog=None, ylog=None, zlog=None, fname=None):

    plt.figure()
    if z is not None:
        plt.scatter(df[x], df[y], c=df[z])
        if xinverse:
            xlim = plt.xlim()
            plt.xlim(xlim[1], xlim[0])
        if yinverse:
            ylim = plt.ylim()
            plt.ylim(ylim[1], ylim[0])
        cbar = plt.colorbar()
        cbar.set_label(labels[z], rotation=270, va='bottom')
    else:
        plt.scatter(df[x], df[y])
        if xinverse:
            xlim = plt.xlim()
            plt.xlim(xlim[1], xlim[0])
        if yinverse:
            ylim = plt.ylim()
            plt.ylim(ylim[1], ylim[0])

    if xlog:
        plt.xscale('log')
    if ylog:
        plt.yscale('log')

    plt.xlabel(labels[x])
    plt.ylabel(labels[y])

    if fname is not None:
        plt.savefig('../{}.pdf'.format(fname))


if __name__ == '__main__':
    df = read_data(converged=True)
    plot_data(df, x='teff', y='lum', z='logg', xinverse=True, ylog=True, fname='HR')
    plt.show()
