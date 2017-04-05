import os
import numpy as np
from glob import glob
from astropy.io import fits
from PyAstronomy import pyasl
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d


def nrefrac(wavelength, density=1.0):
    """
    Refactory index by Elden 1953 from vacuum to air.
    """
    wl = np.array(wavelength)

    s2 = (1e4/wl)**2
    n = 1.0 + 6.4328e-5 + (2.94981e-2/(146.0 - s2)) + (2.554e-4/(41. - s2))
    return density * n


def get_wavelength(fname):
    w = fits.getdata(wpath)
    nre = nrefrac(w)  # Correction for vacuum to air (ground based)
    w = w/nre
    return w


def params_from_name(fname):
    p = fname[3:].split('-')[:3]
    p[2] = p[2].rpartition('.')[0]
    Teff = int(p[0])
    logg = float(p[1])
    feh = float(p[2])
    return Teff, logg, feh


def params_to_name(fname, resolution):
    params = list(params_from_name(fname))
    params += [resolution]

    fout = '{}-{}-{}-res:{}.fits'.format(*params)
    return fout


def equidistant_wavelength(w):
    dA = 0.01
    N = int((w[-1] - w[0]) / dA)
    w_new = np.arange(N) * dA + w[0]
    return w_new


def same_w_grid(w, f):
    w_new = equidistant_wavelength(w)
    interp = interp1d(w, f, kind='linear')
    f_new = interp(w_new)
    return w_new, f_new


def header_information(w):
    crval1 = w[0]
    cdelt1 = w[1]-w[0]
    naxis1 = len(w)
    return crval1, cdelt1, naxis1


if __name__ == '__main__':
    resolution = 100000
    w0, w1 = 10060, 23310
    wpath = os.path.expanduser('~/.plotfits/WAVE_PHOENIX-ACES-AGSS-COND-2011.fits')
    w = get_wavelength(wpath)
    idx = (w0 <= w) & (w <= w1)
    w = w[idx]

    for fname in sorted(glob('lte*.fits'))[3:]:
        fout = params_to_name(fname, resolution)
        print fout

        y = fits.getdata(fname)
        y = y[idx]
        w_new, y_new = same_w_grid(w, y)
        print 'Convolving...'
        y_new = pyasl.instrBroadGaussFast(w_new, y_new, resolution, edgeHandling="firstlast", fullout=False, maxsig=None)

        crval1, cdelt1, naxis1 = header_information(w_new)
        hdr = fits.Header()
        hdr["NAXIS1"] = naxis1
        hdr["CDELT1"] = cdelt1
        hdr["CRVAL1"] = crval1
        fits.writeto(fout, y_new, hdr, overwrite=True)
