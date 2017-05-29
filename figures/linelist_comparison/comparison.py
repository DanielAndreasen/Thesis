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


def get_combined_data():
    names = ('wavelength', 'element', 'EP', 'loggf', 'EW')
    df1 = pd.read_table('linelist1.moog', delimiter=r'\s+', names=names, skiprows=1)
    df2 = pd.read_table('linelist2.moog', delimiter=r'\s+', names=names, skiprows=1)
    df1['wavelength'] = [round(w, 2) for w in df1['wavelength']]
    df2['wavelength'] = [round(w, 2) for w in df2['wavelength']]
    df = pd.merge(df1, df2, how='outer',
                  left_on='wavelength',
                  right_on='wavelength',
                  suffixes=('_1', '_2'))
    df['diff'] = df['EW_1'] - df['EW_2']
    return df


if __name__ == '__main__':

    df = get_combined_data()
    m, s = np.nanmedian(df['diff']), np.nanstd(df['diff'])

    plt.figure()
    plt.plot(df['EW_1'], df['diff'], '.')
    plt.hlines([m, m+s, m-s], 4, 200)

    plt.xlabel(r'EW$_1$ [m$\AA$]')
    plt.ylabel(r'EW$_1$ - EW$_2$ [m$\AA$]')
    # plt.savefig('../linelist_comparison.pdf')
    plt.show()
