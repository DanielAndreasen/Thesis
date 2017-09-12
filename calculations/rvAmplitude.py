from __future__ import division
import numpy as np
import pandas as pd
import astropy.units as u
import astropy.constants as c
import matplotlib.pyplot as plt

plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
plt.rcParams['axes.spines.right'] = False
plt.rcParams['axes.spines.top'] = False
plt.rcParams['axes.linewidth'] = 2
plt.rcParams['xtick.major.width'] = 2
plt.rcParams['ytick.major.width'] = 2


def get_K(e, mp, ms, P, i=90):
    Mjup = c.M_jup.value
    Mearth = c.M_earth.value
    a = (28.4329*u.m/u.s)/np.sqrt(1-e**2)
    K = a*(mp*Mearth*np.sin(np.deg2rad(i))/Mjup) * ms**(-2/3) * P**(-1/3)
    return K


def get_K1(e, mp, ms, a, i=90):
    Mjup = c.M_jup.value
    Mearth = c.M_earth.value
    k = (28.4329*u.m/u.s)/np.sqrt(1-e**2)
    K = k*(mp*Mearth*np.sin(np.deg2rad(i))/Mjup) * ms**(-1/2) * a**(-1/2)
    return K




if __name__ == '__main__':
    Mplanet = 1  # Earth mass
    P_G = 1  # Period for G type star [yr]
    P_M = 0.1  # Period for M type star [yr]

    amplitude_G = get_K(e=0, mp=Mplanet, ms=1.0, P=P_G)
    amplitude_M = get_K(e=0, mp=Mplanet, ms=0.3, P=P_M)

    print('Amplitude for G type: {}'.format(amplitude_G.to('cm/s')))
    print('Amplitude for M type: {}'.format(amplitude_M.to('cm/s')))

    amplitude_G = get_K1(e=0, mp=Mplanet, ms=1.0, a=1.0)
    amplitude_M = get_K1(e=0, mp=Mplanet, ms=0.3, a=0.1)

    print('Amplitude for G type: {}'.format(amplitude_G.to('cm/s')))
    print('Amplitude for M type: {}'.format(amplitude_M.to('cm/s')))
