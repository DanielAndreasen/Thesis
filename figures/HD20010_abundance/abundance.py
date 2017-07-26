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

"""Difference in abundance from lowest and highest measured EW for HD20010.
when an overlap was observed."""


def readmoog(fname):
    """Read the summary (with abundances) from MOOG abfind"""
    with open(fname, 'r') as lines:
        for line in lines:
            if line.startswith('wavelength'):
                break
        data = []
        for line in lines:
            line = line.split(' ')
            try:
                line = map(float, filter(None, line))
                data.append(line)
            except ValueError:
                return np.array(data)


if __name__ == '__main__':
    dlow = readmoog('error_low.out')
    dhigh = readmoog('error_high.out')

    plt.subplot(211)
    plt.plot(dlow[:, 0], dhigh[:, 5]-dlow[:, 5],  '.')
    plt.xlabel(r'Wavelength [$\AA$]')
    plt.ylabel('Difference in abundance [dex]')
    plt.xlim(9500, 25000)
    plt.ylim(-0.05, 0.7)
    plt.subplot(212)
    plt.hist(dhigh[:, 5]-dlow[:, 5], histtype='step', lw=2)
    plt.xlabel('Difference in abundance [dex]')

    plt.tight_layout()

    plt.savefig('../HD20010abundance_error.pdf')
    plt.show()
