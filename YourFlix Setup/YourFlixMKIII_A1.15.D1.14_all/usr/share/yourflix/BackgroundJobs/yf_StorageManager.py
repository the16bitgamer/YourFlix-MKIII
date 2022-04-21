#! /usr/bin/env python
#Import from Parent DIR
import sys, os
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from Resources import yf_LinuxDefaults as LinuxDefaults
from Utilities import yf_Log as Log
from Utilities import PlatformCheck as PC
from Resources import yf_Execptions as YException

#The Storage Manager is here to set the specifics of mounting Yourflix storage devices
#and tracking it.

def MountDrive(DriveID, FS, PHYSLOC):
    if(PC.GetPlatform() == "Linux"):
        Log.Debug("Mount Storage at Location")
    else:
        Log.Debug("Incompatible Platform, please use YourFlix on Linux")

def UnMountDrive(DriveId):
    if(PC.GetPlatform() == "Linux"):
        Log.Debug("Unmounting Storage at Location")
    else:
        Log.Debug("Incompatible Platform, please use YourFlix on Linux")

def GetAllStorageDrives():
    if(PC.GetPlatform() == "Linux"):
        Log.Debug("Getting Storage Drive")
    else:
        Log.Debug("Incompatible Platform, please use YourFlix on Linux")

def CheckMountedDrives():
    if(PC.GetPlatform() == "Linux"):
        Log.Debug("Verifing Drives and Mount locations")
        if(os.path.exists(LinuxDefaults.Phys_ConfigLoc)):
            Log.Debug("Path Exists "+LinuxDefaults.Phys_DbLoc)
        else:
            raise YException.MissingFileError("YourFlix config failed to generate or was deleted")
    else:
        Log.Debug("Incompatible Platform, please use YourFlix on Linux")

def RestoreMountedDrives():
    if(PC.GetPlatform() == "Linux"):
        Log.Debug("Restoring/Rebuilding FSTAB")
    else:
        Log.Debug("Incompatible Platform, please use YourFlix on Linux")

def CheckDatabase():
    Log.Debug("Check if DB exists and update/rebuild if it does")

if __name__ == '__main__':
    CheckMountedDrives()