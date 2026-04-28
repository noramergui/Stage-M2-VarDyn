"""
VarDyn configuration file for the Gulf Stream region in the eNATL60-BLB002 simulation. 
The model is a 1.5 layer quasi-geostrophic model, and the reduced basis is made of empirical modes with a spatially variable time decorrelation scale. 
The observations are nadir along-track SSH observations from 6 different altimetry missions (AL, C2, H2B, J3, S3A and S3B) and SWOT swath SSH observations. 
"""

#################################################################################################################################
# Import libraries     
#################################################################################################################################

from datetime import datetime,timedelta


#################################################################################################################################
# GLOBAL PARAMETERS
#################################################################################################################################

name_experiment = 'VarDyn-QG_eNATL60-BLBT02_Azores_winter_cfl.1'

myPath = '/home/nora/Workdir/VarDyn'

path_data = '/data1/data/models/eNATL60/BLBT02'

path_VarDyn = '/home/nora/VarDyn'

 
#################################################################################################################################
# EXPERIMENTAL PARAMETERS
#################################################################################################################################
EXP = dict(

    name_experiment = name_experiment, # name of the experiment

    saveoutputs = True, # save outputs flag (True or False)

    name_exp_save = name_experiment, # name of output files

    path_save = f'{myPath}/outputs/{name_experiment}', # path of output files

    tmp_DA_path = f"{myPath}/scratch/{name_experiment}", # temporary data assimilation directory path,

    init_date = datetime(2009,12,1,0), # initial date (yyyy,mm,dd,hh) 

    final_date = datetime(2010,2,16,0),  # final date (yyyy,mm,dd,hh) 

    assimilation_time_step = timedelta(hours=6),  

    saveoutput_time_step = timedelta(hours=6),  # time step at which the states are saved 

    flag_plot = 0, # Set to 1 if you want intermediate plots for debugging

)
    
#################################################################################################################################
# GRID parameters
#################################################################################################################################
NAME_GRID = 'myGRID'

myGRID = dict(

    super = 'GRID_CAR',

    lon_min = -33,                                        # domain min longitude

    lon_max = -23,                                        # domain max longitude

    lat_min = 28,                                         # domain min latitude

    lat_max = 38,                                         # domain max latitude

    dx = 10,                                              # grid spacing in km

    dy = 10,                                              # grid spacing in km

    name_init_mask = f'{path_data}/coarsened/eNATL60-BLBT02_coarse-5_rolling-240.nc',

    name_var_mask = {'lon':'lon','lat':'lat','var':'ssh'}

)

#################################################################################################################################
# Model parameters
#################################################################################################################################
NAME_MOD = 'myMOD'

myMOD = dict(

    super = 'MOD_QG1L_JAX',

    name_class = 'Qgm',

    name_var = {'SSH':'ssh'},

    save_diagnosed_variables = False, # Save diagnosed variables in the model output

    dtmodel = 1800, # model timestep

    time_scheme = 'rk2',

    init_from_bc = True,

    filec_aux = f'{path_VarDyn}/mapping/aux/aux_first_baroclinic_speed.nc',

    name_var_c = {'lon':'lon','lat':'lat','var':'c1'},

    cfl = .1,

    Kdiffus = 150,
    
)

#################################################################################################################################
# BOUNDARY CONDITIONS
#################################################################################################################################
NAME_BC = 'myBC' # For now, only BC_EXT is available

myBC = dict(

    super = 'BC_EXT',

    file = f'{path_data}/coarsened/eNATL60-BLBT02_coarse-5_rolling-240.nc', # netcdf file(s) in whihch the boundary conditions fields are stored

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

    Npix = 4, # Number of pixels to perform projection y=Hx

    mask_coast = False,

    mask_borders = False,

)

#################################################################################################################################
# Reduced basis parameters
#################################################################################################################################
NAME_BASIS =  'myBASIS'

myBASIS = dict(

    super = 'BASIS_BMaux_JAX',

    name_mod_var = 'ssh', # Name of the related model variable 

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

    maxiter = 500, # Maximal number of iterations for the minimization process (typically 500)

    save_minimization = True, # save cost function and its gradient at each iteration 

    ftol = 1e-5, 

    path_save_control_vectors = f'{myPath}/controls/{name_experiment}',

    timestep_checkpoint = timedelta(hours=6), #  timesteps separating two consecutive analysis 

    restart_4Dvar = False,

    freq_it_plot = 10, # Frequency of iteration to plot the cost function and its gradient  
 
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

    path = f'{path_data}/obs/swot/*.nc',

    name_time = 'time',
    
    name_lon = 'longitude',

    name_lat = 'latitude',

    name_var = {'SSH':'ssh'},

)

#################################################################################################################################
# Diagnostics
#################################################################################################################################
NAME_DIAG = 'myDIAG'

myDIAG = dict(

    super = 'DIAG_OSSE',

    dir_output = f'{myPath}/diags/{name_experiment}',

    name_ref = f'{path_data}/bm/eNATL60-BLBT02_ssh.nc',

    name_ref_time = 'time',

    name_ref_lon = 'lon',

    name_ref_lat = 'lat',

    name_ref_var = 'ssh',

    name_exp_var = 'ssh',

    path_images2mp4 = '/data1/packages/climporn/ffmpeg/images2mp4.sh',

    compare_to_baseline = False,

    name_bas = f'{myPath}/outputs//*.nc',

    name_bas_time = 'time',

    name_bas_lon = 'lon',

    name_bas_lat = 'lat',

    name_bas_var = 'ssh'

)