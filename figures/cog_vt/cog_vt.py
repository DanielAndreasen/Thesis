from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'

'''Curve of growth as function of vt.
The curves (cog_vt?.dat) are done manually by changing the vt in the solar
atmosphere model, then formatting the output nicely.
'''


if __name__ == '__main__':

    vts = [0.5, 2.5, 5.0]
    for i in range(1, 4):
        gf, rw = np.loadtxt('cog_vt%s.dat' % i, unpack=True)
        idx = np.argsort(gf)
        gf, rw = gf[idx], rw[idx]
        plt.plot(gf, rw, label=r'$\xi=%.2f$km/s' % vts[i-1])

    plt.legend(loc='best', frameon=False)
    plt.xlabel(r'log $gf$')
    plt.ylabel(r'$\log(EW/\lambda)$')
    ax = plt.gca()
    ax.spines['top'].set_color('none')
    ax.spines['right'].set_color('none')
    ax.spines['left'].set_linewidth(2)
    ax.spines['bottom'].set_linewidth(2)
    ax.xaxis.set_tick_params(width=2)
    ax.yaxis.set_tick_params(width=2)

    # plt.savefig('../cog_vt.pdf')
    plt.show()
