#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  6 19:20:42 2021

@author: leguillou
"""

name_experiment = 'VarDyn-QG_eNATL60-BLB002_GulfStream_multiwindows'

myPath = '/data2/nora/Workdir/VarDyn'

path_data = '/data1/data/models/eNATL60/BLB002'

path_VarDyn = '/home/nora/VarDyn'

compute_obs = False 

#######################################     ##########################################################################################
# Global libraries     
#################################################################################################################################

from datetime import datetime,timedelta
 
#################################################################################################################################
# EXPERIMENTAL PARAMETERS
#################################################################################################################################
EXP = dict(

    name_experiment = name_experiment, # name of the experiment

    saveoutputs = True, # save outputs flag (True or False)

    name_exp_save = name_experiment, # name of output files

    path_save = f'{myPath}/outputs/{name_experiment}', # path of output files

    tmp_DA_path = f"{myPath}/scratch/{name_experiment}", # temporary data assimilation directory path,

    init_date = datetime(2009,7,11,0), # initial date (yyyy,mm,dd,hh) 

    final_date = datetime(2010,2,25,0),  # final date (yyyy,mm,dd,hh) 

    assimilation_time_step = timedelta(hours=6),  

    saveoutput_time_step = timedelta(hours=6),  # time step at which the states are saved 

    flag_plot = 0,

    write_obs = True,

    path_obs = f'{myPath}/obs',

    compute_obs = compute_obs

)
    
#################################################################################################################################
# GRID parameters
#################################################################################################################################
NAME_GRID = 'myGRID'

myGRID = dict(

    super = 'GRID_GEO',

    lon_min = -65,                                        # domain min longitude

    lon_max = -55,                                        # domain max longitude

    lat_min = 33,                                         # domain min latitude

    lat_max = 43,                                         # domain max latitude

    dlon = 1/10,                                              # grid spacinng in km

    dlat = 1/10,                                              # grid spacing in km

    name_init_mask = f'{path_data}/coarsened/eNATL60-BLB002_coarse-5_rolling-20.nc',

    name_var_mask = {'lon':'lon','lat':'lat','var':'ssh'}

)

#################################################################################################################################
# Model parameters
#################################################################################################################################
NAME_MOD = ['myMOD0','myMOD1']

myMOD0 = dict(

    super = 'MOD_DIFF',

    name_var = {'SSH':'ssh_barotrop'},

    #name_init_var = {'SSH':'ssh_barotrop'},

    dtmodel = 1800, # model timestep

    init_from_bc = False,
    
)

myMOD1 = dict(

    super = 'MOD_QG1L_JAX',

    name_class = 'Qgm',#'QgmWithTiles',

    name_var = {'SSH':'ssh'},

    name_init_var = {'SSH':'ssh'},

    save_diagnosed_variables = False, # Save diagnosed variables in the model output

    dtmodel = 1800, # model timestep

    time_scheme = 'rk2',

    init_from_bc = True,

    filec_aux = f'{path_VarDyn}/mapping/aux/aux_first_baroclinic_speed.nc',

    name_var_c = {'lon':'lon','lat':'lat','var':'c1'},

    cmin= 2.,

    cfl = .1,

    Kdiffus = 150,
    
)

#################################################################################################################################
# BOUNDARY CONDITIONS
#################################################################################################################################
NAME_BC = 'myBC' # For now, only BC_EXT is available

myBC = dict(

    super = 'BC_EXT',

    file = f'{path_data}/coarsened/eNATL60-BLB002_coarse-5_rolling-10.nc', # netcdf file(s) in whihch the boundary conditions fields are stored

    name_lon = 'lon',

    name_lat = 'lat',

    name_time = 'time',

    name_var = {'SSH':'ssh'}, # name of the boundary conditions variable

    name_mod_var = {'SSH':'ssh'},

)

#################################################################################################################################
# OBSERVATIONAL OPERATORS
#################################################################################################################################
NAME_OBSOP = 'myOBSOP'

myOBSOP = dict(

    super = 'OBSOP_INTERP_L3_JAX',

    write_op = True,

    path_save = f'{myPath}/H', # Directory where to save observational operator

    compute_op = compute_obs, # Force computing H 

    Npix = 4, # Number of pixels to perform projection y=Hx

    mask_coast = False,

    mask_borders = False,

)

#################################################################################################################################
# Reduced basis parameters
#################################################################################################################################
NAME_BASIS =  ['myBASIS0', 'myBASIS1', 'myBASIS2']

myBASIS0 = dict(

    super = 'BASIS_GAUSS3D_JAX',

    name_mod_var = 'ssh_barotrop', # Name of the related model variable 
    
    flux = True, # Whether making a component signature in space appear/disappear in time. For dynamical mapping, use flux=False

    facns = 3., #factor for wavelet spacing in space

    facnlt = 3., #factor for wavelet spacing in time

    sigma_D = 1000, # Spatial scale (km)

    sigma_T = 3, # Time scale (days)

    sigma_Q = 0.05, 

    normalize_fact = True,

    flag_variable_Q = False,

    path_sad = None,#'/home/flo/MASSH/mapping/aux/std_variable_barotrop_new.nc',

    name_var_sad = None,#{'lon':'lon', 'lat':'lat', 'var':'std_barotrop'}, # Name of longitude,latitude and variable of depth netcdf file

)

myBASIS1 = dict(

    super = 'BASIS_GAUSS3D_JAX',

    name_mod_var = 'ssh', # Name of the related model variable 
    
    flux = True, # Whether making a component signature in space appear/disappear in time. For dynamical mapping, use flux=False

    facns = 3., #factor for wavelet spacing in space

    facnlt = 3., #factor for wavelet spacing in time

    sigma_D = 970, # Spatial scale (km)

    sigma_T = 25, # Time scale (days)

    sigma_Q = 0.03, # Standard deviation for matrix Q 

    normalize_fact = True,
)


myBASIS2 = dict(

    super = 'BASIS_BMaux_JAX',

    name_mod_var = 'ssh', # Name of the related model variable 
    
    wavelet_init = False,
    
    flux = False, # Whether making a component signature in space appear/disappear in time. For dynamical mapping, use flux=False

    facns = 1., #factor for wavelet spacing in space

    facnlt = 2., #factor for wavelet spacing in time

    npsp = 3.5, # Defines the wavelet shape

    facpsp = 1.5, # factor to fix df between wavelets

    file_aux = f'{path_VarDyn}/mapping/aux/aux_reduced_basis_BM.nc', # Name of auxilliary file in which are stored the std and tdec for each locations at different wavelengths.

    lmin = 80, # minimal wavelength (in km)

    lmax = 1000., # maximal wavelength (in km)

    factdec = 7.5, # factor to be multiplied to the computed time of decorrelation 

    tdecmin = 2., # minimum time of decorrelation 

    tdecmax = 20., # maximum time of decorrelation 

    facQ = 1, # factor to be multiplied to the estimated Q

    lc = None,
)


#################################################################################################################################
# Analysis parameters
#################################################################################################################################
NAME_INV = 'myINV'

myINV = dict(

    super = 'INV_4DVAR',

    flag_full_jax = False,

    save_minimization = True, # save cost function and its gradient at each iteration 

    compute_test = False, # TLM, ADJ & GRAD tests

    ftol = 1e-5, # Gradient norm must be less than gtol before successful termination.

    maxiter = 500, # Maximal number of iterations for the minimization process

    opt_method = 'L-BFGS-B', # method for scipy.optimize.minimize

    path_save_control_vectors = f'{myPath}/controls/{name_experiment}',

    timestep_checkpoint = timedelta(hours=6), #  timesteps separating two consecutive analysis 

    prec = True, # preconditoning

    path_init_4Dvar = None,

    restart_4Dvar = False,

    anomaly_from_bc = False,

    sigma_R = None, 

    freq_it_plot = 50, # Frequency of iteration to plot the cost function and its gradient  
 
)

#################################################################################################################################
# Observation parameters
#################################################################################################################################
NAME_OBS = ['AL','C2','H2B','J3','S3A','S3B','S6A']

sigma_noise = 0.1 # Value of (constant) measurement error for all the nadir observations (in m)

AL = dict(

    super = 'OBS_SSH_NADIR',

    path = f'{path_data}/obs/nadirs/al.nc',

    name_time = 'time',
    
    name_lon = 'lon',

    name_lat = 'lat',
    
    name_var = {'SSH':'ssh'},

    sigma_noise = sigma_noise, # Value of (constant) measurement error 

)

C2 = dict(

    super = 'OBS_SSH_NADIR',

    path = f'{path_data}/obs/nadirs/c2.nc',

    name_time = 'time',
    
    name_lon = 'lon',

    name_lat = 'lat',
    
    name_var = {'SSH':'ssh'},

    sigma_noise = sigma_noise, # Value of (constant) measurement error 

)

H2B = dict(

    super = 'OBS_SSH_NADIR',

    path = f'{path_data}/obs/nadirs/h2b.nc',

    name_time = 'time',
    
    name_lon = 'lon',

    name_lat = 'lat',
    
    name_var = {'SSH':'ssh'},

    sigma_noise = sigma_noise, # Value of (constant) measurement error 

)

J3 = dict(

    super = 'OBS_SSH_NADIR',

    path = f'{path_data}/obs/nadirs/j3.nc',

    name_time = 'time',
    
    name_lon = 'lon',

    name_lat = 'lat',
    
    name_var = {'SSH':'ssh'},

    sigma_noise = sigma_noise, # Value of (constant) measurement error 

)

S3A = dict(

    super = 'OBS_SSH_NADIR',

    path = f'{path_data}/obs/nadirs/s3a.nc',

    name_time = 'time',
    
    name_lon = 'lon',

    name_lat = 'lat',
    
    name_var = {'SSH':'ssh'},

    sigma_noise = sigma_noise, # Value of (constant) measurement error 

)

S3B = dict(

    super = 'OBS_SSH_NADIR',

    path = f'{path_data}/obs/nadirs/s3b.nc',

    name_time = 'time',
    
    name_lon = 'lon',

    name_lat = 'lat',
    
    name_var = {'SSH':'ssh'},

    sigma_noise = sigma_noise, # Value of (constant) measurement error 

)

S6A = dict(

    super = 'OBS_SSH_NADIR',

    path = f'{path_data}/obs/nadirs/s6a.nc',

    name_time = 'time',
    
    name_lon = 'lon',

    name_lat = 'lat',
    
    name_var = {'SSH':'ssh'},

    sigma_noise = sigma_noise, # Value of (constant) measurement error 

)


SWOT = dict(

    super = 'OBS_SSH_SWATH',

    path = f'{path_data}/2020a_SSH_mapping_NATL60_karin_swot.nc',

    name_time = 'time',
    
    name_lon = 'lon',

    name_lat = 'lat',
    
    name_xac = 'x_ac',

    name_var = {'SSH':'ssh_model'},

)

#################################################################################################################################
# Diagnostics
#################################################################################################################################
NAME_DIAG = 'myDIAG'

myDIAG = dict(

    super = 'DIAG_OSSE',

    dir_output = f'{myPath}/diags/{name_experiment}',

    name_ref = f'{path_data}/degraded_20/*_SSH.nc',

    name_ref_time = 'time',

    name_ref_lon = 'lon',

    name_ref_lat = 'lat',

    name_ref_var = 'ssh',

    name_exp_var = 'SSH_tot',

    path_images2mp4 = '/data1/packages/climporn/ffmpeg/images2mp4.sh',

    compare_to_baseline = False,

    name_bas = f'{myPath}/outputs/VarDyn-QG_eNATL60-BLB002_GulfStream_float32/*.nc',

    name_bas_time = 'time',

    name_bas_lon = 'lon',

    name_bas_lat = 'lat',

    name_bas_var = 'ssh'

)
