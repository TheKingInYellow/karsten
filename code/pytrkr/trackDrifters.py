#! /usr/env/python2.7

"""
Creates plots and computes stats for pyticle tracker output.

usage: python trackDrifters.py [-p -a -s -w] -r N -n N

cmd line args:
    -p :: plot
    -a :: compute stats
    -s :: save plots
    -v :: add verbosity
    -o :: overwrite current model and plots
    -b :: select a bottom friction
    -l :: select a location
    -d :: select a simulation file date
    -n :: number of particles (int)
    -r :: radius of initialisation (float)
    -w :: add diffusion in calculations from wiener process
    -f :: diffusion fudge factor
    -t :: change the starting time step
    -e :: define existing pyticle file, default None
"""


# lib imports
from __future__ import division
from pyticle_tracker import pyticle
import sys, os
import os.path as osp
import scipy as sp
import numpy as np
import time
import scipy.io as sio
import netCDF4 as nc
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as tic
import matplotlib.tri as Tri
from matplotlib import rc
from datetime import datetime, timedelta
from pyseidon import *
import argparse as arp
from sklearn.preprocessing import normalize
import pandas as pd
import pylab

# local imports
from createColorMap import createColorMap
from drifterUtils import *
from drifterPlotUtils import plotTimeSeries
from plotParticles import *

LOC = ['DG', 'GP', 'PP']
BFRIC = '0.015'
SIM = ['2014_Aug_12_3D', '2013_Aug_08_3D', '2013_Aug_01_3D', '2012_Jun_05_3D', \
       '2012_Jul_05_3D', '2013_Oct_10_3D', '2013_Nov_05_3D', '2013_Nov_06_3D',
       '2013_Aug_02_3D']

PATH2PLOT = '/EcoII/acadia_uni/projects/drifters/plots/pytrkr/'
PATH2SIM = '/EcoII/acadia_uni/workspace/simulated/FVCOM/dngridCSR/' + \
                        'drifter_runs/BFRIC_'
PATH2OUT = '/EcoII/acadia_uni/projects/drifters/pyticle_tracker/'
PATH2INIT = '/array/home/119865c/karsten/drifters/start_info/'
PATH2OBS = '/EcoII/acadia_uni/workspace/observed/'


def parseArgs():
    """
    Parses command line args.
    """

    parser = arp.ArgumentParser(prog='trackDrifters.py')

    parser.add_argument('-p', nargs='*', metavar='#', choices=[1,2,3], \
            default=0, type=int, help='generate plots.\n\t1 :: basic trajectory' \
            + '\n\t2 :: mean lon/lat error' + '\n\t3 :: log-probability density' \
            + '\n\t4 :: pyticle dispersion' + '\n\t5 :: individual error boxplots')
    parser.add_argument('-s', action='store_true', help='save plots.')
    parser.add_argument('-a', action='store_true', help='run analysis.')
    parser.add_argument('-o', action='store_true', help='overwrite data.')
    parser.add_argument('-v', action='store_true', help='verbose output.')
    parser.add_argument('-b', nargs=1, choices=('0.009','0.012','0.015'), \
            help='select a bottom friction.', default='0.015', type=str)
    parser.add_argument('-l', nargs='*', choices=LOC, \
            help='select a location tag.')
    parser.add_argument('-d', nargs='*', choices=SIM,\
            metavar='YYYY_Mmm_DD_3D', help='select a simulation date.')
    multiple = parser.add_argument_group('pyticle options')
    multiple.add_argument('-w', nargs=1, metavar='#', type=float, \
            help='add diffusion from wiener process. requires a seed')
    multiple.add_argument('-f', nargs=1, help='diffusion fudge factor', \
            metavar='ff', type=float, default=1)
    multiple.add_argument('-t', action='store_true', \
            help='alter the initial timestep.')
    multiple.add_argument('-r', nargs=1, type=float, metavar='#', \
            help='define an initial radius in degrees.')
    multiple.add_argument('-n', type=int, metavar='#', nargs=1, \
            help='define a number of particles.')
    parser.add_argument('-e', nargs=1, type=str, metavar='ncfile', \
            help='use existing particle output.', default=None)
    # parser.add_argument('-sd', nargs=1, metavar='#', type=float,\
    #         help='adds random noise as std. dev. to pyticle velocities.')
    parser._optionals.title = 'optional flag arguments'

    args = parser.parse_args()

    return args


