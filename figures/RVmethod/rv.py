from __future__ import division
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
plt.rcParams['axes.spines.right'] = False
plt.rcParams['axes.spines.top'] = False
plt.rcParams['axes.linewidth'] = 2
plt.rcParams['xtick.major.width'] = 2
plt.rcParams['ytick.major.width'] = 2


if __name__ == '__main__':
    fname = 'EPIC-9792_SOPHIE.rdb'
    t, rv, drv = np.loadtxt(fname, skiprows=2, unpack=True)
    K = 0.103  # km/s
    gamma = np.mean(rv)
    p = 3.25883210
    phase = ((t)%p)/p
    idx = np.argsort(phase)
    x = np.linspace(0, 1, 100)
    y = K*np.sin(2*np.pi*x-1.3)+gamma

    plt.subplot(211)
    plt.errorbar(t, rv, yerr=drv, fmt='o')
    plt.xlabel('Time')
    plt.ylabel('RV [ km/s]')

    plt.subplot(212)
    plt.errorbar(phase[idx], rv[idx], yerr=drv[idx], fmt='o')
    plt.plot(x, y)
    plt.hlines(gamma, 0, 1, linestyle='--', alpha=0.6)
    plt.xlabel('Phase, P=3.261 days')
    plt.ylabel('RV [ km/s]')

    plt.tight_layout()
    # plt.savefig('../RVmethod.pdf')
    plt.show()
