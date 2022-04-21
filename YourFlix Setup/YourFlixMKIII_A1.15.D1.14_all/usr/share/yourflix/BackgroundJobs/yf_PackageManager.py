#! /usr/bin/env python
#Import from Parent DIR
import sys, os
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from Resources import yf_Defaults as Defaults
from Utilities import yf_Log as Log
from Utilities import PipManager


def VerifyPackageInstalls():
    for package in Defaults.PythonModuals:
        name = package[0]
        fileName = package[1]
        packageName = package[2]
        installed = PipManager.IsInstalledPip(name)
        Log.Debug(name + " " + str(installed))
        if(not installed):
            PipManager.InstallPy(fileName, packageName)


def UpdatePackages():
    for package in Defaults.PythonModuals:
        name = package[0]
        packageName = package[2]
        Log.Debug("Checking for updates for: " + name)
        PipManager.UpdatePy(packageName)