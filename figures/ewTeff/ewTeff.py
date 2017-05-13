from __future__ import division
import os
import numpy as np
import matplotlib.pyplot as plt
from interpolation import interpolator
from utils import _run_moog as moog
from utils import Readmoog
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'



'''Show EW dependence on Teff, Fig. 13.4 in Gray'''

def moving_mean(dt, data):

    N = len(data)
    new_data = np.zeros( N )

    if dt == 1:
        return data

    for i in xrange(N):
        if (i-dt//2) < 0:
            d_data = data[0:i+dt//2]
        elif (i+dt//2) > N-1:
            d_data = data[i-dt//2:N]
        else:
            d_data = data[i-dt//2:i+dt//2]
        new_data[i] = np.mean(d_data)
    return new_data


def get_EW(teff):
    interpolator((teff, 4.44, 0.00, 1.00))
    moog()
    d = np.loadtxt('summary.out', skiprows=5, usecols=(6))
    os.remove('summary.out')
    os.remove('result.out')
    return d


if __name__ == '__main__':
    Teffs = np.linspace(3750, 8500, 1000)
    # This part was run in the FASMA folder since I need the directory with atmosphere models
    if not os.path.isfile('ewTeff.dat'):
        d = np.zeros((len(Teffs), 3))
        for i, Teff in enumerate(Teffs):
            ew1, ew2 = get_EW(Teff)
            d[i, 0] = Teff
            d[i, 1] = ew1
            d[i, 2] = ew2
        np.savetxt('ewTeff.dat', d)

    d = np.loadtxt('ewTeff.dat')
    d[:, 1] = moving_mean(50, d[:, 1])
    d[:, 2] = moving_mean(80, d[:, 2])

    plt.plot(Teffs, d[:, 1], '-', label=r'FeI:  4566.52$\AA$')
    plt.plot(Teffs, d[:, 2], '-', label=r'FeII: 4620.51$\AA$')
    plt.vlines(5777, 0, 80, linestyle='--', alpha=0.5)
    plt.xlabel('Teff [K]')
    plt.ylabel(r'EW [m$\AA$]')
    plt.legend(loc='best', frameon=False)

    # Remove right and yop spines
    ax = plt.gca()
    ax.spines['top'].set_color('none')
    ax.spines['right'].set_color('none')


    # plt.savefig('../ewTeff.pdf')
    plt.show()
