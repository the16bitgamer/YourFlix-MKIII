#! /usr/bin/env python
import sys
sys.path.append("..")
from Resources import yf_Defaults as Defaults
from Utilities import yf_Log as Log
from Utilities import PipManager


def VerifyPackageInstalls(UPDATE = False):
    for package in Defaults.PythonModuals:
        name = package[0]
        fileName = package[1]
        packageName = package[2]
        installed = PipManager.IsInstalledPip(name)
        Log.Debug(name + " " + str(installed))
        if(not installed and not UPDATE):
            PipManager.InstallPy(fileName, packageName)

