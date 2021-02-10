import os

def DirMaker():
    GcodeDir()

    try:
        path ="RobotMilling/Milling"
        os.makedirs(path)

    except OSError:
        print(path + "Exists")

    try:
        path = "RobotMilling/Milling/CNC/"

        os.makedirs(path)
    except OSError:
        print(path + "Exists")

    try:
        path = "RobotMilling/Milling/CNC/Loop"
        os.makedirs(path)

    except OSError:
        print(path + "Exists")


    try:
        path = "RobotMilling/Milling/CNC/Dat/"

        os.makedirs(path)
    except OSError:
        print(path + "Exists")


def DirRemover():

    try:
        path = "RobotMilling/Dat/CNC"
        os.removedirs(path)
        path = "RobotMilling/Milling"
        os.removedirs(path)
    except OSError:
        print("Some Error")


def GcodeDir():

    try:
        path ="RobotMilling/Gcode"
        os.makedirs(path)
        path ="RobotMilling/Dat/CNCTemp"
        os.makedirs(path)
    except OSError:
        print(path + "Exists")

def CNCCleaner():
    try:
        mydir = 'RobotMilling/Milling/CNC/Loop'
        for f in os.listdir(mydir):
            if not f.endswith(".src"):
                continue
            os.remove(os.path.join(mydir, f))

    except OSError:
        print("Oh christ Some Error " + mydir)

    try:
        mydir = 'RobotMilling/Milling/CNC/Dat'
        for f in os.listdir(mydir):
            if not f.endswith(".dat"):
                continue
            os.remove(os.path.join(mydir, f))

    except OSError:
        print("Oh christ Some Error " + mydir)

