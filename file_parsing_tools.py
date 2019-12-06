def generate_file(prototypefilepath,path_to_generated_files,FOLDERNAME,generated_music_config_filename,variables_to_be_edited,parameter_values,split_character):
    fp=open(prototypefilepath)

    line = 1
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
#                    print(generated_music_config_filename)
                    if ('arepo/Config.sh' in generated_music_config_filename):
                          line_to_write='%s%s%s\n'%(name,split_character,value)                          
                    else:
                          line_to_write='%s\t\t %s \t%s\n'%(name,split_character,value)

                    continue
                    #

        #if ()

        music_config.write(line_to_write)
#        print(line_to_write)
        #cnt += 1
    music_config.close()

