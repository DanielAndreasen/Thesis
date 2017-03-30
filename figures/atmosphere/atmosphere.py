from __future__ import division
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


me = 9.11*10**(-31)
kb = 8.6173303*10**(-5)
def dist(T):
    # v = np.linspace(10, 5e15, 100)
    v = np.linspace(0.1, 450, 100)
    # coef = 4*np.pi*(me/(2*np.pi*kb*T))**(3/2)
    # d = coef * v**2 * np.exp(-me*v**2/(2*kb*T))
    d = v**2 * np.exp(-v**2/(T))
    return v, d


if __name__ == '__main__':
    df = pd.read_csv('sun.atm')
    Temps = [5000, 6000, 7000, 8000, 9000]

    plt.plot(df.rhotau, df.temp)
    for Temp in Temps:
        dd = np.abs(df.temp-Temp)
        idx = dd == min(dd)
        offset = df.rhotau.values[idx]
        v1, f1 = dist(Temp)
        plt.plot(f1/(max(f1))+offset, v1+Temp, 'C1')

    plt.xlabel(r'$\rho x$')
    plt.ylabel(r'T')
    plt.show()
