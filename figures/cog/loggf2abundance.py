from __future__ import division
import os
import numpy as np
from utils import Readmoog
from utils import _update_par as batch


def read_cog(fname, w):
    """Read the cog_logg?.dat files
    col1: loggf
    col2: logRW
    """
    d = np.loadtxt(fname)
    idx = np.argsort(d[:, 0])
    d = d[idx]
    d[:, 1] = w*np.exp(d[:, 1])  # Convert to EW
    return d


def make_linelist(w, id, ep, loggf, ew):
    """Make a MOOG line list for one line with different EWs"""
    d = np.zeros((len(ew), 5))
    d[:, 0] = w
    d[:, 1] = id
    d[:, 2] = ep
    d[:, 3] = loggf
    d[:, 4] = ew
    np.savetxt('linelist.moog', d,
               fmt=('%9.3f', '%10.1f', '%9.2f', '%9.3f', '%28.1f'),
               header='A header')


def get_abundance():
    w = 4566.52
    d = read_cog('cog.dat', w=w)
    make_linelist(w=w, id=26.0, ep=3.30, loggf=-2.164, ew=d[:, 1])
    batch(atmosphere_model='out.atm')
    os.system('MOOGSILENT > /dev/null')
    params = (5777, 4.44, 0.0, 1.0)
    m = Readmoog(params=params)
    df = m.all_table()
    return df


if __name__ == '__main__':
    # for logg in range(2, 6):
    #     df = get_abundance(logg)
    df = get_abundance()
    print(df.head())
