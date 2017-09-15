from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
from astropy.modeling import models
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
# plt.rcParams['axes.spines.right'] = False
plt.rcParams['axes.spines.top'] = False
plt.rcParams['axes.linewidth'] = 2
plt.rcParams['xtick.major.width'] = 2
plt.rcParams['ytick.major.width'] = 2


def gaussian(amplitude, mean, stddev):
    g = models.Gaussian1D(amplitude=amplitude, mean=mean, stddev=stddev)
    area = np.sqrt(2*np.pi) * abs(amplitude*stddev)
    return g, area


if __name__ == '__main__':
    x = np.linspace(0, 5, 100)
    c = np.ones(len(x))
    g, area = gaussian(-0.8, 2.5, 0.5)
    g = g(x)+1
    ew = area  # Since continuum = 1

    # Plot absorption line
    fig, ax = plt.subplots(1)
    ax.plot(x, g)
    ax.hlines(1, 0, 5, linestyle='--')
    ax.fill_between(x, g, 1, alpha=0.3)
    ax.text(1.5, 0.1, 'Absorped flux')
    ax.set_ylim(0, 1.1)
    ax.set_xlim(-0.5, 9)
    ax.set_yticks([0, 1])
    ax.set_yticklabels([0, r'$F_c$'])
    ax.set_xticks([2.5])
    ax.set_xticklabels([r'$\lambda_0$'])
    ax.set_xlabel('Wavelength')
    ax.set_ylabel('Flux')

    # Plot EW representation
    ax1 = ax.twinx()
    ax1.vlines([7, 7+ew], 0, 1, color='C0')
    ax1.hlines(1, 6.8, 7+ew+0.2, linestyle='--')
    ax1.hlines(0, 7, 7+ew, color='C0')
    ax1.fill_between([7, 7+ew], [0, 0], [1, 1], alpha=0.3, color='C0')
    ax1.set_yticks([0, 1])
    ax1.set_yticklabels(['0', '1'])
    ax1.set_ylim(0, 1.1)
    plt.text(7.3, 0.15, 'EW')
    xp, yp = 7.0, 0.13
    plt.annotate('', (xp, yp),
                (xp+ew, yp),
                ha="right", va="center",
                arrowprops=dict(arrowstyle='<|-|>',
                                shrinkA=0,
                                shrinkB=0,
                                fc="k", ec="k"))

    # Plot text combining two plots
    plt.text(4.3, 0.7, 'Equal area')
    xp, yp = 2.5, 0.68
    plt.annotate('', (xp, yp),
                (7.0+ew/2, yp),
                ha="right", va="center",
                arrowprops=dict(arrowstyle='<|-|>',
                                shrinkA=0,
                                shrinkB=0,
                                fc="k", ec="k"))

    plt.tight_layout()
    # plt.savefig('../ewTheoretical.pdf')
    plt.show()
