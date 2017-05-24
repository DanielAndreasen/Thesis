from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
from astropy.modeling import models
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'


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
    plt.plot(x, g)
    plt.hlines(1, 0, 5, linestyle='--')
    plt.fill_between(x, g, 1, alpha=0.3)
    plt.text(1.5, 0.1, 'Absorped flux')

    # Plot EW representation
    plt.vlines([7, 7+ew], 0, 1, color='C0')
    plt.hlines(1, 6.8, 7+ew+0.2, linestyle='--')
    plt.fill_between([7, 7+ew], [0, 0], [1, 1], alpha=0.3, color='C0')
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


    plt.ylim(0, 1.1)
    plt.xlim(-0.5, 9)
    plt.yticks([0, 1], [0, r'$F_c$'])
    plt.xticks([2.5], [r'$\lambda_0$'])
    plt.xlabel('Wavelength')
    plt.ylabel('Flux')

    # Remove right and top spines
    ax = plt.gca()
    ax.spines['top'].set_color('none')
    ax.spines['right'].set_color('none')
    ax.spines['left'].set_linewidth(2)
    ax.spines['bottom'].set_linewidth(2)
    ax.xaxis.set_tick_params(width=2)
    ax.yaxis.set_tick_params(width=2)

    # plt.savefig('../ewTheoretical.pdf')
    plt.show()
