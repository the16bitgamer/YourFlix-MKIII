#! /usr/bin/env python
#Import from Parent DIR
import sys, os
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

import subprocess
import importlib.util
from Utilities import NetworkCheck
from Utilities import yf_Log as Log
from Resources import yf_LinuxDefaults as LinuxDefaults

PackageLoc = LinuxDefaults.PyModulesLoc

def InstallPy(PACKAGE_NAME, PACKAGE):
    path = os.path.join(PackageLoc,PACKAGE_NAME)
    if(NetworkCheck.CheckPypi()):
        Log.Debug("Installing " + PACKAGE + " via Network")
        ans = subprocess.check_call([sys.executable, "-m", "pip", "install", PACKAGE])
    else:
        Log.Debug("Installing " + PACKAGE + " Locally")
        ans = subprocess.check_call([sys.executable, "-m", "pip", "install", path])

def UpdatePy(PACKAGE):
    if(NetworkCheck.CheckPypi()):
        Log.Debug("Updating " + PACKAGE + " via Network")
        ans = subprocess.check_call([sys.executable, "-m", "pip", "install", PACKAGE, "-U"])
    else:
        Log.Debug("No network connection. Cannot Check for " + PACKAGE + " Updates")


def IsInstalledPip(PACKAGE_NAME):
    if (importlib.util.find_spec(PACKAGE_NAME)):
        return True
    else:
        return False