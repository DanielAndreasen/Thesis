from __future__ import division
import os
import numpy as np
from astropy.io import fits
from plot_fits import nrefrac
from scipy.interpolate import interp1d


def read_phoenix(fname):
    path = os.path.expanduser('~/.plotfits/')
    pathwave = os.path.join(path, 'WAVE_PHOENIX-ACES-AGSS-COND-2011.fits')
    w = fits.getdata(pathwave)
    f = fits.getdata(fname)
    nre = nrefrac(w)  # Correction for vacuum to air (ground based)
    w = w/nre
    return w, f


if __name__ == '__main__':
    w1, w2 = 10000, 25000
    dA = 0.01
    w, f = read_phoenix('lte04300-1.50-0.5.fits')

    idx = (w1 <= w) & (w <= w2)
    w, f = w[idx], f[idx]

    N = int((w[-1] - w[0]) / dA)

    flux_int_func = interp1d(w, f, kind='linear')
    ll_int = np.arange(N) * dA + w[0]
    flux_int = flux_int_func(ll_int)
    hdr = fits.getheader('lte04300-1.50-0.5.fits')
    hdr["NAXIS1"] = N
    hdr["CDELT1"] = dA
    hdr["CRVAL1"] = w[0]

    fits.writeto('Arcturus_PHOENIX.fits', flux_int, hdr, clobber=True)
