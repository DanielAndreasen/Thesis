from __future__ import division
import os
import numpy as np
import pandas as pd
from astropy.io import fits
import matplotlib.pyplot as plt
from rv_measure import main as rv_measure
from plot_fits import get_wavelength, dopplerShift, nrefrac

plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
plt.rcParams['axes.spines.right'] = False
plt.rcParams['axes.spines.top'] = False
plt.rcParams['axes.linewidth'] = 2
plt.rcParams['xtick.major.width'] = 2
plt.rcParams['ytick.major.width'] = 2


def read_arcturus(fname):
    w = get_wavelength(fits.getheader(fname))
    f = fits.getdata(fname)
    return w, f


def read_phoenix(fname):
    path = os.path.expanduser('~/.plotfits/')
    pathwave = os.path.join(path, 'WAVE_PHOENIX-ACES-AGSS-COND-2011.fits')
    w = fits.getdata(pathwave)
    f = fits.getdata(fname)
    nre = nrefrac(w)  # Correction for vacuum to air (ground based)
    w = w/nre
    return w, f


if __name__ == '__main__':
    w1, w2 = 10150, 10200

    # Arcturus
    wa, fa = read_arcturus('10148-10207_s-obs.fits')
    # wa, fa = read_arcturus('ArcturusSummer.fits')
    i1 = (w1 <= wa) & (wa <= w2)
    wa, fa = wa[i1], fa[i1]
    f = np.polyfit(wa, fa, 1)
    fa /= np.poly1d(f)(wa)
    fa /= np.median(fa)

    # Model
    wm, fm = read_phoenix('lte04300-1.50-0.5.fits')
    i2 = (w1 <= wm) & (wm <= w2)
    wm, fm = wm[i2], fm[i2]

    fm /= np.median(fm)

    rv = rv_measure('10148-10207_s-obs.fits', 'lte04300-1.50-0.5.fits')
    fm, wm = dopplerShift(wm, fm, v=rv[0], fill_value=0.95)

    plt.figure(figsize=(10, 4))
    plt.plot(wm, fm, '-', label='PHOENIX')
    plt.plot(wa, fa, '-', label='Arcturus')
    plt.xlabel(r'Wavelength [$\AA$]')
    plt.ylabel('Normalized flux')
    plt.legend(loc='best', frameon=False)
    plt.tight_layout()

    # plt.savefig('../arcturus_phoenix.pdf')
    plt.show()
