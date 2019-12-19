import sys
sys.path.append('/home/aklantbhowmick/anaconda3/lib/python3.7/site-packages')
sys.path.append('/home/aklantbhowmick/anaconda3/lib/python3.7/site-packages/scalpy/')
sys.path.append('/home/aklantbhowmick/anaconda3/envs/nbodykit-env/lib/python3.6/site-packages/')
import mdot_to_Lbol
import arepo_package
import scipy.interpolate
radiative_efficiency=0.1
total_conv=mdot_to_Lbol.get_conversion_factor_arepo(radiative_efficiency)
import h5py
from matplotlib import pyplot as plt
import numpy

#%pylab inline

scaled_halo_centers=numpy.array([1.,1.,1.])

def get_group_ids(output_path,z_current,N,group_type='group'):    
    if (group_type=='groups'):              
        masstype,output_redshift=(arepo_package.get_group_property(output_path,'GroupMassType', desired_redshift));
    elif (group_type=='subhalo'):              
        masstype,output_redshift=(arepo_package.get_subhalo_property(output_path,'SubhaloMassType', desired_redshift));
        subhalo_group_number,output_redshift=(arepo_package.get_subhalo_property(output_path,'SubhaloGrNr', desired_redshift));
        
    mass=masstype[:,1]
    indices=numpy.argsort(mass)[-N:]
    if (group_type=='groups'):   
        return indices
    if (group_type=='subhalo'):  
        return indices,subhalo_group_number[indices]


path_to_parameter_file='zoom_parameters.txt'    
fp=open(path_to_parameter_file)
line=1
while line:
    line = fp.readline()
    exec(line)
    
    
    
#path_to_uniform_run='/ufrc/lblecha/aklantbhowmick/arepo_runs_aklant/'
#uniform_run='L25n128MUSIC_rerun'
#index_of_selected_halo=5
#desired_redshift_of_selected_halo=0
#earlier_redshift=125    

    
    
basePath=path_to_uniform_run+uniform_run+'/output/'
boxsize=arepo_package.get_box_size(basePath)
particle_property='Coordinates'
p_type=1
group_particles,output_redshift=arepo_package.get_particle_property_within_groups(basePath,particle_property,p_type,desired_redshift_of_selected_halo,index_of_selected_halo,group_type='groups',list_all=True)

particle_property='ParticleIDs'
ParticleIDs,output_redshift=arepo_package.get_particle_property_within_groups(basePath,particle_property,p_type,desired_redshift_of_selected_halo,index_of_selected_halo,group_type='groups',list_all=True)
boxsize=arepo_package.get_box_size(basePath)

h=h5py.File('/orange/lblecha/aklantbhowmick/ICs_with_MUSIC/L25n128MUSIC_uniform.hdf5')
hp1=h.get('PartType1')
ParticleIDs_in_IC=hp1.get('ParticleIDs')[:]
Coordinates_in_IC=hp1.get('Coordinates')[:]

particle_property='ParticleIDs'
ParticleIDs_early,output_redshift_early=arepo_package.get_particle_property(basePath,particle_property,p_type,earlier_redshift)
particle_property='Coordinates'
Coordinates_early,output_redshift_early=arepo_package.get_particle_property(basePath,particle_property,p_type,earlier_redshift)

def find_index(b):
    return (numpy.where(ParticleIDs_early==b))[0]
vec_find_index=numpy.vectorize(find_index)
indices_particles=vec_find_index(ParticleIDs)
Coordinates_early_selected=Coordinates_early[indices_particles]


initial_positions_of_halo_particles=Coordinates_in_IC[ParticleIDs]
f,ax=plt.subplots(figsize=(10,10))
#arepo_package.make_image(group_particles,group_particles,'yz',ax,boxsize,NBINS=200,colormap='Blues_r',opacity=0.4)
arepo_package.make_image(group_particles,group_particles,'xy',ax,boxsize,200,scaled_halo_centers,colormap='Blues_r',opacity=1,about_COM=True,REPOSITION=False)

ax.tick_params(labelsize=30)
ax.set_xlabel('$X-X_{\mathrm{COM}}$',fontsize=30)
ax.set_ylabel('$Y-Y_{\mathrm{COM}}$',fontsize=30)
plt.savefig('halo_image.png',bbox_inches='tight')

initial_positions_of_halo_particles=Coordinates_in_IC[ParticleIDs]
f,ax=plt.subplots(figsize=(10,10))
#arepo_package.make_image(Coordinates_early_selected,group_particles,'yz',ax,boxsize,NBINS=20,colormap='Blues_r',opacity=0.4)
arepo_package.make_image(Coordinates_early_selected,group_particles,'xy',ax,boxsize,200,scaled_halo_centers,colormap='Blues_r',opacity=1,about_COM=True,REPOSITION=False)

ax.tick_params(labelsize=30)
ax.set_xlabel('$X-X_{\mathrm{COM}}$',fontsize=30)
ax.set_ylabel('$Y-Y_{\mathrm{COM}}$',fontsize=30)
plt.savefig('halo_particles_close_to_initial_condition.png',bbox_inches='tight')

f,ax=plt.subplots(1,3,figsize=(18,7),sharey=True,sharex=True)
centers,counts,xmin,xmax=arepo_package.get_distribution(Coordinates_early_selected[:,0],100,-boxsize/2,5*boxsize/2,boxsize,min_count)
ax[0].plot(centers,counts)
ax[0].axvspan(xmin,xmax,alpha=0.3)

centers,counts,ymin,ymax=arepo_package.get_distribution(Coordinates_early_selected[:,1],100,-boxsize/2,5*boxsize/2,boxsize,min_count)
ax[1].plot(centers,counts)
ax[1].axvspan(ymin,ymax,alpha=0.3)
centers,counts,zmin,zmax=arepo_package.get_distribution(Coordinates_early_selected[:,2],100,-boxsize/2,5*boxsize/2,boxsize,min_count)
ax[2].plot(centers,counts)
ax[2].axvspan(zmin,zmax,alpha=0.3)

ax[0].set_xlabel('x',fontsize=30)
ax[1].set_xlabel('y',fontsize=30)
ax[2].set_xlabel('z',fontsize=30)
ax[0].set_ylabel('Number of particles',fontsize=30)
ax[0].tick_params(labelsize=20)
ax[1].tick_params(labelsize=20)
ax[2].tick_params(labelsize=20)
plt.savefig('distribution_of_particles_and_volume_selection.png',bbox_inches='tight')

plt.subplots_adjust(wspace=0)
zoom_volume_mins=numpy.array([xmin,ymin,zmin])
zoom_volume_maxs=numpy.array([xmax,ymax,zmax])
zoom_volume_centers=(zoom_volume_maxs+zoom_volume_mins)/2/boxsize
zoom_volume_centers[zoom_volume_centers<0]+=1
zoom_volume_centers[zoom_volume_centers>1]-=1

zoom_volume_extent=(zoom_volume_maxs-zoom_volume_mins)/boxsize  
numpy.save('Volume_parameters_for_MUSIC.npy',[zoom_volume_centers,zoom_volume_extent])