def analyseTracks(pytkl, drift, ncfile, sim, loc, row, args):
    """
    Runs a bunch of statistics on the two tracks.
    """
    pass


if __name__ == '__main__':

    # set cmd line options
    print 'parsing command line options...'
    args = parseArgs()

    if args.l:
        LOC = args.l
    if args.d:
        SIM = args.d

    if args.b:
        bfric = args.b
    else:
        bfric = BFRIC

    for loc in LOC:
        for sim in SIM:

            filename = PATH2SIM + bfric + '/' + loc + '/' + sim + \
                        '/output/subdomain_' + loc + '1_0001.nc'
            start_info = PATH2INIT + 'pyticle_info_' + loc + '_' + sim + '.txt'
            path2drift = PATH2OBS + loc + '/Drifter/'
            outpath = PATH2OUT

            if args.v:
                print 'looking for ncfile...'
            if not osp.exists(filename):
                continue

            # define output path
            if args.n:
                outpath += 'n{}'.format(args.n[0])
            if args.r:
                outpath += '_r{}'.format(args.r[0])
            if args.t:
                outpath += '_t'
            if args.w:
                outpath += '_w{}'.format(args.w[0])
                if args.f[0] != 1:
                    outpath += '_ff{}'.format(args.f[0])

            if outpath != '/':
                outpath += '/'

            outpath += loc + '_' + sim
            if args.n:
                outpath += '_n{}'.format(args.n[0])
            if args.r:
                outpath += '_r{}'.format(args.r[0])
            if args.t:
                outpath += '_t'
            if args.w:
                outpath += '_w{}'.format(args.w[0])
                if args.f[0] != 1:
                    outpath += '_f{}'.format(args.f[0])

            outpath += '/'

            if not osp.exists(outpath):
                os.makedirs(outpath)

            # get starting locations and timesteps of drifters
            indata = np.genfromtxt(start_info, dtype=None)
            if args.v:
                print str(indata.shape[0]) + ' drifters...'

            # set centre of location
            if loc == 'GP':
                centre = [-66.33906, 44.26898]
            elif loc == 'DG':
                centre = [-65.76000, 44.67751]
            elif loc == 'PP':
                centre = [-65.206924, 44.389368]
            else:
                sys.exit('location tag not recognized.')

            if not osp.exists(filename) or not osp.isfile(filename):
                sys.exit('simulation path not found / valid.')

            # open the FVCOM file
            if args.v:
                print 'opening fvcom file...'
            ncfile = FVCOM(filename, debug=False)
            if args.v:
                print 'calculating model velocity norm...'
            ncfile.Util3D.velo_norm()

            # set seaborn sns font
            sns.set(font="serif")
            # activate latex text rendering
            # rc('text', usetex=True)

            if bfric not in ['0.015', '0.012', '0.009']:
                sys.exit('bottom friction tag not valid.')

            for row in indata:
                drifter = path2drift + row[0]
                inloc = [row[1], row[2]]
                inlocs = inloc
                savedir = outpath + row[0][:-4] + '_output.nc'

                # added radius and number of particles
                if args.n:
                    num = args.n[0]
                    inlocs = np.tile(inloc, (num, 1))
                    if args.v:
                        print 'starting with {} particles...'.format(num)
                else:
                    num = 1

                if args.r:
                    # 1 deg lat = 111117 m
                    # 1 deg lon =  79868 m
                    inlocs = np.vstack((np.random.uniform( \
                            inloc[0]-args.r[0]/79868.0, \
                            inloc[0]+args.r[0]/79868.0, num), \
                            np.random.uniform(inloc[1]-args.r[0]/111117.0, \
                                              inloc[1]+args.r[0]/111117.0, \
                                              num))).T

                    if args.v:
                        print 'randomizing starting locations...'

                if args.t:
                    if args.v:
                        print 'randomizing starting times...'
                    intime = row[3] + np.random.choice([-1,1])
                else:
                    intime = row[3]

                # if the run exists skip it
                if not osp.exists(savedir):
                    # set options of drifters
                    # note: interpolation ratio is how many timesteps per
                    # model timestep to linearly interpolate nc data
                    # output ratio is how often to output particle potision
                    options={}
                    options['starttime']=intime
                    options['endtime']=row[4]
                    options['interpolationratio']=60
                    options['outputratio']=2
                    options['ncformat']='NETCDF4_CLASSIC'
                    options['useLL']=True
                    options['layer']=0
                    options['gridDim']='2D'
                    if args.w:
                        options['diffusion']=True
                        options['seed']=args.w[0]
                        options['ff']=args.f[0]

                    options['projstr']='lcc +lon_0=-64.55880 +lat_0=41.78504 '+ \
                                   '+lat_1=39.69152 +lat_2=43.87856'

                    # run mitchell's particle tracker
                    if args.v:
                        print 'tracking pyticles...'
                    start = time.clock()
                    mypy=pyticle(filename, inlocs, savedir, options=options)
                    mypy.run()
                    print('run in: %f' % (time.clock() - start))

                # open pytkl structure
                if args.v:
                    print 'opening pytkl file...'
                pytkl = nc.Dataset(savedir, 'r', format='NETCDF4_CLASSIC')

                if args.v:
                    print 'creating time window...'
                # this is in julian time
                tModel = ncfile.Variables.julianTime
                tPytkl = pytkl.variables['time'][:]

                win1 = (np.abs(tModel - tPytkl.min())).argmin()
                win2 = (np.abs(tModel - tPytkl.max())).argmin()

                # calculate time norm
                if win1 == win2:
                    tideNorm = np.mean(ncfile.Variables.velo_norm[win1,:,:], 0)
                else:
                    tideNorm = np.mean(ncfile.Variables.velo_norm[win1:win2,:,:],0)
                if args.v:
                    print 'opening drifter file...'
                drift = Drifter(path2drift + row[0], debug=False)

                # do things based on command line args
                if 0 not in args.p:
                    save = PATH2PLOT
                    if args.n:
                        save += 'n{}'.format(args.n[0])
                    if args.r:
                        save += '_r{}'.format(args.r[0])
                    if args.t:
                        save += '_t'
                    if args.w:
                        save += '_w{}'.format(args.w[0])
                        if args.f[0] != 1:
                            save += '_ff{}'.format(args.f[0])

                    if save[-1] != '/':
                        save += '/'

                    save = save + loc + '_' + sim
                    if args.n:
                        save += '_n{}'.format(args.n[0])
                    if args.r:
                        save += '_r{}'.format(args.r[0])
                    if args.t:
                        save += '_t'
                    if args.w:
                        save += '_w{}'.format(args.w[0])
                        if args.f[0] != 1:
                            save += '_ff{}'.format(args.f[0])

                    save += '/'

                    if 1 in args.p:
                        plotTracks(pytkl, drift, ncfile, row[0][:-4], tideNorm, \
                                    sim, loc, save=args.s, write=args.o, \
                                    verbose=args.v, saveplot=save)
                    if 2 in args.p:
                        geographicError(pytkl, drift, ncfile, row[0][:-4], \
                                    sim, loc, save=args.s, write=args.o, \
                                    verbose=args.v, saveplot=save)
                    if 3 in args.p:
                        spatialProbability(pytkl, drift, ncfile, row[0][:-4], \
                                    sim, loc, save=args.s, write=args.o, \
                                    verbose=args.v, saveplot=save)
                   if 4 in args.p:
                        dispersionPlots(pytkl, drift, ncfile, row[0][:-4], \
                                    sim, loc, save=args.s, write=args.o, \
                                    verbose=args.v, saveplot=save)
                   if 5 in args.p:
                        boxplotError(pytkl, drift, ncfile, row[0][:-4], \
                                    sim, loc, save=args.s, write=args.o, \
                                    verbose=args.v, saveplot=save)

                if args.a:
                    analyseTracks(pytkl,drift,ncfile,sim,loc,row,args)

            print '...all done!'
