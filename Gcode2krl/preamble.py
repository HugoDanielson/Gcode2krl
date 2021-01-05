#funcion of type input(array size: IN, cncframename : IN, Premable : OUT)

#Function Name
def dat_top(counter):
    #p.dat_preamble_top(rewritten_code)
   # rewritten_code.write('\n')
    text = []
    text.append('DEFDAT CNCFRAMES PUBLIC \n')

    for i in range(0,2):
        text.append('\n')
    return text


def dat_bot():
    text = '\nENDDAT'
    return text


def dat_array_maker(arraynumber):
    text = []

    for i in range(1,arraynumber):
        arraypremable = 'DECL GLOBAL FRAME gfCNCPoint%s[%s] \n' % (i, 30000)
        text.append(arraypremable)
    return text

def dat_last_array(arraynumber,counter):
    text = []
    arraypremable = 'DECL GLOBAL FRAME gfCNCPoint%s[%s] \n' % (arraynumber, counter)
    text.append(arraypremable)
    text.append('\n')
    return text


def src_array_maker(arraynumber):
    text = []


    for i in range(1,arraynumber):
        arraypremable = '\nFOR counter = 1 TO 30000 \n'
        text.append(arraypremable)

        arraypremable = 'gfCNCPoint%s[counter].A=-30 \n' % (i)
        text.append(arraypremable)

        arraypremable = 'LIN gfCNCPoint%s[counter] C_VEL \n' % (i)
        text.append(arraypremable)

        arraypremable = 'ENDFOR \n'
        text.append(arraypremable)
    return text

def src_last_array(arraynumber,counter):
    text = []
    arraypremable = '\nFOR counter = 1 TO {} \n'.format(counter)
    text.append(arraypremable)

    arraypremable = 'gfCNCPoint%s[counter] .A=-30 \n' % (arraynumber)
    text.append(arraypremable)

    arraypremable = 'LIN gfCNCPoint%s[counter] C_VEL \n' % (arraynumber)
    text.append(arraypremable)

    arraypremable = 'ENDFOR \n'
    text.append(arraypremable)
    return text


def src_template():
    text = []
    text.append('\n\n\n')
    Int = 'INT lnActSt,lnUsedBase,lnUsedTool,lnBaseNr\n'
    text.append(Int)
    Int = 'INT lnJobNr, lnCounter,lnCounter2,lnSegments\n'
    text.append(Int)
    Int = 'INT counter\n'
    text.append(Int)

    real = 'REAL lrAmountCut, lrWorkPieceSize,lrRadius,lrDepthOfCut\n'
    text.append(real)
    frame = 'FRAME lfZcut \n    FRAME lfToolDiamShift\n FRAME lfStartMillingPos\n FRAME lfBaseShift\n FRAME lfBaseCycleZ\n'
    text.append(frame)

    frame = 'FRAME lfBaseCycleShift \n    FRAME lfCircAuxPoint1\n FRAME lfCircEndPoint1\n'
    text.append(frame)

    return text