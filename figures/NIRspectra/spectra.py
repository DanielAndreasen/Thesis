from __future__ import division
import numpy as np
import pandas as pd
from glob import glob
from astropy.io import fits
import matplotlib.pyplot as plt

plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
plt.rcParams['axes.spines.right'] = False
plt.rcParams['axes.spines.top'] = False
plt.rcParams['axes.linewidth'] = 2
plt.rcParams['xtick.major.width'] = 2
plt.rcParams['ytick.major.width'] = 2

def get_wavelength(hdr, convert=False):
    """Return the wavelength vector calculated from the header of a FITS
    file.

    Input
    -----
    hdr : FITS header
      Header from a FITS ('CRVAL1', 'CDELT1', and 'NAXIS1' is required as keywords)
    convert : bool
      If True, multiple the wavelength vector with 10 (nm -> AA)

    Output
    ------
    w : ndarray
      Equidistant wavelength vector
    """
    w0, dw, n = hdr['CRVAL1'], hdr['CDELT1'], hdr['NAXIS1']
    w1 = w0 + dw * n
    w = np.linspace(w0, w1, n, endpoint=False)
    if convert:
        w *= 10
    return w


def get_HD20010(fname, w1, w2, rv=0):
    fname = 'HD20010/{}'.format(fname)
    w = get_wavelength(fits.getheader(fname))
    w = w * (1.0 + rv/299792.458)
    f = fits.getdata(fname)
    idx = (w1 <= w) & (w <= w2)
    w, f = w[idx], f[idx]
    f /= np.median(f)
    return w, f


def get_10Leo(fname, w1, w2, rv=0):
    w = get_wavelength(fits.getheader(fname))
    w = w * (1.0 + rv/299792.458)
    f = fits.getdata(fname)
    # print(w)
    # print(w1, w2)
    idx = (w1 <= w) & (w <= w2)
    w, f = w[idx], f[idx]
    f /= np.median(f)
    return w, f


def get_Arcturus(fname, w1, w2, rv=0):
    fname = 'Arcturus/{}'.format(fname)
    w = get_wavelength(fits.getheader(fname))
    w = w * (1.0 + rv/299792.458)
    f = fits.getdata(fname)
    idx = (w1 <= w) & (w <= w2)
    w, f = w[idx], f[idx]
    f /= np.median(f)
    return w, f




if __name__ == '__main__':
    wmin, wmax = 10214, 10260
    w1, f1 = get_HD20010(fname='10212-10262.fits', w1=wmin, w2=wmax, rv=33)
    w2, f2 = get_10Leo(fname='10Leo/10LeoYJband.fits', w1=wmin, w2=wmax, rv=10)
    w3, f3 = get_Arcturus(fname='10200-10259_s-obs.fits', w1=wmin, w2=wmax, rv=0)
    wmin, wmax = 16260, 16334
    w4, f4 = get_HD20010(fname='16257-16334.fits', w1=wmin, w2=wmax, rv=40)
    w5, f5 = get_10Leo(fname='10Leo/10LeoHband.fits', w1=wmin, w2=wmax, rv=15)
    w6, f6 = get_Arcturus(fname='16254-16334_s-obs.fits', w1=wmin, w2=wmax, rv=0)

    fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1)

    ax1.plot(w1, f1+0.4, color='C0', label='HD 20010')
    ax1.plot(w2, f2+0.2, color='C1', label='10 Leo')
    ax1.plot(w3, f3, color='C2', label='Arcturus')
    ax2.plot(w4, f4+0.4, color='C0', label='HD 20010')
    ax2.plot(w5, f5+0.2, color='C1', label='10 Leo')
    ax2.plot(w6, f6, color='C2', label='Arcturus')

    ax2.set_xlabel(r'Wavelength [$\AA{}$]')
    ax1.legend(loc='best', frameon=False)
    plt.tight_layout()

    # plt.savefig('../NIRspectra.pdf')
    plt.show()
