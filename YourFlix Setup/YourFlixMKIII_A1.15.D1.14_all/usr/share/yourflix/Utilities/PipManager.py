#! /usr/bin/env python
import subprocess
import importlib.util
import sys
import os
import NetworkCheck
import yf_Log as Log

PackageLoc = "./Resources/lib"

def InstallPy(PACKAGE_NAME, PACKAGE):
    path = os.path.join(PackageLoc,PACKAGE_NAME)
    if(NetworkCheck.CheckPypi()):
        Log.Debug("Installing " + PACKAGE + " via Network")
        ans = subprocess.check_call([sys.executable, "-m", "pip", "install", PACKAGE])
    else:
        Log.Debug("Installing " + PACKAGE + " Locally")
        ans = subprocess.check_call([sys.executable, "-m", "pip", "install", path])

def IsInstalledPip(PACKAGE_NAME):
    if (importlib.util.find_spec(PACKAGE_NAME)):
        return True
    else:
        return False