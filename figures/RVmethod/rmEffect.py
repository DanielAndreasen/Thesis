from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.anchored_artists import AnchoredSizeBar
from mpl_toolkits.axes_grid1.inset_locator import inset_axes, zoomed_inset_axes

plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
plt.rcParams['axes.spines.right'] = False
plt.rcParams['axes.spines.top'] = False
plt.rcParams['axes.linewidth'] = 2
plt.rcParams['xtick.major.width'] = 2
plt.rcParams['ytick.major.width'] = 2


def add_sizebar(ax, x, y1, y2):
    ax.plot(x, y1, '--k', alpha=0.7)
    ax.plot(x, y1+y2)
    ax.set_xlim(-0.2, 0.2)


if __name__ == '__main__':
    x1 = np.linspace(-np.pi, np.pi, 1000)
    y1 = -100*np.sin(x1)
    y2 = -40*np.cos(x1*35 + 35/np.pi)
    idx = (x1 > -0.09) & (0.09 > x1)
    y2[~idx] = 0

    fig, ax = plt.subplots(1)
    ax.plot(x1, y1+y2)
    ax.plot(x1[idx], y1[idx], '--k', alpha=0.7)
    ax.set_xlabel(r'Phase [P=$2\pi$]')
    ax.set_ylabel('RV [m/s]')
    plt.grid(True)

    axins = inset_axes(ax, width="40%", height=1., loc=1)
    plt.xticks(visible=False)
    plt.yticks(visible=False)
    add_sizebar(axins, x1, y1, y2)

    # plt.savefig('../RMeffect.pdf')
    plt.show()
