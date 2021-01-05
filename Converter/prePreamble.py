

def run(numberOfDats,counter):

    end_text = '\nENDDAT'
    i = 0

    while i < numberOfDats:
        i += 1
        dat_code_path = 'RobotMilling/Dat/CNC/CNC{}.dat'.format(i)
        dat_code = open(dat_code_path, "r")
        lines = dat_code.readlines()
        dat_code.close()
        dat_code = open(dat_code_path, 'w')
        pre_text = 'DEFDAT CNC%d Public \n' % (i)


        if i != numberOfDats:
            arraypremable = 'DECL GLOBAL FRAME gfCNCPoint%s[%d] \n \n \n' % (i, 30000)
        else:
            arraypremable = 'DECL GLOBAL FRAME gfCNCPoint%s[%d] \n \n \n' % (i, counter)

        lines.insert(0,arraypremable)
        lines.insert(0, pre_text)
        lines.append(end_text)

        dat_code.writelines(lines)
        dat_code.close()

def src_loop(numberOfDats,counter):

    loop_name = 'CNC_LOOP'
    src_code_editor = open('RobotMilling/Milling/Loop/{}.src'.format(loop_name), 'w')
    src_code = []
    src_code.append('DEF {}() \n'.format(loop_name))
    src_code.append('INT counter \n')
    text = []
    for i in range(1,numberOfDats+1):

        if i != numberOfDats:
            arraypremable = '\nFOR counter = 1 TO 30000 \n'
        else:
            arraypremable = '\nFOR counter = 1 TO %d \n'% (counter)
        text.append(arraypremable)

        arraypremable = 'gfCNCPoint%s[counter].A=-30 \n' % (i)
        text.append(arraypremable)
        arraypremable = 'LIN gfCNCPoint%s[counter] C_VEL \n' % (i)
        text.append(arraypremable)
        arraypremable = 'ENDFOR \n'
        text.append(arraypremable)




    src_code.extend(text)
    src_code.append('\nEND')
    src_code_editor.writelines(src_code)
    src_code_editor.close()


