#! /usr/env/python2.7

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as tic
import matplotlib.tri as Tri
import seaborn as sns
import sys

def createColorMap(model, var, title='', label='', mesh=True, bounds=[], \
                    debug=True, c='jet'):
    """
    2D colormap plot of a given variable and mesh. This function is adapted from
    PySeidon's colormap_var, except it is customized to add the plot to an
    existing figure. Holds the plot.

    input:
        - var = gridded variable, 1D numpy array (nele or nnode)
        - title = plot title, string
        - mesh = boolean, True with mesh, False without mesh
        - bounds = list, constricted region subdomain in form of
            [lon.min, lon.max, lat.min, lat.max]
        - color = 'jet' or 'gist_earth'
    returns:
        - figure for future plotting
    """

    if debug:
        print '\tplotting grid...'
    # figure if var has nele or nnode dimensions
    if var.shape[0] == model.Grid.nele:
        dim = model.Grid.nele
    elif var.shape[0] == model.Grid.nnode:
        dim = model.Grid.nnode
    else:
        sys.exit('variable has the wrong dimension, shape not equal to grid ' \
                + 'nummber of elements or nodes')

    # bounding box nodes, elements and variables
    lon = model.Grid.lon[:]
    lat = model.Grid.lat[:]
    if debug:
        print '\tcomputing bounding box...'
    if bounds:
        bb = bounds
    else:
        bb = [lon.min(), lon.max(), lat.min(), lat.max()]

    if not hasattr(model.Grid, 'triangleLL'):
        # mesh triangle
        if debug:
            print '\tcomputing triangulation...'
        trinodes = model.Grid.trinodes[:]
        tri = Tri.Triangulation(lon, lat, triangles=trinodes)
    else:
        tri = model.Grid.triangleLL

    # setting limits and levels of colormap
    if debug:
        print '\tcomputing cmin...'
    cmin = var[:].min()
    if debug:
        print '\tcomputing cmax...'
    cmax = var[:].max()
    step = (cmax-cmin) / 50.0

    # depth contours to plot
    levels = np.arange(cmin, (cmax+step), step)

    # define figure window
    if debug:
        print '\tcreating subplot...'

    fig = plt.figure(figsize=(18,10))
    plt.rc('font', size='22')
    ax = fig.add_subplot(111, aspect=(1.0/np.cos(np.mean(lat) * np.pi/180.0)))

    if debug:
        print '\tcomputing colormap...'
    if c == 'jet':
        cmap = plt.cm.jet
    elif c == 'earth':
        cmap = plt.cm.gist_earth

    f = ax.tripcolor(tri, var[:], vmax=cmax, vmin=cmin, cmap=cmap)

    if mesh:
        plt.triplot(tri, color='white', linewidth=0.5)

    # label and axis parameters
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    ax.patch.set_facecolor('0.5')
    cbar = fig.colorbar(f, ax=ax)
    cbar.set_label(label, rotation=-90, labelpad=30)
    scale = 1

    # ticker for coordinate degree axis
    if debug:
        print '\tconfiguring axis...'
    ticks = tic.FuncFormatter(lambda lon, pos: '{0:g}'.format(lon/scale))
    ax.xaxis.set_major_formatter(ticks)
    ax.yaxis.set_major_formatter(ticks)
    ax.set_xlim([bb[0], bb[1]])
    ax.set_ylim([bb[2], bb[3]])
    ax.grid()
    plt.title(title)

    plt.hold('on')

    if debug:
        print '...colormap passed.'

    return fig

