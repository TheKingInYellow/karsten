#! /usr/env/python2.7

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as tic
import matplotlib.tri as Tri
import seaborn as sns
import sys

def createColorMap(var, lon, lat, trinodes, title='', label='', \
                mesh=True, bounds=[], c='jet', where=111, figsize=(18,10), \
                fontsize='22', hide=False):
    """
    2D colormap plot of a given variable and mesh. Customized to add the plot to an
    existing figure.

    input:
        - var = gridded variable, 1D numpy array (nelem or nnode)
        - lon, lat = array of lon, lat coordinates
        - trinodes = triangulation node indices
        - mesh = boolean, True with mesh, False without mesh
        - bounds = list, constricted region subdomain in form of
            [lon.min, lon.max, lat.min, lat.max]
        - c = 'jet' or 'gist_earth'
        - figsize, fontsize : optional parameters
        - hide: hide long, lat coordinates
    returns:
        - figure for future plotting
    """

    # figure if var has nele or nnode dimensions
    if var.shape[0] == trinodes.shape[0]:
        dim = trinodes.shape[0]
    elif var.shape[0] == lon.shape[0]:
        dim = lon.shape[0]
    else:
        sys.exit('variable has the wrong dimension, shape not equal to grid ' \
                + 'nummber of elements or nodes')

    # bounding box nodes, elements and variables
    if bounds:
        bb = bounds
    else:
        bb = [lon.min(), lon.max(), lat.min(), lat.max()]

    # mesh triangle
    tri = Tri.Triangulation(lon, lat, triangles=trinodes)

    # setting limits and levels of colormap
    cmin = var[:].min()
    cmax = var[:].max()
    step = (cmax-cmin) / 50.0

    # depth contours to plot
    levels = np.arange(cmin, (cmax+step), step)

    # define figure window
    fig = plt.figure(figsize=figsize)
    plt.rc('font', size=fontsize)
    ax = fig.add_subplot(where, aspect=(1.0/np.cos(np.mean(lat) * np.pi/180.0)))

    if c == 'jet':
        cmap = plt.cm.jet
    elif c == 'earth':
        cmap = plt.cm.gist_earth

    f = ax.tripcolor(tri, var[:], vmax=cmax, vmin=cmin, cmap=cmap)

    if mesh:
        plt.triplot(tri, color='white', linewidth=0.5)

    # label and axis parameters
    if hide:
        ax.set_xlabel('x')
        ax.set_ylabel('y')
    else:
        ax.set_xlabel('Longitude')
        ax.set_ylabel('Latitude')
    ax.patch.set_facecolor('0.5')
    cbar = fig.colorbar(f, ax=ax)
    cbar.set_label(label, rotation=-90, labelpad=30)
    scale = 1

    # ticker for coordinate degree axis
    if hide:
        ax.set_yticklabels([])
        ax.set_xticklabels([])
    else:
        ticks = tic.FuncFormatter(lambda lon, pos: '{0:g}'.format(lon/scale))
        ax.xaxis.set_major_formatter(ticks)
        ax.yaxis.set_major_formatter(ticks)

    # set axis limits based on bounds
    ax.set_xlim([bb[0], bb[1]])
    ax.set_ylim([bb[2], bb[3]])
    ax.grid()
    plt.title(title)

    plt.hold('on')

    return fig

