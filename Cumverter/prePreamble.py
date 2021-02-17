

def run(numberOfDats,counter):

    end_text = '\nENDDAT'
    i = 0

    while i < numberOfDats:
        i += 1
        dat_code_path = 'RobotMilling/Milling/CNC/DAT/CNC{}.dat'.format(i)
        dat_code = open(dat_code_path, "r")
        lines = dat_code.readlines()
        dat_code.close()
        dat_code = open(dat_code_path, 'w')
        pre_text = 'DEFDAT CNC%d Public \n' % (i)
        pre_text1 = 'GLOBAL STRUC sCNC%d FRAME fCNC, INT grFeedrate \n' % (i)


        if i != numberOfDats:
            arraypremable = 'DECL GLOBAL sCNC%s gsCNC%s[%d] \n \n \n' % (i,i, 30000)
        else:
            arraypremable = 'DECL GLOBAL sCNC%s gsCNC%s[%d]  \n \n \n' % (i,i, counter)

        lines.insert(0,arraypremable)
        lines.insert(0, pre_text1)
        lines.insert(0, pre_text)

        lines.append(end_text)

        dat_code.writelines(lines)
        dat_code.close()

def src_loop(numberOfDats,counter,loop_name):

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
        arraypremable = 'LIN gsCNC%s[counter].fCNC C_VEL \n' % (i)
        changeSpeedpremable = 'ChangeSpeed(gsCNC%s[counter].grfeedrate)\n' % (i)
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

