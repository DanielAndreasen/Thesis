from __future__ import division
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'

'''Stellar mass and radius from asteroseismic scaling relation'''


def get_mass(Dv, vmax, Teff=5777):
    a1 = (134.9/Dv)**(4/5)
    a2 = (3.05/(vmax*np.sqrt(Teff/5777)))**(-3/5)
    return a1 * a2


def get_radius(Dv, vmax, Teff=5777):
    a1 = (134.9/Dv)**2
    a2 = 3.05/(vmax*np.sqrt(Teff/5777))
    return (a1 * a2)**(1/5)


def adjust_style():
    fig.subplots_adjust(hspace=0.1)
    ax.spines['top'].set_color('none')
    ax.spines['bottom'].set_color('none')
    ax.spines['left'].set_color('none')
    ax.spines['right'].set_color('none')
    ax.tick_params(labelcolor='w', top='off', bottom='off', left='off', right='off')

    xticks = range(120, 141, 5)
    ax1.set_xticks(xticks)
    ax1.set_xticklabels(['']*len(xticks))
    ax1.spines['top'].set_color('none')
    ax1.spines['right'].set_color('none')
    ax1.spines['left'].set_linewidth(2)
    ax1.spines['bottom'].set_linewidth(2)
    ax1.xaxis.set_tick_params(width=2)
    ax1.yaxis.set_tick_params(width=2)

    ax2.set_xticks(xticks)
    # ax1.set_xticklabels(['']*len(xticks))
    ax2.spines['top'].set_color('none')
    ax2.spines['right'].set_color('none')
    ax2.spines['left'].set_linewidth(2)
    ax2.spines['bottom'].set_linewidth(2)
    ax2.xaxis.set_tick_params(width=2)
    ax2.yaxis.set_tick_params(width=2)


if __name__ == '__main__':
    Npoints = 100
    Dv_all = np.linspace(120, 140, Npoints)  # microHz
    vmax_all = np.linspace(2.5, 3.5, Npoints)  # mHz
    Ms = np.zeros((len(Dv_all), len(vmax_all)))
    Rs = np.zeros((len(Dv_all), len(vmax_all)))
    X, Y = np.meshgrid(Dv_all, vmax_all)
    for i, Dv in enumerate(Dv_all):
        for j, vmax in enumerate(vmax_all):
            Ms[i, j] = get_mass(Dv, vmax)
            Rs[i, j] = get_radius(Dv, vmax)

    fig = plt.figure()
    ax = fig.add_subplot(111)

    ax1 = fig.add_subplot(211)
    im1 = ax1.contourf(X, Y, Ms, 100)
    ax1.plot(134.9, 3.05, '*y', ms=10)
    cbar = fig.colorbar(im1)
    cbar.set_label('Solar mass', rotation=270, va='bottom')

    ax2 = fig.add_subplot(212)
    im2 = ax2.contourf(X, Y, Rs, 100)
    ax2.plot(134.9, 3.05, '*y', ms=10)
    cbar = fig.colorbar(im2)
    cbar.set_label('Solar radius', rotation=270, va='bottom')

    # Add labels and adjust style
    adjust_style()
    ax.set_ylabel(r'$\nu_{\mathrm{max}}$ [mHz]')
    ax1.set_title('Asteroseismic scaling relation')
    ax2.set_xlabel(r'$\Delta\nu$ [$\mu$Hz]')
    plt.tight_layout()

    # plt.savefig('../scaling_relation.pdf')
    plt.show()
