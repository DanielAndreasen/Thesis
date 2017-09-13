from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
from loggf2abundance import get_abundance
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'

'''Curve of growth'''


if __name__ == '__main__':

    df = get_abundance()

    abundances = [6.2, 7.2, 8.2, 9.2]
    ds = np.zeros((len(abundances), 2))
    for i, abundance in enumerate(abundances):
        abundance_diff = abs(df['abund']-abundance)
        idx = abundance_diff == min(abundance_diff)
        ds[i, 0] = df.loc[idx, 'abund']
        ds[i, 1] = df.loc[idx, 'logRWin']

    plt.subplot(211)
    plt.plot(df['abund'], df['logRWin'], '-', alpha=0.7)
    for i, di in enumerate(ds):
        plt.plot(di[0], di[1], 'o', c='C%s' % i)
    plt.text(6.0, -5.6, 'Weak line', rotation=30)
    plt.text(7.5, -4.75, 'Saturation', rotation=11)
    plt.text(9.0, -4.2, 'Strong line', rotation=15)
    plt.xlim(5.9, 9.7)
    plt.ylim(-6.1, -4.2)
    plt.xlabel('Abundance')
    plt.ylabel(r'$\log(EW/\lambda)$')
    ax = plt.gca()
    ax.spines['top'].set_color('none')
    ax.spines['right'].set_color('none')
    ax.spines['left'].set_linewidth(2)
    ax.spines['bottom'].set_linewidth(2)
    ax.xaxis.set_tick_params(width=2)
    ax.yaxis.set_tick_params(width=2)

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
    ax.spines['left'].set_linewidth(2)
    ax.spines['bottom'].set_linewidth(2)
    ax.xaxis.set_tick_params(width=2)
    ax.yaxis.set_tick_params(width=2)

    plt.tight_layout()

    # plt.savefig('../cog.pdf')
    plt.show()
