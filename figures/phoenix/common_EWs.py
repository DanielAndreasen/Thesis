from __future__ import division
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
plt.rcParams['axes.spines.right'] = False
plt.rcParams['axes.spines.top'] = False
plt.rcParams['axes.linewidth'] = 2
plt.rcParams['xtick.major.width'] = 2
plt.rcParams['ytick.major.width'] = 2


def read_star(fname):
    columns = ('wavelength', 'element', 'EP', 'loggf', 'EW')
    df = pd.read_csv(fname, delimiter=r'\s+',
                     names=columns,
                     skiprows=1,
                     usecols=['wavelength', 'EW'])
    return df


if __name__ == '__main__':
    df_syn = read_star('Arcturus_PHOENIX.moog')
    df_arc = read_star('ArcturusSummer.moog')
    df = pd.merge(df_syn, df_arc, left_on='wavelength', right_on='wavelength')
    df['diff'] = df['EW_y']-df['EW_x']

    print df['diff'].describe()

    plt.plot(df['EW_y'], df['diff'], 'o')
    plt.xlabel(r'EW Arcturus [m$\AA$]')
    plt.ylabel(r'EW (Arcturus-PHOENIX) [m$\AA$]')
    plt.tight_layout()
    plt.grid()

    # plt.savefig('../commonEWS.pdf')
    plt.show()
