import sys
sys.path.append('/home/aklantbhowmick/anaconda3/lib/python3.7/site-packages')
sys.path.append('/home/aklantbhowmick/anaconda3/lib/python3.7/site-packages/scalpy/')
sys.path.append('/home/aklantbhowmick/anaconda3/envs/nbodykit-env/lib/python3.6/site-packages/')
import arepo_package
import scipy.interpolate
import h5py
import os
import numpy
#%pylab inline
#path_to_parameter_file='zoom_parameters.txt'
path_to_parameter_file='../preparing_files_for_zoom_simulations/zoom_parameters.txt'
fp=open(path_to_parameter_file)
line=1
while line:
    line = fp.readline()
    exec(line)


FOLDERNAME='L%dn%d_%s'%(BOXSIZE_IN_MPC,N,TYPE)
if not os.path.exists(path_to_generated_files+FOLDERNAME):
        print("Making new directory")
        os.makedirs(path_to_generated_files+FOLDERNAME)
        
if not os.path.exists(path_to_generated_files+FOLDERNAME+'/'+'MUSIC'):
        print("Making new directory")
        os.makedirs(path_to_generated_files+FOLDERNAME+'/'+'MUSIC')
        
if not os.path.exists(path_to_generated_files+FOLDERNAME+'/'+'AREPO'):
        print("Making new directory")
        os.makedirs(path_to_generated_files+FOLDERNAME+'/'+'AREPO')
        
zoom_centers,zoom_extent=numpy.load('../preparing_files_for_zoom_simulations/Volume_parameters_for_MUSIC.npy')
        
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
    '(%.3f,%.3f,%.3f)'%(zoom_centers[0],zoom_centers[1],zoom_centers[2]),
    '(%.3f,%.3f,%.3f)'%(zoom_extent[0],zoom_extent[1],zoom_extent[2]) 
     ])

variables_to_be_edited_in_AREPO_config=numpy.array([
    'PMGRID',
    'PLACEHIGHRESREGION'])
parameter_values_in_AREPO_config=numpy.array(['%d'%N,
                                              2])

variables_to_be_edited=numpy.array(['SnapshotFileBase',
                                    'TimeBegin',
                                    'Omega0',
                                    'OmegaLambda',
                                    'OmegaBaryon',
                                    'HubbleParam',
                                    'BoxSize'])
parameter_values=numpy.array(['snap',
                              '%.7f'%(1./(1+zstart)),
                              '%.4f'%om_m,
                              '%.4f'%om_l,
                              '%.6f'%om_b,
                              '%.3f'%H0,
                              '%d'%(BOXSIZE_IN_MPC*1000)])




def generate_file(prototypefilepath,generated_music_config_filename,variables_to_be_edited,parameter_values,split_character):
    fp=open(prototypefilepath)
    
    line = fp.readline()
    music_config=open(path_to_generated_files+FOLDERNAME+generated_music_config_filename,'w')
    while line:
        #print(line)
        line = fp.readline()

        line_to_write=line

        if (split_character in line):
            line_splitted=line.split(split_character)
            parameter_name,parameter_value=line_splitted[0],line_splitted[1]
            #print(parameter_name)
            for name,value in list(zip(variables_to_be_edited,parameter_values)):
                #print(name, parameter_name)
                #print(name in parameter_name)

                if (parameter_name in name)|(name in parameter_name):
                    #print("Match")
                    line_to_write='%s\t\t %s \t%s\n'%(name,split_character,value)

                    continue
                    #   

        #if ()

        music_config.write(line_to_write) 
        print(line_to_write)
        #cnt += 1
    music_config.close()
    
if(len(variables_to_be_edited_in_MUSIC)!=len(parameter_values_in_MUSIC)):
    print("ERROR: must have equal number of parameters and their values")
    exit

split_character='='
generate_file(prototypefilepath_MUSIC,generated_MUSIC_config_filename,variables_to_be_edited_in_MUSIC,parameter_values_in_MUSIC,split_character)

if(len(variables_to_be_edited_in_AREPO_config)!=len(parameter_values_in_AREPO_config)):
    print("ERROR: must have equal number of parameters and their values")
    exit

split_character='='
generate_file(prototypefilepath_AREPO,generated_AREPO_config_filename,variables_to_be_edited_in_AREPO_config,parameter_values_in_AREPO_config,split_character)

if(len(variables_to_be_edited)!=len(parameter_values)):
    print("ERROR: must have equal number of parameters and their values")
    exit
prototypefilepath = '/ufrc/lblecha/aklantbhowmick/arepo_runs_aklant/L25n32MUSIC_zoom_levelmax7_padding8/param.txt'
generated_music_config_filename = '/AREPO/param.txt'
split_character=' '
generate_file(prototypefilepath,generated_music_config_filename,variables_to_be_edited,parameter_values,split_character)



