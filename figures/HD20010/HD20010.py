from __future__ import division
import pandas as pd
from utils import Readmoog
import matplotlib.pyplot as plt
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'

"""
Abundances for HD20010 before and after refining the line list. The impact is
rather small but visible.
"""

if __name__ == '__main__':
    datasets = ('HD20010_before.out', 'HD20010_after.out')

    for i, dataset in enumerate(datasets):
        time = dataset.split('_')[-1].replace('.out', '').title()

        # Read and prepare the dataset
        df = Readmoog(fname=dataset)
        df = df.all_table()
        df = df[df.atom == 'FeI']
        df = df[df.EP <= 5.5]
        df['abund'] = df['abund']-df['abund'].median()

        # Standard deviation
        s = df['abund'].std()

        # Plot the abundances and standard deviation
        plt.plot(df['EP'], df['abund'], 'o', c='C%s' % i, alpha=0.6, label=time)
        plt.hlines(-s, 2.0, 5.5, color='C%s' % i)
        plt.hlines(+s, 2.0, 5.5, color='C%s' % i)

    plt.hlines(0, 2.0, 5.5, linestyle='--', alpha=0.6)

    plt.legend(frameon=False, loc='best')
    plt.xlabel('Excitation potential [eV]')
    plt.ylabel('Iron abundance - median abundance')

    y1, y2 = plt.ylim()
    plt.ylim(1.1*y1, 1.1*y2)
    plt.tight_layout()

    # plt.savefig('../HD20010.pdf')
    plt.show()
