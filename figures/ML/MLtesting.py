from __future__ import division
import cPickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import linear_model
from sklearn import preprocessing
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, Ridge

plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
plt.rcParams['axes.spines.right'] = False
plt.rcParams['axes.spines.top'] = False
plt.rcParams['axes.linewidth'] = 2
plt.rcParams['xtick.major.width'] = 2
plt.rcParams['ytick.major.width'] = 2


if __name__ == '__main__':
    df = pd.read_csv('combined.csv')
    df.dropna(axis=1, inplace=True)
    df.set_index('linelist', inplace=True)
    wavelengths = df.columns.values[:-4]
    labels = df.columns.values[-4:]
    for i, wavelength in enumerate(map(float, wavelengths)):
        if (wavelength - float(wavelengths[i+1])) > 0:
            break

    ws = {str(w): 'w{}'.format(i+1) for i, w in enumerate(wavelengths)}
    df.rename(columns=ws, inplace=True)
    df = df[df.vt > 0.1]
    df = df[df.teff > 5200]

    # Train
    xlabel = ws.values()
    ylabel = ['teff', 'logg', 'feh', 'vt']
    X = df.loc[:, xlabel]
    X = preprocessing.scale(X)
    y = df.loc[:, ylabel]

    N = 1000
    scores = np.zeros((N, 4))
    for j in range(N):
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33)
        clf = linear_model.LinearRegression()
        clf.fit(X_train, y_train)

        y_pred = clf.predict(X_test)
        for i, label in enumerate(ylabel):
            score = mean_absolute_error(y_test[label], y_pred[:, i])
            scores[j, i] = score

    plt.subplot(221)
    plt.hist(scores[:, 0], histtype='step', lw=2)
    plt.xlabel('Teff [K]')
    plt.subplot(222)
    plt.hist(scores[:, 1], histtype='step', lw=2)
    plt.xlabel('logg [dex]')
    plt.subplot(223)
    plt.hist(scores[:, 2], histtype='step', lw=2)
    plt.xlabel('[Fe/H] [dex]')
    plt.subplot(224)
    plt.hist(scores[:, 3], histtype='step', lw=2)
    plt.xlabel('vt [km/s]')

    plt.tight_layout()

    # plt.savefig('../ML.pdf')
    plt.show()
