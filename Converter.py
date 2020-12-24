import easygui as g
import preamble as p

msg = ' Select desired file to be converted'
#cnc_code_path = g.fileopenbox(msg)
cnc_code_path = None
if cnc_code_path == None:
    cnc_code_path= 'SideCut.txt'


cnc_code = open(cnc_code_path, "r")
lines = cnc_code.readlines()
cnc_code.close()


msg = ' Select desired converted file location'
#converted_code_path = g.fileopenbox(msg)
converted_code_path = None
if converted_code_path == cnc_code_path:
    print("FATAL ERROR")
    quit()
elif converted_code_path == None:
    converted_code_path = 'SideCut_ReWritten.dat'
    print(converted_code_path)


rewritten_code = open(converted_code_path, 'w')


counter = 0
gfArrayTracker = 1



for line in lines:
    # Removes all non-move operations
    if line.startswith('GOTO/') and line.count(',') < 4:




      if counter >= 30000:
          counter = 0
          gfArrayTracker = gfArrayTracker + 1


          rewritten_code.write('\n')

      else:


        # Keeps track of array size
        counter = counter + 1
        gfCncPoint = 'gfCNCPoint{}[{}]'.format(gfArrayTracker,counter)
        line = line.replace('GOTO/', gfCncPoint + ' = {X ')

        # Removes \n from the end of the string
        line = line.strip()

        # Split line according to where commas appear
        line = line.split(',')

        # Append the appropriate signum for KRL
        line[1] = ', ' + 'Y ' + line[1] + ', '
        line[2] = 'Z ' + line[2] + ', '
        line.append('A 0.000, ')
        line.append('B 0.000, ')
        line.append('C 0.000 } ')

        # Write to file
        for i in range(0, len(line)):
            rewritten_code.write(line[i])
        rewritten_code.write('\n')



rewritten_code = open(converted_code_path, 'r')

end_code = []
end_code.extend(p.dat_top(gfArrayTracker))
end_code.extend((p.dat_array_maker(gfArrayTracker)))
end_code.extend(p.dat_last_array(gfArrayTracker,counter))
end_code.extend(rewritten_code.readlines())


rewritten_code = open(converted_code_path, 'w')
rewritten_code.writelines(end_code)
rewritten_code.write(p.dat_bot())
rewritten_code.close()

src_code_editor = open('src_Code.txt', 'w')
src_code=[]
src_code.extend((p.src_array_maker(gfArrayTracker)))
src_code.extend(p.src_last_array(gfArrayTracker,counter))
src_code_editor.writelines(src_code)
src_code_editor.close()


