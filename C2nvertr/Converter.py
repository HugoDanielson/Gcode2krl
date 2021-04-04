import easygui as g
import prePreamble as p
import MakeDirectory as m
import numpy as np
import os

#Strategy:
# Load G-CODE
# 1 Remove all none move commands
# 2 Keep track of array Size
# 3 Append missing data for KRL readable
# 4 write to temp file
# 5 Read from temp file
# 6 Parse temp file into several Dat Files with 30 000 as maximum array size
# 7 Create corresponding SRC

path_name = 'Mill_RIGHT'
point_name = 'gs' + path_name
loop_name = path_name + "_Loop"
counter = 0
gfArrayTracker = 1
grfeedrate = '0'
tempfeedrate = '0'
gABC = [0.0,0.0,0.0]
#m.DirMaker()
#m.CNCCleaner()



cnc_code_path= 'RobotMilling/Gcode/{}.txt'.format(path_name)
cnc_code = open(cnc_code_path, "r")
lines = cnc_code.readlines()
cnc_code.close()


converted_code_path = 'RobotMilling/Dat/CNCTemp/Temp.dat'
rewritten_code = open(converted_code_path, 'w')




for line in lines:
    # Removes all non-move operations
    if line.startswith('RAPID'):
        grfeedrate = str(3000)

    elif line.startswith('FEDRAT/'):
        line = line.replace('MMPM,', '')
        line = line.strip()
        line = line.split('/')

        tempfeedrate = str(float(line[1]) / 60)
        grfeedrate = tempfeedrate





    elif line.startswith('GOTO/'):

        line = line.replace('GOTO/', '')
        line = line.strip()
        line = line.split(',')



        # Append the appropriate signum for KRL

        if len(line) == 6:
            #line[0] = gfCncPoint + ' = {X ' + line[0] + ', '
            line[0] =  '{X ' + line[0] + ', '
            line[1] =  'Y ' + line[1] + ', '
            line[2] = 'Z ' + line[2] + ', '
            #line[3] =  'A ' + str( round(np.rad2deg(np.arccos(float(line[3])))-180.0,4)) + ', '
            #line[4] =  'B ' + str(round(np.rad2deg(np.arccos(float(line[4])))-90,4)) + ', '
            #line[5] = ' C ' + str(round(np.rad2deg(np.arccos(float(line[5])))-90.0,4)) +  '}'
            line[3] =  'A ' + '0' + ', '
            line[4] =  'B ' + '0' + ', '
            line[5] = ' C ' + '0' +  '}'
            line.append(', grFeedrate ' + grfeedrate + '}' )

            gABC = [line[3],line[4],line[5]]

        elif len(line) == 3:

            # line[0] = gfCncPoint + ' = {X ' + line[0] + ', '
            line[0] = '{X ' + line[0] + ', '
            line[1] =  'Y ' + line[1] + ', '
            line[2] = 'Z ' + line[2] + ', '

            for j in range(0,3):
                line.append(gABC[j])

            line.append(', grFeedrate ' + grfeedrate + '}')


        # Write to file
        for i in range(0, len(line)):
            rewritten_code.write(line[i])
        rewritten_code.write('\n')
    else:
        grfeedrate = tempfeedrate

rewritten_code = open(converted_code_path, 'r')
lines = rewritten_code.readlines()
rewritten_code.close()


#final_code_path = 'RobotMilling/Dat/CNC/CNC{}.dat'.format(gfArrayTracker)
final_code_path = 'RobotMilling/Milling/CNC/Dat/{}{}.dat'.format(path_name, gfArrayTracker)
final_code = open(final_code_path, 'w')



for line in lines:

    if counter >= 30000:
        counter = 0
        final_code.close()

        gfArrayTracker = gfArrayTracker + 1
        final_code_path = 'RobotMilling/Milling/CNC/Dat/{}{}.dat'.format(path_name, gfArrayTracker)

        final_code = open(final_code_path, 'w')


    #else:
    # Keeps track of array size
    counter = counter + 1
    #point_name = 'gsCNC'
    gfCncPoint = '%s%s[%d] = {fCnC '%(point_name, gfArrayTracker, counter)
    line = gfCncPoint + line


    # Write to file



    for i in range(0, len(line)):
        final_code.write(line[i])



final_code.close()


p.run(gfArrayTracker, counter, point_name, path_name)
p.src_loop(gfArrayTracker, counter,loop_name, point_name)
