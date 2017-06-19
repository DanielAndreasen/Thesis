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


if __name__ == '__main__':
    fe = 7.47
    df = pd.read_table('Fe1_before_recal.log', delimiter=r'\s+')
    idx = abs(df['abund']-fe) <= 1.0


    plt.plot(df.loc[~idx, 'wavelength'], df.loc[~idx, 'abund'], '.C3', alpha=0.7)
    plt.plot(df.loc[idx,  'wavelength'], df.loc[idx,  'abund'], '.C2', alpha=0.7)
    plt.xlabel(r'Wavelength [$\AA$]')
    plt.ylabel('Iron abundance')

    x1, x2 = plt.xlim()
    plt.hlines(fe, x1*1.05, x2*0.99, linestyle='--', alpha=0.5)
    plt.xlim(x1, x2)
    plt.tight_layout()

    # plt.savefig('../calibrated_loggf.pdf')
    plt.show()
