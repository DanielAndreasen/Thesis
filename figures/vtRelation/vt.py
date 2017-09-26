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


def read_data():
    return pd.read_table('../FASMA/FASMAtest.csv')


if __name__ == '__main__':
    df = read_data()

    plt.scatter(df.teff, df.vt, c=df.logg, s=5)
    plt.xlabel(r'T$_\mathrm{eff}$ [K]')
    plt.ylabel('vt [km/s]')
    cbar = plt.colorbar()
    cbar.set_label(r'$\log g$ [dex]', rotation=270, va='bottom')

    plt.tight_layout()
    # plt.savefig('../vtRelation.pdf')
    plt.show()
