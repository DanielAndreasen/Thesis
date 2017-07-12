from __future__ import division
import numpy as np
import pandas as pd
from PyAstronomy import pyasl
import matplotlib.pyplot as plt
from astropy import constants as c

plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
plt.rcParams['axes.spines.right'] = False
plt.rcParams['axes.spines.top'] = False
plt.rcParams['axes.linewidth'] = 2
plt.rcParams['xtick.major.width'] = 2
plt.rcParams['ytick.major.width'] = 2


if __name__ == '__main__':
    df = pd.DataFrame(pyasl.ExoplanetEU().data)

    planet_mass = np.array([c.M_earth.value, 1.024E26 , c.M_jup.value])/c.M_jup.value

    plt.semilogy(df['discovered'], df['plMass'], '.')
    plt.xlabel('Discovery year')
    plt.ylabel(r'Exoplanet mass [M$_\mathrm{Jup}$]')
    x1, x2 = plt.xlim()
    plt.hlines(planet_mass, x1, x2, linestyle='--')
    plt.xlim(x1, x2)
    plt.tight_layout()

    # plt.savefig('../exoplanetMass.pdf')
    plt.show()
