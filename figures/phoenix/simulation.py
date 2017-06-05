from __future__ import division
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def read_data(fname):
    return pd.read_table(fname, delimiter=r'\s+')


def extract_parameters(dataframe):
    dataframe['teff_true'] = [int(teff.split('-')[0]) for teff in dataframe.linelist]
    dataframe['logg_true'] = [float(logg.split('-')[1]) for logg in dataframe.linelist]
    dataframe['feh_true'] = [float(feh.split('-')[2]) for feh in dataframe.linelist]
    return dataframe



if __name__ == '__main__':
    dfm = read_data('marcs.dat')
    dfm = extract_parameters(dfm)

    dfk = read_data('kurucz.dat')
    dfk = extract_parameters(dfk)


    plt.subplot(211)
    plt.errorbar(dfm.teff_true, dfm.teff, yerr=dfm.tefferr, fmt='o-', label='Marcs')
    plt.errorbar(dfk.teff_true, dfk.teff, yerr=dfk.tefferr, fmt='o-', label='Kurucz')
    plt.plot([min(dfm.teff_true), max(dfm.teff_true)], [min(dfm.teff_true), max(dfm.teff_true)], '--k', alpha=0.5)
    plt.ylabel('Teff derived from FASMA')
    plt.legend(loc='best', frameon=False)

    plt.subplot(212)
    plt.errorbar(dfm.teff_true, dfm.teff - dfm.teff_true, yerr=dfm.tefferr, fmt='o-')
    plt.errorbar(dfk.teff_true, dfk.teff - dfk.teff_true, yerr=dfk.tefferr, fmt='o-')
    plt.xlabel('True Teff from PHOENIX')
    plt.grid(True)

    # plt.savefig('Simulated_teff.pdf')
    plt.show()
