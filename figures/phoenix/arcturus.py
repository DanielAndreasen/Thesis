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


def read_arcturus():
    pass
    return w, f


if __name__ == '__main__':
    wa, fa = read_arcturus()
    wm, fm = read_phoenix()


    w1, w2 = 10150, 10200
    i1 = (w1 <= wa) & (wa <= w2)
    i2 = (w1 <= wm) & (wm <= w2)
    wa, fa = wa[i1], fa[i1]
    wm, fm = wm[i2], fm[i2]

    plt.plot(wa, fa, '-', label='Arcturus')
    plt.plot(wm, fm, '-', label='PHOENIX')
    plt.xlabel(r'Wavelength [$\AA$]')
    plt.ylabel('Normalized flux')
    plt.legend(loc='best', frameon=False)

    # plt.savefig('../arcturus_phoenix.pdf')
    plt.show()
