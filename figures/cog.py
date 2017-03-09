from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

'''Curve of growth'''


if __name__ == '__main__':

    d = np.loadtxt('cog.dat')
    idx = np.argsort(d[:, 0])
    d = d[idx]

    loggf_points = [-4, -2, 0, 2.036]
    ds = np.zeros((len(loggf_points), 2))
    for i, loggf_point in enumerate(loggf_points):
        idx = d[:, 0]-loggf_point == min(abs(d[:, 0]-loggf_point))
        ds[i, 0] = d[idx, 0]
        ds[i, 1] = d[idx, 1]

    plt.subplot(211)
    plt.plot(d[:, 0], d[:, 1], '-')
    for di in ds:
        plt.plot(di[0], di[1], 'o')
    plt.text(-4.6, -5.7, 'Weak line', rotation=33)
    plt.text(-2.2, -4.4, 'Saturation', rotation=10)
    plt.text(1.0, -3.0, 'Strong line', rotation=15)
    plt.xlabel(r'log $gf$')
    plt.ylabel(r'$\log(EW/\lambda)$')

    plt.subplot(212)
    w0 = 4566.52
    for i in range(1, 5):
        w, f = np.loadtxt('synth%s.asc' % i, skiprows=2, unpack=True)
        plt.plot(w, f, 'C%s' % i)

    plt.xlim(w0-1.6, w0+1.5)
    plt.xlabel(r'Wavelength [$\AA$]')
    plt.ylabel('Flux')
    plt.tight_layout()

    # plt.savefig('cog.pdf')
    plt.show()