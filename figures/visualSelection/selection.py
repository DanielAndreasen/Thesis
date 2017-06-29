from __future__ import division
import gzip
import numpy as np
import pandas as pd
from astropy.io import fits
import matplotlib.pyplot as plt
from VALDextraction import VALDmail
from plot_fits import get_wavelength

plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
plt.rcParams['axes.spines.right'] = False
plt.rcParams['axes.spines.top'] = False
plt.rcParams['axes.linewidth'] = 2
plt.rcParams['xtick.major.width'] = 2
plt.rcParams['ytick.major.width'] = 2


def merge_data():
    names = 'Wavelength Ele excit loggf EW'.split(' ')
    d1 = pd.read_csv('Fe1.moog', names=names, delimiter=r'\s+', skiprows=1)
    d1['Wavelength'] = map(lambda x: round(x, 2), d1['Wavelength'])
    d2 = pd.read_csv('linelist_newEW.moog', names=names, delimiter=r'\s+', skiprows=1)
    df = pd.merge(d1, d2, left_on='Wavelength', right_on='Wavelength', how='outer')
    return df


def read_raw_VALD(fname):
    df = []
    with gzip.open(fname, 'r') as lines:
        for i, line in enumerate(lines):
            if i < 2:
                continue
            try:
                line = line.split(',')[:-1]  # Don't care about references
                line[0] = line[0].replace("'", "")  # Remove single quotes
                line[1:] = map(float, line[1:])  # Convert the rest to floats
                df.append(line)
            except IndexError:  # Reached the reference part
                break

    names = ('element', 'wavelength', 'EP', 'loggf',
             'rad', 'stark', 'waals', 'f')
    df = pd.DataFrame(df, columns=names)
    return df.loc[:, ('element', 'wavelength', 'EP', 'loggf')]


def read_sun(w1, w2):
    path = '/home/daniel/.plotfits/solarspectrum_01.fits'
    w = get_wavelength(fits.getheader(path))
    f = fits.getdata(path)

    idx = (w1 <= w) & (w <= w2)
    w, f = w[idx], f[idx]
    f /= np.median(f)
    f /= f.max()
    return w, f


if __name__ == '__main__':
    df = merge_data()
    d = df[np.isnan(df['EW_y'])]
    wavelength = np.random.choice(d['Wavelength'])

    # print 'Using wrong wavelength at {:.2f}AA'.format(wavelength)
    # VALDmail(wavelength=wavelength, step=1.5)
    dd = read_raw_VALD('lines1.gz')
    dd['EW'] = dd['loggf'] - dd['EP']*5040/5777
    dd['EW'] = (dd['EW'] - min(dd['EW'])) / (max(dd['EW'])-min(dd['EW']))
    dd['EW'] = dd['EW']**2
    w, f = read_sun(dd['wavelength'].min(), dd['wavelength'].max())

    idx = (dd['element'] == 'Fe 1') | (dd['element'] == 'Fe 2')
    d1 = dd[idx]
    d2 = dd[~idx]

    plt.plot(w, f)
    x1, x2 = plt.xlim()
    y1, y2 = plt.ylim()

    for line, strength in d1[['wavelength', 'EW']].values:
        plt.vlines(line, 1-(1-y1)*strength, 1, color='C2', alpha=strength)
    for line, strength in d2[['wavelength', 'EW']].values:
        plt.vlines(line, 1-(1-y1)*strength, 1, color='C1', alpha=strength)
    plt.xlim(x1, x2)
    plt.ylim(y1-0.005, y2)
    ax = plt.gca()
    ax.xaxis.get_major_formatter().set_useOffset(False)

    w_mid = (x2+x1)/2
    xticks = (w_mid-0.90, w_mid-0.45, w_mid, w_mid+0.45, w_mid+0.90)
    xticks = map(lambda x: round(x, 2), xticks)
    plt.xticks(xticks, xticks)

    plt.xlabel(r'Wavelength [$\AA$]')
    plt.ylabel('Flux')

    # plt.savefig('../visualSelection.pdf')
    plt.show()
