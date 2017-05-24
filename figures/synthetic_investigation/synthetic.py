from __future__ import division
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'


def synth_data(synth='synth.asc', nr=3):
    with open(synth, 'rb') as f:
        line = f.readline()
        rows = int(line.split('=')[1].strip(' '))

    data = np.zeros((nr, rows, 2))
    with open(synth, 'r') as f:
        i = -1
        for j, line in enumerate(f):
            if line.startswith('the'):
                row = 0
                pass
            elif line.startswith('start'):
                i += 1
            else:
                w = float(line[0:12].strip(' '))
                f = float(line[13::].strip(' '))
                data[i][row] = [w, f]
                row += 1
    os.remove(synth)
    return data


def moog(reduced_linelist=False):
    if reduced_linelist:
        os.system('mv lines.moog lines_original.moog')
        os.system('mv lines_temp.moog lines.moog')
    with open('sun.txt', 'w') as f:
        f.write('sun.par\nq\n')
    os.system('MOOGSILENT < sun.txt; clear')
    for file in ('out1', 'out2', 'sun.txt'):
        os.remove(file)

    if reduced_linelist:
        os.system('mv lines_original.moog lines.moog')
    return synth_data()


def remove_line(wavelength, linelist):
    new = ''
    with open(linelist, 'r') as lines:
        for line in lines:
            if line.startswith(wavelength):
                continue
            new += line

    with open('lines_temp.moog', 'w') as fout:
        fout.write(new)


def adjust_style():
    fig.subplots_adjust(hspace=0.1)
    ax.spines['top'].set_color('none')
    ax.spines['bottom'].set_color('none')
    ax.spines['left'].set_color('none')
    ax.spines['right'].set_color('none')
    ax.tick_params(labelcolor='w', top='off', bottom='off', left='off', right='off')

    ax1.spines['top'].set_color('none')
    ax1.spines['right'].set_color('none')
    ax1.spines['left'].set_linewidth(2)
    ax1.spines['bottom'].set_linewidth(2)
    ax1.xaxis.set_tick_params(width=2)
    ax1.yaxis.set_tick_params(width=2)
    ax2.spines['top'].set_color('none')
    ax2.spines['right'].set_color('none')
    ax2.spines['left'].set_linewidth(2)
    ax2.spines['bottom'].set_linewidth(2)
    ax2.xaxis.set_tick_params(width=2)
    ax2.yaxis.set_tick_params(width=2)


if __name__ == '__main__':
    wavelength = 15550.439
    observed = np.loadtxt('observed.asc')
    observed[:, 1] /= np.median(observed[:, 1])
    fehs = [' 0.20', ' 0.00', '-0.20']
    xticks = range(15548, 15554)

    # Run MOOG
    synthetics1 = moog()
    remove_line(str(wavelength), 'lines.moog')
    synthetics2 = moog(True)


    fig = plt.figure(figsize=(8, 4))
    ax = fig.add_subplot(111)
    ax.set_ylabel('Normalized flux')

    ax1 = fig.add_subplot(211)
    ax1.plot(observed[:, 0], observed[:, 1], '-k', lw=3, alpha=0.5, label='Sun')
    for feh, synthetic in zip(fehs, synthetics1):
        ax1.plot(synthetic[:, 0], synthetic[:, 1], '--', label='[Fe/H]={}'.format(feh))
    ax1.legend(loc='best', frameon=False)
    ax1.set_xticks(xticks)
    ax1.set_xticklabels(['']*len(xticks))

    ax2 = fig.add_subplot(212, sharey=ax1)
    ax2.plot(observed[:, 0], observed[:, 1], '-k', lw=3, alpha=0.5)
    for synthetic in synthetics2:
        ax2.plot(synthetic[:, 0], synthetic[:, 1], '--')
    ax2.set_xlabel(r'Wavelength [$\AA$]')

    adjust_style()
    plt.tight_layout()
    # plt.savefig('../synthetic_investigation.pdf')
    plt.show()
