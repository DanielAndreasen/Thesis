from __future__ import division
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from interpolation import interpolator
from utils import _run_moog as moog
from utils import Readmoog

'''Show EW dependence on Teff, Fig. 13.4 in Gray'''


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
    # d = np.zeros((len(Teffs), 3))
    # for i, Teff in enumerate(Teffs):
    #     ew1, ew2 = get_EW(Teff)
    #     d[i, 0] = Teff
    #     d[i, 1] = ew1
    #     d[i, 2] = ew2
    # np.savetxt('ewTeff.dat', d)

    d = np.loadtxt('ewTeff.dat')

    plt.plot(Teffs, d[:,1], '-', label=r'FeI:  4566.52$\AA$')
    plt.plot(Teffs, d[:,2], '-', label=r'FeII: 4620.51$\AA$')
    plt.xlabel('Teff [K]')
    plt.ylabel(r'EW [m$\AA$]')
    plt.legend(loc='best', frameon=False)

    # plt.savefig('ewTeff.pdf')
    plt.show()
