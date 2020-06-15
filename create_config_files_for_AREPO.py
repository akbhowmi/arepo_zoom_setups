import sys
sys.path.append('/home/aklantbhowmick/anaconda3/lib/python3.7/site-packages')
sys.path.append('/home/aklantbhowmick/anaconda3/lib/python3.7/site-packages/scalpy/')
sys.path.append('/home/aklantbhowmick/anaconda3/envs/nbodykit-env/lib/python3.6/site-packages/')
import arepo_package
import scipy.interpolate
import h5py
import os
import numpy
import file_parsing_tools
import shutil
#%pylab inline
#path_to_parameter_file='zoom_parameters.txt'
path_to_parameter_file='../preparing_files_for_zoom_simulations/zoom_parameters.txt'
fp=open(path_to_parameter_file)
line=1
while line:
    line = fp.readline()
    exec(line)

#----------------------------------Creating the desired output_list file------------------------------
z_range=numpy.linspace(z_earliest_snapshot_output,z_latest_snapshot_output,no_of_snapshots)
f=open('./setup_prototypes/AREPO/output_list_for_zoom.txt','w')
for z in z_range:
    scale=1./(1.+z)
    f.write("%.10f          1\n"%scale)
f.close()
#-----------------------------------------------------------------------------------------------------




#FOLDERNAME='L%dn%d_%s'%(BOXSIZE_IN_MPC,N,TYPE)
if not os.path.exists(path_to_generated_files+FOLDERNAME):
        print("Making new directory")
        os.makedirs(path_to_generated_files+FOLDERNAME)
        
#if not os.path.exists(path_to_generated_files+FOLDERNAME+'/'+'MUSIC'):
#        print("Making new directory")
#        os.makedirs(path_to_generated_files+FOLDERNAME+'/'+'MUSIC')
        
if not os.path.exists(path_to_generated_files+FOLDERNAME+'/'+'AREPO'):
#        print("Making new directory")
#        os.makedirs(path_to_generated_files+FOLDERNAME+'/'+'AREPO')
        print('Copying AREPO files')
        source = "./setup_prototypes/AREPO"
        destination = path_to_generated_files+FOLDERNAME+'/AREPO'
        shutil.copytree(source, destination)
        #os.makedirs(path_to_generated_files+FOLDERNAME+'/'+'MUSIC')
        

ic_object=h5py.File(path_to_generated_files+FOLDERNAME+'/MUSIC/IC.hdf5')
header=ic_object['Header'].attrs
PMGRID=header['suggested_pmgrid']
GRIDBOOST=header['suggested_gridboost']
if(GRIDBOOST==0):
    GRIDBOOST=1


zoom_centers,zoom_extent=numpy.load('../preparing_files_for_zoom_simulations/Volume_parameters_for_MUSIC.npy')
        
#--------------------------------------------------------------------------------------------------------------------------------------
variables_to_be_edited_in_AREPO_config=numpy.array([
    'PMGRID',
    'PLACEHIGHRESREGION','GRIDBOOST'])
parameter_values_in_AREPO_config=numpy.array(['%d'%PMGRID,
                                              2,'%d'%GRIDBOOST])
if(len(variables_to_be_edited_in_AREPO_config)!=len(parameter_values_in_AREPO_config)):
    print("ERROR: must have equal number of parameters and their values")
    exit

split_character='='

file_parsing_tools.generate_file(prototypefilepath_AREPO_config,path_to_generated_files,FOLDERNAME,generated_AREPO_config_filename,variables_to_be_edited_in_AREPO_config,parameter_values_in_AREPO_config,split_character)

#----------------------------------------------------------------------------------------------------------------------------------------------

variables_to_be_edited=numpy.array(['SnapshotFileBase',
                                    'TimeBegin',
                                    'Omega0',
                                    'OmegaLambda',
                                    'OmegaBaryon',
                                    'HubbleParam',
                                    'BoxSize',
                                    'InitCondFile',
                                    'SeedBlackHoleMass',
                                    'MinFoFMassForNewSeed',
                                    'MinMetallicityForNewSeed',
                                    'MaxMetallicityForNewSeed']) 
parameter_values=numpy.array(['snap',
                              '%.7f'%(1./(1+zstart)),
                              '%.4f'%om_m,
                              '%.4f'%om_l,
                              '%.6f'%om_b,
                              '%.4f'%(H0/100.),
                              '%d'%(BOXSIZE_IN_MPC*1000),
                              path_to_generated_files+FOLDERNAME+'/MUSIC/IC',
                              '%.15fe%d'%(10**(log_seed_blackhole_mass-int(log_seed_blackhole_mass)),int(log_seed_blackhole_mass)-10),
                              '%.15fe%d'%(10**(log_seed_FOF_min_mass-int(log_seed_FOF_min_mass)),int(log_seed_FOF_min_mass)-10),
                              '%.15fe%d'%(10**(log_min_metallicity_for_seed-int(log_min_metallicity_for_seed)),int(log_min_metallicity_for_seed)),   
                              '%.15fe%d'%(10**(log_max_metallicity_for_seed-int(log_max_metallicity_for_seed)),int(log_max_metallicity_for_seed))])

if(len(variables_to_be_edited)!=len(parameter_values)):
    print("ERROR: must have equal number of parameters and their values")
    exit

split_character=' '
file_parsing_tools.generate_file(prototypefilepath_AREPO_param,path_to_generated_files,FOLDERNAME,generated_AREPO_param_filename,variables_to_be_edited,parameter_values,split_character)
#----------------------------------------------------------------------------------------------------------------------------------------------


