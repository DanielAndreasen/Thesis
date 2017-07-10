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


def get_phase(time, period):
    return (time % period)/period



if __name__ == '__main__':
    fname = 'ktwo211089792.txt'
    P = 3.26083740

    time, flux = np.loadtxt(fname, usecols=(0, 1), unpack=True)
    phase = get_phase(time-0.45*P, P)
    idx = np.argsort(phase)

    plt.subplot(211)
    plt.plot(time, flux, '-')
    plt.xlabel('Time')
    plt.ylabel('Flux')

    plt.subplot(212)
    plt.plot(phase[idx], flux[idx], '.C0')
    plt.xlabel('Phase, P=3.261 days')

    plt.tight_layout()
    # plt.savefig('../transitMethod.pdf')
    plt.show()
