from __future__ import division
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
plt.rcParams['axes.spines.right'] = False
plt.rcParams['axes.spines.top'] = False
plt.rcParams['axes.linewidth'] = 2
plt.rcParams['xtick.major.width'] = 2
plt.rcParams['ytick.major.width'] = 2


def extract_parameters(dataframe):
    dataframe['teff_true'] = [int(teff.split('-')[0]) for teff in dataframe.linelist]
    dataframe['logg_true'] = [float(logg.split('-')[1]) for logg in dataframe.linelist]
    dataframe['feh_true'] = [float(feh.split('-')[2]) for feh in dataframe.linelist]
    return dataframe


if __name__ == '__main__':
    df = pd.read_table('arcturus.dat', delimiter=r'\s+')
    dfm = df[df['model'] == 'marcs']
    dfm = extract_parameters(dfm)

    dfk = df[df['model'] == 'kurucz95']
    dfk = extract_parameters(dfk)

    plt.figure(figsize=(12, 6))
    ###########################################
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

    ###########################################
    # plt.subplot(232)
    # plt.hist(dfm.logg, label='Marcs', alpha=0.6)
    # plt.hist(dfk.logg, label='Kurucz', alpha=0.6)
    # # plt.errorbar(dfm.logg, dfm.logg_true, yerr=dfm.loggerr, fmt='o-', label='Marcs')
    # # plt.errorbar(dfk.logg, dfk.logg_true, yerr=dfk.loggerr, fmt='o-', label='Kurucz')
    # plt.ylabel('logg derived from FASMA')
    # plt.legend(loc='best', frameon=False)
    #
    # plt.subplot(235)
    # plt.errorbar(dfm.logg, dfm.logg - dfm.logg_true, yerr=dfm.loggerr, fmt='o-')
    # plt.errorbar(dfk.logg, dfk.logg - dfk.logg_true, yerr=dfk.loggerr, fmt='o-')
    # plt.xlabel('True logg from PHOENIX')
    # plt.grid(True)
    #
    #
    # ###########################################
    # plt.subplot(233)
    # plt.hist(dfm.feh, label='Marcs', alpha=0.6)
    # plt.hist(dfk.feh, label='Kurucz', alpha=0.6)
    # # plt.errorbar(dfm.feh_true, dfm.feh, yerr=dfm.feherr, fmt='o-', label='Marcs')
    # # plt.errorbar(dfk.feh_true, dfk.feh, yerr=dfk.feherr, fmt='o-', label='Kurucz')
    # plt.plot([min(dfm.feh_true), max(dfm.feh_true)], [min(dfm.feh_true), max(dfm.feh_true)], '--k', alpha=0.5)
    # plt.ylabel('[Fe/H] derived from FASMA')
    # plt.legend(loc='best', frameon=False)
    #
    # plt.subplot(236)
    # plt.errorbar(dfm.feh, dfm.feh - dfm.feh_true, yerr=dfm.feherr, fmt='o-')
    # plt.errorbar(dfk.feh, dfk.feh - dfk.feh_true, yerr=dfk.feherr, fmt='o-')
    # plt.xlabel('True [Fe/H] from PHOENIX')
    # plt.grid(True)


    # plt.savefig('Simulated_teff.pdf')
    plt.show()
