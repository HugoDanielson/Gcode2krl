import prePreamble as p
import MakeDirectory as m
from prePreamble import ABCTracker

#Strategy:
# Load G-CODE
# 1 Remove all none move commands
# 2 Keep track of array Size
# 3 Append missing data for KRL readable
# 4 write to temp file
# 5 Read from temp file
# 6 Parse temp file into several Dat Files with 30 000 as maximum array size
# 7 Create corresponding SRC


grfeedrate = '0'
tempfeedrate = '0'
#m.DirMaker()
m.CNCCleaner()

ABCTracker = ABCTracker()
cnc_code_path= 'RobotMilling/Gcode/CNC.txt'
converted_code_path = 'RobotMilling/Dat/CNCTemp/Temp.dat'
final_code_path = 'RobotMilling/Milling/CNC/Dat/CNC1.dat'
cnc_code = open(cnc_code_path, "r")
rewritten_code = open(converted_code_path, 'w')

lines = cnc_code.readlines()
cnc_code.close()



for line in lines:
    # Removes all non-move operations
    if line.startswith('RAPID'):
        grfeedrate = str(2000)

    elif line.startswith('FEDRAT/'):

        tempfeedrate,grfeedrate = p.feed_rate_handler(line)



    elif line.startswith('GOTO/'):

       lines = p.frame_maker(line,grfeedrate,ABCTracker)

       for i in range(0, len(lines)):
           rewritten_code.write(lines[i])
       rewritten_code.write('\n')

    else:
        grfeedrate = tempfeedrate

rewritten_code = open(converted_code_path, 'r')
lines = rewritten_code.readlines()
rewritten_code.close()


gfArrayTracker,counter = p.final_code_handler(final_code_path,lines)

p.run(gfArrayTracker,counter)
p.src_loop(gfArrayTracker,counter,'CNC_LOOP')
