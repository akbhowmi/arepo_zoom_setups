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


#FOLDERNAME='L%dn%d_%s'%(BOXSIZE_IN_MPC,N,TYPE)

#print('Copying MUSIC files')
#source = "./setup_prototypes/MUSIC"
#destination = path_to_generated_files+FOLDERNAME+'/MUSIC'

# Copy the content of
# source to destination
#shutil.copytree(source, destination)







if not os.path.exists(path_to_generated_files+FOLDERNAME):
        print("Making new directory")
        os.makedirs(path_to_generated_files+FOLDERNAME)
        
#if not os.path.exists(path_to_generated_files+FOLDERNAME+'/'+'MUSIC'):
        print("Making new directory")
        print('Copying MUSIC files')
        source = "./setup_prototypes/MUSIC"
        destination = path_to_generated_files+FOLDERNAME+'/MUSIC'
        shutil.copytree(source, destination)
        #os.makedirs(path_to_generated_files+FOLDERNAME+'/'+'MUSIC')

if not os.path.exists(path_to_generated_files+FOLDERNAME+'/'+'DIAGNOSTICS'):
        print("Making new directory")
        print('Copying diagnosic files')
        destination = path_to_generated_files+FOLDERNAME+'/DIAGNOSTICS/'
        os.makedirs(destination)
        shutil.copy('./distribution_of_particles_and_volume_selection.png', destination)
        shutil.copy('./halo_image.png', destination)
        shutil.copy('./halo_particles_close_to_initial_condition.png', destination)
        shutil.copy('./Volume_parameters_for_MUSIC.npy', destination)
shutil.copy('./zoom_parameters.txt', destination)
        #os.makedirs(path_to_generated_files+FOLDERNAME+'/'+'MUSIC')        





#if not os.path.exists(path_to_generated_files+FOLDERNAME+'/'+'AREPO'):
#        print("Making new directory")
#        os.makedirs(path_to_generated_files+FOLDERNAME+'/'+'AREPO')
        
zoom_centers,zoom_extent=numpy.load('../preparing_files_for_zoom_simulations/Volume_parameters_for_MUSIC.npy')
        
#-------------------------------------------------------------------------------------------------------------------------------------
variables_to_be_edited_in_MUSIC=numpy.array(['zstart',
                                             'levelmin',
                                             'levelmin_TF',
                                             'levelmax',
                                             'Omega_m',
                                             'Omega_L',
                                             'Omega_b',
                                             'H0',
                                             'sigma_8',
                                             'filename',
                                             'boxlength',
                                             'ref_center',
                                             'ref_extent'])
parameter_values_in_MUSIC=numpy.array([
    '%d'%zstart,
    '%d'%levelmin,
    '%d'%(levelmin+1),
    '%d'%levelmax,
    '%.4f'%om_m,
    '%.4f'%om_l,
    '%.6f'%om_b,
    '%.3f'%H0,
    '%.6f'%sigma_8,
    MUSIC_OUTPUT_FILENAME,
    '%d'%BOXSIZE_IN_MPC,
    '%.3f,%.3f,%.3f'%(zoom_centers[0],zoom_centers[1],zoom_centers[2]),
    '%.3f,%.3f,%.3f'%(zoom_extent[0],zoom_extent[1],zoom_extent[2]) 
     ])


if(len(variables_to_be_edited_in_MUSIC)!=len(parameter_values_in_MUSIC)):
    print("ERROR: must have equal number of parameters and their values")
    exit

split_character='='
file_parsing_tools.generate_file(prototypefilepath_MUSIC,path_to_generated_files,FOLDERNAME,generated_MUSIC_config_filename,variables_to_be_edited_in_MUSIC,parameter_values_in_MUSIC,split_character)



