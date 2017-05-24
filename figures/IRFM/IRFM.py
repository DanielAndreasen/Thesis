from __future__ import division
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from astropy import constants as c
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'


def solar_radius(flux, fluxE):
    R = c.R_sun.value
    d = c.au.value
    return 2*np.sqrt(fluxE/flux) * d / (2*R)


def solar_teff(flux, fluxE):
    def angD(flux, fluxE):
        return 2*np.sqrt(fluxE/flux)
    theta = angD(flux, fluxE)
    sigma = c.k_B.value
    Teff = ( 4*fluxE/(sigma*theta**2) )**(1/4)
    return Teff.values


if __name__ == '__main__':
    df = pd.read_csv('IRFM_Sun.csv')

    rsun = solar_radius(df.Flux, df.FluxE)
    Teff = solar_teff(df.Flux, df.FluxE)
    print 'Solar radius: %.3f(%.3f)' % (np.mean(rsun), np.std(rsun))
    print 'Solar Teff: %d(%d)' % (np.mean(Teff), np.std(Teff))


    # Plot
    plt.semilogy(df.w, df.Flux, 'o-', label='Calculated flux')
    plt.semilogy(df.w, df.FluxE, 'o-', label='Measured flux at Earth')

    ax = plt.gca()
    ax.spines['top'].set_color('none')
    ax.spines['right'].set_color('none')
    ax.spines['left'].set_linewidth(2)
    ax.spines['bottom'].set_linewidth(2)
    ax.xaxis.set_tick_params(width=2)
    ax.yaxis.set_tick_params(width=2)

    plt.xlabel(r'Wavelength [$\mu$m]')
    plt.ylabel(r'Flux [W m$^{-2}$ Hz$^{-1}$]')
    plt.legend(loc='best', frameon=False)
    plt.tight_layout()

    # plt.savefig('../IRFM.pdf')
    plt.show()
