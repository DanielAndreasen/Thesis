from __future__ import division
from astropy.io import fits
import matplotlib.pyplot as plt
from plot_fits import get_wavelength

plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
plt.rcParams['axes.spines.right'] = False
plt.rcParams['axes.spines.top'] = False
plt.rcParams['axes.linewidth'] = 2
plt.rcParams['xtick.major.width'] = 2
plt.rcParams['ytick.major.width'] = 2


if __name__ == '__main__':
    fname1 = 'HD79210_vis/6246.0-6355.0.fits'
    fname2 = 'HD79210_nir/10427.0-10621.0.fits'

    f1 = fits.getdata(fname1)
    w1 = get_wavelength(fits.getheader(fname1))
    f2 = fits.getdata(fname2)
    w2 = get_wavelength(fits.getheader(fname2))

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.spines['top'].set_color('none')
    ax.spines['bottom'].set_color('none')
    ax.spines['left'].set_color('none')
    ax.spines['right'].set_color('none')
    ax.tick_params(labelcolor='w', top='off', bottom='off', left='off', right='off')
    ax.set_title('HD 79210 - optical and NIR')
    ax.set_xlabel(r'Wavelength [$\AA$]')
    ax.set_ylabel('Flux')

    ax1 = fig.add_subplot(211)
    ax1.plot(w1, f1)

    ax2 = fig.add_subplot(212)
    ax2.plot(w2, f2)

    plt.tight_layout()
    # plt.savefig('../opticalVSnir.pdf')
    plt.show()
