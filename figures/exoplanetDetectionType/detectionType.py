from __future__ import division
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from PyAstronomy import pyasl
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
plt.rcParams['axes.spines.right'] = False
plt.rcParams['axes.spines.top'] = False
plt.rcParams['axes.linewidth'] = 2
plt.rcParams['xtick.major.width'] = 2
plt.rcParams['ytick.major.width'] = 2


def imscatter(x, y, image, ax=None, zoom=1):
    if ax is None:
        ax = plt.gca()
    try:
        image = plt.imread(image)
    except TypeError:
        # Likely already an array...
        pass
    im = OffsetImage(image, zoom=zoom)
    x, y = np.atleast_1d(x, y)
    artists = []
    for x0, y0 in zip(x, y):
        ab = AnnotationBbox(im, (x0, y0), xycoords='data', frameon=False)
        artists.append(ax.add_artist(ab))
    ax.update_datalim(np.column_stack([x, y]))
    return artists


if __name__ == '__main__':
    df = pyasl.ExoplanetEU2(skipUpdate=True).getAllDataPandas()
    detectionTypes = {
        'Transit': ['Primary Transit', 2],
        'RV': ['Radial Velocity', 2],
        'Imaging': ['Imaging', 5],
        'Astrometry': ['Astrometry', 20],
        'TTV': ['TTV', 10],
        'Microlensing': ['Microlensing', 5]}
    planets = {
        'mercury': [0.390, 0.00017, 0.02],
        # 'venus':   [0.723, 0.00256, 0.02],
        'earth':   [1.000, 0.00315, 0.04],
        # 'mars':    [1.524, 0.00034, 0.01],
        'jupiter': [5.203, 1.00000, 0.03]}

    x, y = 'semi_major_axis', 'mass'
    for detectionType, (real, ms) in detectionTypes.iteritems():
        idx = df['detection_type'] == real
        plt.loglog(df[idx][x], df[idx][y], '.', label=detectionType, ms=ms)
    plt.legend(loc='best', frameon=False)
    plt.xlabel('Semi major axis [AU]')
    plt.ylabel(r'Exoplanet mass [M$_\mathrm{Jup}$]')
    x1, x2 = plt.xlim()

    ax = plt.gca()
    for planet in planets.iterkeys():
        image_path = ('../HZ/{}.png'.format(planet))
        x = planets[planet][0]
        y = planets[planet][1]
        zoom = planets[planet][2]
        imscatter(x, y, image_path, zoom=zoom, ax=ax)
        plt.hlines(y, x1, x, linestyle='--', alpha=0.6)

    # plt.savefig('../exoplanetDetectionType.pdf')
    plt.show()
