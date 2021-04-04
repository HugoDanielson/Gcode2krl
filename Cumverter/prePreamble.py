import numpy as np


def run(numberOfDats, counter):
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
            arraypremable = 'DECL GLOBAL sCNC%s gsCNC%s[%d] \n \n \n' % (i, i, 30000)
        else:
            arraypremable = 'DECL GLOBAL sCNC%s gsCNC%s[%d]  \n \n \n' % (i, i, counter)

        lines.insert(0, arraypremable)
        lines.insert(0, pre_text1)
        lines.insert(0, pre_text)

        lines.append(end_text)

        dat_code.writelines(lines)
        dat_code.close()


def src_loop(numberOfDats, counter, loop_name):
    # loop_name = 'CNC_LOOP'
    src_code_editor = open('RobotMilling/Milling/CNC/Loop/{}.src'.format(loop_name), 'w')
    src_code = []
    src_code.append('DEF {}() \n'.format(loop_name))
    src_code.append('INT counter \n')
    text = []
    for i in range(1, numberOfDats + 1):

        if i != numberOfDats:
            arraypremable = '\nFOR counter = 1 TO 30000 \n'
        else:
            arraypremable = '\nFOR counter = 1 TO %d \n' % (counter)
        text.append(arraypremable)

        # arraypremable = 'gfCNCPoint%s[counter].A=0 \n' % (i)
        # text.append(arraypremable)
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


class ABCTracker():
    def __init__(self):
        self.TempData = [0.00, 0.00, 0.00]

    def Retrieve(self):
        return self.TempData

    def Store(self, TempData):
        self.TempData = TempData


def frame_maker(line, grfeedrate, ABC):
    line = line.replace('GOTO/', '')
    line = line.strip()
    line = line.split(',')

    # Append the appropriate signum for KRL

    if len(line) == 6:

        line[0] = '{X ' + line[0] + ', '
        line[1] = 'Y ' + line[1] + ', '
        line[2] = 'Z ' + line[2] + ', '
        line[3] = 'A ' + str(np.rad2deg(np.arccos(float(line[3])))) + ', '
        line[4] = 'B ' + str(np.rad2deg(np.arccos(float(line[4])))) + ', '
        line[5] = ' C ' + str(np.rad2deg(np.arccos(float(line[5])))) + '}'
        line.append(', grFeedrate ' + grfeedrate + '}')

        StoreData = [line[3], line[4], line[5]]
        ABC.Store(StoreData)

        # templine[0] = line[3]
        # templine[1] = line[4]
        # templine[2] = line[5]

    elif len(line) == 3:
        # line[0] = gfCncPoint + ' = {X ' + line[0] + ', '
        line[0] = '{X ' + line[0] + ', '
        line[1] = 'Y ' + line[1] + ', '
        line[2] = 'Z ' + line[2] + ', '
        line.append(ABC.retreive())

        # line.append('A 0.000, ')
        # line.append('B 0.000, ')
        # line.append('C 0.000 } ')
        line.append(', grFeedrate ' + grfeedrate + '}')
    return line  # , templine[]


def feed_rate_handler(line):
    line = line.replace('MMPM,', '')
    line = line.strip()
    line = line.split('/')

    tempfeedrate = str(float(line[1]) / 60)
    grfeedrate = tempfeedrate

    return tempfeedrate, grfeedrate


def final_code_handler(final_code_path, lines):
    counter = 0
    gfArrayTracker = 1
    final_code = open(final_code_path, 'w')

    for line in lines:
        if counter >= 30000:
            counter = 0
            final_code.close()
            gfArrayTracker += 1
            final_code_path = 'RobotMilling/Milling/CNC/Dat/CNC{}.dat'.format(gfArrayTracker)
            final_code = open(final_code_path, 'w')
        counter += 1
        gfCncPoint = 'gsCNC%s[%d] = {fCnC ' % (gfArrayTracker, counter)
        line = gfCncPoint + line

        for i in range(0, len(line)):
            final_code.write(line[i])

    final_code.close()

    return gfArrayTracker, counter
