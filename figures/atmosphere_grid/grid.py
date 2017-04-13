from __future__ import division
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from glob import glob
import gzip
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'

path = '/home/daniel/Documents/Uni/phdproject/programs/FASMA/models/kurucz95'
# path = '/home/daniel/Documents/Uni/phdproject/programs/FASMA/models/apogee_kurucz'
# path = '/home/daniel/Documents/Uni/phdproject/programs/FASMA/models/marcs'


def extract_feh(directories):
    d = np.zeros(len(directories))
    for i, directory in enumerate(directories):
        z = directory.rpartition('/')[-1]
        sign = z[0]
        if sign == 'm':
            d[i] = - float(z[1:])/10
        else:
            d[i] = float(z[1:])/10
    return np.sort(d)


def extract_teff_logg(model):
    '13000g35.m10.gz'
    model = model.rpartition('/')[-1]
    p = model.split('.')[0].split('g')
    teff = int(p[0])
    logg = float(p[1])/10
    return teff, logg


def extract_t_1stlayer(model):
    f = gzip.open(model, compresslevel=1)
    data = f.readlines()
    model = np.loadtxt(data[23:-2])
    return model[0, 1]


if __name__ == '__main__':

    directories = np.sort(glob('%s/*' % path))
    fehs = extract_feh(directories)
    teff_min, teff_max = 3000, 10000

    directory = directories[9]
    models = np.array(glob('%s/*' % (directory)))

    p = np.array([extract_teff_logg(model) for model in models])
    teff, logg = p[:, 0], p[:, 1]
    idx = (teff_min <= teff) & (teff <= teff_max)
    teff, logg = teff[idx], logg[idx]
    T = np.array([extract_t_1stlayer(model) for model in models[idx]])

    plt.scatter(teff, logg, s=6, c=T, cmap=cm.inferno)
    plt.scatter(5777, 4.44, c=3725.8, marker='*', s=100, cmap=cm.inferno)

    plt.xlim(teff_min, teff_max)
    plt.title('[Fe/H]=%.2f' % fehs[9])
    plt.xlabel(r'$T_\mathrm{eff}$ [K]')
    plt.ylabel(r'$\log g$')

    cbar = plt.colorbar()
    cbar.set_label('Temperature in 1st layer', rotation=270, va='bottom')
    plt.tight_layout()

    # plt.savefig('../model_atmosphere.pdf')
    plt.show()
