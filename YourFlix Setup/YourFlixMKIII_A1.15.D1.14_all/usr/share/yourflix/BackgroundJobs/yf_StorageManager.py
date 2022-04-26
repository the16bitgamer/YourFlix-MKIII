#! /usr/bin/env python
#Import from Parent DIR
import sys, os
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from Resources import yf_Defaults as Defaults
from Resources import yf_DBDefaults as DBDefaults
from Utilities import yf_Log as Log
from Database import yf_DbHandler as DB
from Resources import yf_Execptions as YException
from BackgroundJobs import yf_DatabaseManager as DBManager

def CheckMountedDrives():
    Log.Debug("Checking the Mounted Drives")
    drivesToMount = Defaults.MountedDrives
    drivesToMount += DBManager.GetMountedDrives('/usr/share/yourflix/yourflix.db')
    checkMounted = []
    for drive in drivesToMount:
        if(drive not in checkMounted):
            Log.Debug(drive[0])
            checkMounted.append(drive)
    Log.Debug(checkMounted)
    MountDrives(checkMounted)

def MountDrives(LIST_OF_DRIVES):
    Log.Debug("Mounting the Drives")
    Defaults.MountedDrives = LIST_OF_DRIVES

if __name__ == '__main__':
    CheckMountedDrives()