from pyseidon import *
from interpolation_utils import *
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta

# ----------Grand Passage:
# PATH_TO_SIM_FILE="/EcoII/acadia_uni/workspace/simulated/FVCOM/dngridCSR/drifter_runs/GP/2013_Aug_01_3D/output/subdomain_GP1_0001.nc"
# PATH_TO_OBS_FILE="/EcoII/acadia_uni/workspace/observed/GP/Drifter/GP_F_20130801_78_2_001_SE15.mat"
# PATH_TO_ADCP='/EcoII/acadia_uni/workspace/observed/GP/ADCP/Flow_GP-130730-TA_avg15.mat'

# ----------Digby Gut:

LOC = ['GP', 'DG', 'PP']
DATE = ['2013_Aug_08_3D', '2013_Nov_06_3D', '2014_Aug_12_3D']
BF = ['0.015', '0.015', '0.015']


PATH2SIM="/EcoII/acadia_uni/workspace/simulated/FVCOM/dngridCSR/" \
        + "drifter_runs/BFRIC_" + BF[0] + "/" + LOC[0] + "/" + DATE[0] + \
        "/output/" + "subdomain_" + LOC[0] + "1_0001.nc"
PATH2SIM2='/EcoII/acadia_uni/workspace/simulated/FVCOM/dngridCSR/' \
        + 'drifter_runs/BFRIC_' + BF[1] + '/' + LOC[1] + "/" + DATE[1] + \
        '/output/' + 'subdomain_' + LOC[1] + '1_0001.nc'
PATH2SIM3='/EcoII/acadia_uni/workspace/simulated/FVCOM/dngridCSR/' \
        + 'drifter_runs/BFRIC_' + BF[2] + '/' + LOC[2] + "/" + DATE[2] + \
        '/output/' + 'subdomain_' + LOC[2] + '1_0001.nc'

PATH2OBS="/EcoII/acadia_uni/workspace/observed/" + LOC[0] + "/Drifter/" \
        + "GP_F_20130808_78_1_001.mat"
PATH2OBS2="/EcoII/acadia_uni/workspace/observed/" + LOC[1] + "/Drifter/" \
        + "DG_F_20131106_78_1_001_SW10.mat"
PATH2OBS3="/EcoII/acadia_uni/workspace/observed/" + LOC[2] + "/Drifter/" \
        + "PP_F_20140812_78_K_005_N02.mat"

if __name__ == '__main__':
    """
    The program initializes the FVCOM, Drifter, and Validation classes for the
    given FVCOM grid models and drifter file(s).
    """

    model = FVCOM(PATH2SIM, debug=True)
    model2= FVCOM(PATH2SIM2, debug=True)
    model3= FVCOM(PATH2SIM3, debug=True)

    drift = Drifter(PATH2OBS, debug=True)
    drift2= Drifter(PATH2OBS2, debug=True)
    drift3= Drifter(PATH2OBS3, debug=True)
    # adcp = ADCP(PATH_TO_ADCP, debug=True)

    # create validation objects
    valid = Validation(drift, model, flow='sf', debug=True)
    valid2 = Validation(drift2, model2, flow='sf', debug=True)
    valid3 = Validation(drift3, model3, flow='sf', debug=True)

