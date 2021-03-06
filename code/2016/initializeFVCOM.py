#from pyseidon import *
#from pyseidon_dvt import *
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime, timedelta
import netCDF4 as nc

# local imports - might interfere if using a different pyseidon
from drifterPlotUtils import *
from drifterAnalysisUtils import *
from drifterUtils import *
from plotParticles import *
from createColorMap import createColorMap

# load pyseidon
from pyseidon_dvt import *
from interpolation_utils import *

LOC = ['GP', 'GP', 'GP']
DATE = ['2013_Aug_08_3D', '2013_Aug_01_3D', '2013_Aug_02_3D']
BF = ['0.015', '0.015', '0.015']
run_str = 'n10000_r50.0_g'
OBS = ["GP_F_20130808_H_002", \
       "GP_F_20130801_78_1_007_SE15",  \
       "GP_E_20130802_78_1_002"]
bounds_MP = [-64.44, -64.36, 45.32, 45.34]
AX=[]

#PATH2OBS="/EcoII/Luna/Drifter_data/MinasPassage/MP_BMP_20170106_processed.mat"
PATH2OBS="/array/home/119865c/workspace/MP_BMP_20170106.mat"
#PATH2SIM="/EcoII/Luna/FVCOM_data/acadia_bof_v2/3d/2017-01-06_2017-01-07/" +\
#         "output/acadia_bof_v2_3d_0001.nc"
PATH2SIM="/array/home/119865c/workspace/acadia_bof_v2_3d_20170106.nc"
#PATH2SIM="/EcoII/acadia_uni/workspace/simulated/FVCOM/dngridCSR/" \
#        + "drifter_runs/BFRIC_" + BF[0] + "/" + LOC[0] + "/" + DATE[0] + \
#        "/output/" + "subdomain_" + LOC[0] + "1_0001.nc"
#PATH2SIM2='/EcoII/acadia_uni/workspace/simulated/FVCOM/dngridCSR/' \
#        + 'drifter_runs/BFRIC_' + BF[1] + '/' + LOC[1] + "/" + DATE[1] + \
#        '/output/' + 'subdomain_' + LOC[1] + '1_0001.nc'
#PATH2SIM3='/EcoII/acadia_uni/workspace/simulated/FVCOM/dngridCSR/' \
#        + 'drifter_runs/BFRIC_' + BF[2] + '/' + LOC[2] + "/" + DATE[2] + \
#        '/output/' + 'subdomain_' + LOC[2] + '1_0001.nc'
#
#PATH2OBS="/EcoII/acadia_uni/workspace/observed/" + LOC[0] + "/Drifter/" \
#        + OBS[0] + ".mat"
#PATH2OBS2="/EcoII/acadia_uni/workspace/observed/" + LOC[1] + "/Drifter/" \
#        + OBS[1] + ".mat"
#PATH2OBS3="/EcoII/acadia_uni/workspace/observed/" + LOC[2] + "/Drifter/" \
#        + OBS[2] + ".mat"
#
#PATH2PY = '/EcoII/acadia_uni/projects/drifters/pyticle_tracker/' + run_str + \
#          '/' + LOC[0] + '_' + DATE[0] + '_' + run_str + '/' + \
#          OBS[0] + "_output.nc"
#PATH2PY2 = '/EcoII/acadia_uni/projects/drifters/pyticle_tracker/' + run_str + \
#          '/' + LOC[1] + '_' + DATE[1] + '_' + run_str + '/' + \
#          OBS[1] + "_output.nc"
#PATH2PY3 = '/EcoII/acadia_uni/projects/drifters/pyticle_tracker/' + run_str + \
#          '/' + LOC[2] + '_' + DATE[2] + '_' + run_str + '/' + \
#          OBS[2] + "_output.nc"


if __name__ == '__main__':
    """
    The program initializes the FVCOM, Drifter, and Validation classes for the
    given FVCOM grid models and drifter file(s).
    """

    model = FVCOM(PATH2SIM, ax=AX, debug=False)
    # model2= FVCOM(PATH2SIM2, debug=False)
    # model3= FVCOM(PATH2SIM3, debug=False)

    drift = Drifter(PATH2OBS, debug=False)
    # drift2= Drifter(PATH2OBS2, debug=False)
    # drift3= Drifter(PATH2OBS3, debug=False)
    # adcp = ADCP(PATH_TO_ADCP, debug=True)

    # pytkl = nc.Dataset(PATH2PY, 'r', type='NETCDF4_CLASSIC')
    # pytkl2 = nc.Dataset(PATH2PY2, 'r', type='NETCDF4_CLASSIC')
    # pytkl3 = nc.Dataset(PATH2PY3, 'r', type='NETCDF4_CLASSIC')

    # create validation objects
   #  valid = Validation(drift, model, flow='sf', debug=True)
    # valid2 = Validation(drift2, model2, flow='sf', debug=True)
    # valid3 = Validation(drift3, model3, flow='sf', debug=True)

