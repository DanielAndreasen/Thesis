from __future__ import division
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from PyAstronomy import pyasl

plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
plt.rcParams['axes.spines.right'] = False
plt.rcParams['axes.spines.top'] = False
plt.rcParams['axes.linewidth'] = 2
plt.rcParams['xtick.major.width'] = 2
plt.rcParams['ytick.major.width'] = 2


if __name__ == '__main__':
     df = pyasl.ExoplanetEU2().getAllDataPandas()
     rename = {'name': 'plName',
                      'radius': 'plRadius',
                      'orbital_period': 'period',
                      'semi_major_axis': 'sma'}
     df.rename(columns=rename, inplace=True)
     idx = df['detection_type'] == 'Primary Transit'
     df = df[idx]

     plt.loglog(df['period'], df['plRadius'], '.', alpha=0.3)
     plt.xlabel('Period [days]')
     plt.ylabel(r'Planetary radius [R$_\mathrm{Jup}$]')

     plt.tight_layout()
    #  plt.savefig('../transitAll.pdf')
     plt.show()
