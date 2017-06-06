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


def extract_parameters(df):
    df['teff_true'] = map(lambda s: int(s.split('-')[0]),   df.linelist)
    df['logg_true'] = map(lambda s: float(s.split('-')[1]), df.linelist)
    df['feh_true']  = map(lambda s: float(s.split('-')[2]), df.linelist)
    return df


if __name__ == '__main__':
    for fname in ('simulation_free.dat', 'simulation_fix.dat'):
        t = fname.split('_')[1].strip('.dat')
        df = pd.read_table(fname, delimiter=r'\s+')
        df = extract_parameters(df)
        dfm = df[df['model'] == 'marcs']
        dfk = df[df['model'] == 'kurucz95']

        plt.figure(figsize=(12, 6))
        ###########################################
        plt.subplot(211)
        # plt.title('Simulation: {}'.format(t))
        plt.errorbar(dfm.teff_true, dfm.teff, yerr=dfm.tefferr, fmt='o-', label='Marcs')
        plt.errorbar(dfk.teff_true, dfk.teff, yerr=dfk.tefferr, fmt='o-', label='Kurucz')
        plt.plot([min(dfm.teff_true), max(dfm.teff_true)], [min(dfm.teff_true), max(dfm.teff_true)], '--k', alpha=0.5)
        plt.ylabel(r'T$_\mathrm{eff}$ derived from FASMA [K]')
        plt.legend(loc='best', frameon=False)

        plt.subplot(212)
        plt.errorbar(dfm.teff_true, dfm.teff - dfm.teff_true, yerr=dfm.tefferr, fmt='o-')
        plt.errorbar(dfk.teff_true, dfk.teff - dfk.teff_true, yerr=dfk.tefferr, fmt='o-')
        plt.xlabel(r'True T$_\mathrm{eff}$ from PHOENIX [K]')
        plt.ylabel(r'T$_\mathrm{eff}$ (PHOENIX-FASMA) [K]')
        plt.grid(True)

        # plt.savefig('../simulated_teff_{}.pdf'.format(t))
    plt.show()
