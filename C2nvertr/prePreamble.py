

def run(numberOfDats, counter, point_name, path_name):

    end_text = '\nENDDAT'
    i = 0
    while i < numberOfDats:
        i += 1
        dat_code_path = 'RobotMilling/Milling/CNC/DAT/{}{}.dat'.format(path_name, i)
        dat_code = open(dat_code_path, "r")
        lines = dat_code.readlines()
        dat_code.close()
        dat_code = open(dat_code_path, 'w')
        pre_text = 'DEFDAT %s%d Public \n' % (path_name, i)
        pre_text1 = 'GLOBAL STRUC s%s%d FRAME fCNC, INT grFeedrate \n' % (path_name, i)


        if i != numberOfDats:
            arraypremable = 'DECL GLOBAL s%s%s %s%s[%d] \n \n \n' % (path_name,i, point_name, i, 30000)
        else:
            arraypremable = 'DECL GLOBAL s%s%s %s%s[%d]  \n \n \n' % (path_name,i, point_name, i, counter)

        lines.insert(0,arraypremable)
        lines.insert(0, pre_text1)
        lines.insert(0, pre_text)

        lines.append(end_text)

        dat_code.writelines(lines)
        dat_code.close()

def src_loop(numberOfDats, counter, loop_name, point_name):

    #loop_name = 'CNC_LOOP'
    src_code_editor = open('RobotMilling/Milling/CNC/Loop/{}.src'.format(loop_name), 'w')
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

        #arraypremable = 'gfCNCPoint%s[counter].A=0 \n' % (i)
        #text.append(arraypremable)
        arraypremable =       '     LIN %s%s[counter].fCNC C_VEL \n' % (point_name, i)
        changeSpeedpremable = '     ChangeSpeed(%s%s[counter].grfeedrate)\n' % (point_name, i)
        EnDForpremable = 'ENDFOR \n'
        text.append(changeSpeedpremable)
        text.append(arraypremable)
        text.append(EnDForpremable)




    src_code.extend(text)
    src_code.append('\nEND \n \n \n')

    ChangeSpeed = 'DEF ChangeSpeed(lrFeedRate:IN) \n' \
                  '     REAL lrFeedRate \n \n \n' \
                  '     LDAT_ACT.VEL = lrFeedRate * (DEF_VEL_CP / (DEF_VEL_CP*1000)) \n \n' \
                  '        IF (lrFeedRate < 1.0) THEN \n' \
                  '             PDAT_ACT.VEL = 1 \n' \
                  '             PDAT_ACT.VEL = lrFeedRate \n' \
                  '        ENDIF \n \n' \
                  '     BAS(#CP_DAT) \n' \
                  '     BAS(#PTP_DAT) \n' \
                  '\nEND \n \n \n'

    src_code.append(ChangeSpeed)
    src_code_editor.writelines(src_code)
    src_code_editor.close()

