from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'

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
    plt.plot(d[:, 0], d[:, 1], '-', alpha=0.7)
    for i, di in enumerate(ds):
        plt.plot(di[0], di[1], 'o', c='C%s' % i)
    plt.text(-4.6, -5.8, 'Weak line', rotation=30)
    plt.text(-1.6, -4.3, 'Saturation', rotation=11)
    plt.text(1.0, -3.0, 'Strong line', rotation=15)
    plt.xlim(-5, 3)
    plt.ylim(-7.2, -2.6)
    plt.xlabel(r'log $gf$')
    plt.ylabel(r'$\log(EW/\lambda)$')
    ax = plt.gca()
    ax.spines['top'].set_color('none')
    ax.spines['right'].set_color('none')

    plt.subplot(212)
    w0 = 4566.52
    for i in range(1, 5):
        w, f = np.loadtxt('synth%s.asc' % i, skiprows=2, unpack=True)
        plt.plot(w, f, 'C%s' % (i-1))

    plt.xlim(w0-1.6, w0+1.5)
    plt.ylim(0, 1.05)
    plt.xlabel(r'Wavelength [$\AA$]')
    plt.ylabel('Flux')
    ax = plt.gca()
    ax.spines['top'].set_color('none')
    ax.spines['right'].set_color('none')

    plt.tight_layout()

    # plt.savefig('../cog.pdf')
    plt.show()
