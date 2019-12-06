# arepo_zoom_setups
This is set of codes that can be used to setup zoom simulations using the cosmological code AREPO and initial condition generator MUSIC.

Important note: In order to use this setup, you must already have uniform simulation run with a known random seed for the initail density field.

Following is the sequence of steps o create a zoom setup:

Step 1: Setup your desired configuration. The configuration file is zoom_parameters.txt. Please refer to 'zoom_parameters.txt' for a detailed description of the parameters

Step 2: Execute the python file 'create_zoom_volume_for_a_halo.py'. 

This code selects your desired halo from a uniform volume run, and traces the particles of the halo to the initial conditions. It then constructs a minimum rectangular volume that contains all the particles. A projected image of the selected halo can be seen on 'halo_image.png'. The script also generates the following output files to perform visual sanity checks. The positions of the particles at the initial time (z=127 by default) can be seen on 'halo_particles_close_to_initial_condition.png'. The initial distributions of particles along x y z and the resulting choice of zoom volume can be seen on 'distribution_of_particles_and_volume_selection.png'  
        
 Step 3:  Execute the python file 'create_config_files_for_MUSIC.py'. This generates the entire configuration for MUSIC in the location given by:        path_to_generated_files + FOLDERNAME  + '/MUSIC'
 
where the variables 'path_to_generated_files' and 'FOLDERNAME' are set by user on 'zoom_parameters.txt'

Step 4: Go to the generated 'MUSIC' folder and execute the code using the command './MUSIC MUSIC_CONFIG.txt'. This generates the output initial condition file 'IC.hdf5'

Step5:   Execute the python file 'create_config_files_for_AREPO.py'. This generates the entire configuration for AREPO in the location given by:        path_to_generated_files + FOLDERNAME  + '/AREPO'

Step6:  Go to the generated 'AREPO/arepo' folder and compile arepo using the command 'make'. 

Step7: Submit the job using the job script 'AREPO/arepo.job'
 
 
 





