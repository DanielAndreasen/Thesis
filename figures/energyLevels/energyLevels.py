from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'


if __name__ == '__main__':
    n = np.arange(1, 9)
    En = -13.6/n**2

    ytick1 = map(lambda s: '%.2feV' % s, En[0:5])
    ytick1 += ['0.00eV']
    ytick2 = map(lambda s : r'$n=%d$' % s, n[0:5])
    ytick2 += [r'$n=\infty$']

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_yticks(list(En[0:5])+[0])
    ax.set_yticklabels(ytick1)
    ax.set_xticks([-10], [''])
    ax.set_ylabel(r'Energy level, $E_n$')
    ax.set_title('Energy levels for hydrogen')
    ax.set_ylim(-14.2, 0.5)

    ax1 = ax.twinx()
    ax1.hlines(En, 0, 1)
    ax.hlines([0], 0, 1, linestyle='--')
    ax1.set_yticks(list(En[0:5])+[0])
    ax1.set_yticklabels(ytick2)
    ax1.text(0.74235, -13.55, 'Ground state')
    ax1.text(0.64516,  -3.35, 'First excited state')
    ax1.text(0.58610,  -1.45, 'Second excited state')
    ax1.text(0.81017,   0.05, 'Ionization')

    ax1.set_xticks([-9])
    ax1.set_xticklabels([''])
    ax1.set_xlim(-0.1, 1.1)
    ax1.set_ylim(-14.2, 0.5)

    fig.tight_layout()
    # plt.savefig('../energyLevels.pdf')
    plt.show()
