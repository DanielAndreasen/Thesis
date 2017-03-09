from __future__ import division
import numpy as np
import matplotlib.pyplot as plt

'''EW dependence on gravity using:
Teff, feh, vt = 5777, 0.00, 1.0
'''


def get_cog(logg):
    d = np.loadtxt('cog_logg%s.dat' % int(logg))
    idx = np.argsort(d[:, 0])
    d = d[idx]
    return d


def get_synthetic(logg):
    d = np.loadtxt('synth_g%s.asc' % int(logg), skiprows=2)
    return d


def get_abundance(logg):
    return float(np.loadtxt('abundance_g%s.dat' % int(logg), skiprows=1, usecols=(6)))



if __name__ == '__main__':
    loggs = [2.0, 3.0, 4.0, 5.0]
    for logg in loggs:
        cog = get_cog(logg)
        synthetic = get_synthetic(logg)

        plt.subplot(211)  # Upper: CoG
        plt.plot(cog[:, 0], cog[:, 1], label='log g=%.2f' % logg)

        plt.subplot(223)  # Lower left: Synthetic line
        plt.plot(synthetic[:, 0], synthetic[:, 1])


    plt.subplot(224)  # Lower right: abundance vs. logg
    abundance = [get_abundance(logg) for logg in loggs]
    p = np.polyfit(loggs, abundance, 1)
    f = np.poly1d(p)
    plt.plot(loggs, f(loggs), '-k')
    plt.plot(loggs, abundance, 'o')
    plt.text(2.2, 7.5, r'A=%.2f$\cdot \log g$' % p[0])
    plt.xlabel(r'$\log g$')
    plt.ylabel('Abundance')


    ## Styling
    plt.subplot(211)
    plt.legend(loc='best', frameon=False)
    plt.xlabel(r'log $gf$')
    plt.ylabel(r'$\log(EW/\lambda)$')

    plt.subplot(223)
    w0 = 4620.510
    dw = 0.2
    plt.xlim(w0-dw, w0+dw)
    plt.xlabel(r'Wavelength [$\AA$]')
    plt.ylabel('Flux')
    plt.xticks([w0], [w0])

    plt.tight_layout()
    # plt.savefig('ewGravity.pdf')
    plt.show()
