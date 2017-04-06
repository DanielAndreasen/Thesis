from __future__ import division
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from glob import glob

grid = {'teff': (3750, 4000, 4250, 4500, 4750, 5000, 5250, 5500, 5750, 6000,
                     6250, 6500, 6750, 7000, 7250, 7500, 7750, 8000, 8250, 8500,
                     8750, 9000, 9250, 9500, 9750, 10000, 10250, 10500, 10750,
                     11000, 11250, 11500, 11750, 12000, 12250, 12500, 12750, 13000,
                     14000, 15000, 16000, 17000, 18000, 19000, 20000, 21000, 22000,
                     23000, 24000, 25000, 26000, 27000, 28000, 29000, 30000, 31000,
                     32000, 33000, 34000, 35000, 36000, 37000, 38000, 39000),
            'feh': (-3.0, -2.5, -2.0, -1.5, -1.0, -0.5, -0.3, -0.2, -0.1, 0.0,
                    0.1, 0.2, 0.3, 0.5, 1.0),
            'logg': (0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0)}
path = '/home/daniel/Documents/Uni/phdproject/programs/FASMA/models/kurucz95'


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
    # print model
    p = model.split('.')[0].split('g')
    teff = int(p[0])
    logg = float(p[1])/10
    return teff, logg



if __name__ == '__main__':

    directories = glob('%s/*' % path)
    fehs = extract_feh(directories)

    for feh directory in zip(fehs, directories):
        models = glob('%s/*' % (directory))
        plt.figure()
        plt.title('[Fe/H]=%s' % feh)
        for model in models:
            teff, logg = extract_teff_logg(model)
            plt.scatter(teff, logg, color='C0')
        plt.xlabel('Teff')
        plt.ylabel('logg')
    plt.show()
