from __future__ import division
import numpy as np
import pandas as pd
from glob import glob
from utils import Readmoog
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'


def mad(data, axis=None):
    '''Mean absolute deviation'''
    return np.mean(np.absolute(data - np.mean(data, axis)), axis)


def get_data(results):
    dfi = Readmoog(fname=results[0], version=2013).all_table()
    abundances = np.zeros((len(results)+1, len(dfi)))
    ews = [str(round(ew, 3)) for ew in dfi['EWin'].values]

    for i, result in enumerate(results):
        dfi = Readmoog(fname=result, version=2013).all_table()
        abundances[i] = dfi['abund'].values

    df = pd.DataFrame(abundances, columns=dfi.wavelength)

    for wavelength in df.columns:
        m = mad(df[wavelength][:-1].values, axis=None)
        df.loc[100, wavelength] = m

    data = np.vstack((dfi.wavelength, ews, df.loc[100, :].values)).T
    data = pd.DataFrame(data, columns=('wavelength', 'ew', 'mad')).astype(float)
    data['outlier'] = False
    data.sort_values('ew', inplace=True)
    return data


def func(x, a, c, d):
    return a*np.exp(c*x)+d


def adjust_style():
    fig.subplots_adjust(hspace=0.1)

    ax1.spines['top'].set_color('none')
    ax1.spines['right'].set_color('none')
    ax1.spines['left'].set_linewidth(2)
    ax1.spines['bottom'].set_linewidth(2)
    ax1.xaxis.set_tick_params(width=2)
    ax1.yaxis.set_tick_params(width=2)
    ax2.spines['top'].set_color('none')
    ax2.spines['right'].set_color('none')
    ax2.spines['left'].set_linewidth(2)
    ax2.spines['bottom'].set_linewidth(2)
    ax2.xaxis.set_tick_params(width=2)
    ax2.yaxis.set_tick_params(width=2)


if __name__ == '__main__':
    results = glob('Sumlist*.out')
    xticks = range(0, 201, 25)

    df = get_data(results)

    x, y, w = df['ew'].values, df['mad'].values, df['wavelength'].values
    popt, pcov = curve_fit(func, x, y, p0=(0.04, -0.08, 0.02))
    yfit = func(x, *popt)
    y1 = func(x, *popt)
    res = y-yfit
    r = res.copy()

    sigma = 3.1

    m, s = np.median(res), np.std(res)
    outliers = abs(res) > m + sigma*s

    while True in outliers:
        outliers = abs(res) > m + sigma*s
        imax = max(res) == res
        wmax = w[imax][0]
        I = df['wavelength'] == wmax
        df.loc[I, 'outlier'] = True

        x, y, w = x[~imax], y[~imax], w[~imax]
        popt, _ = curve_fit(func, x, y, p0=(0.04, -0.08, 0.02))
        yfit = func(x, *popt)
        res = y-yfit

        m, s = np.median(res), np.std(res)
        outliers = abs(res) > m + sigma*s

    outlier = df['outlier']
    df['detrended'] = df['mad'] / y1

    fig = plt.figure(figsize=(8, 4))
    ax1 = fig.add_subplot(211)
    ax1.plot(df.loc[outlier, 'ew'], df.loc[outlier, 'mad'], '.C3')
    ax1.plot(df.loc[~outlier, 'ew'], df.loc[~outlier, 'mad'], '.C0')
    ax1.plot(x, yfit, '-C1')
    ax1.set_ylabel('MAD')
    ax1.set_xticks(xticks)
    ax1.set_xticklabels(['']*len(xticks))

    ax2 = fig.add_subplot(212)
    ax2.plot(df.loc[outlier, 'ew'], df.loc[outlier, 'detrended'], '.C3')
    ax2.plot(df.loc[~outlier, 'ew'], df.loc[~outlier, 'detrended'], '.C0')
    ax2.set_xlabel(r'EW [m$\AA$]')
    ax2.set_ylabel('Detrended MAD')

    adjust_style()

    # plt.savefig('../disperse_lines.pdf')
    plt.show()
