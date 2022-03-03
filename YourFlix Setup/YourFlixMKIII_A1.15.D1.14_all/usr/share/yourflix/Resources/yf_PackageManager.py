#! /usr/bin/env python
import sys
import yf_Defaults as Defaults
import yf_Log as Log
import PipManager
import AptManager


def VerifyPackageInstalls():
    for package in Defaults.Packages:
        installed = AptManager.IsInstalledApt(package)
        Log.Debug(package + " " + str(installed))
        if(not installed):
            AptManager.InstallApt(package)
    for package in Defaults.PythonModuals:
        name = package[0]
        fileName = package[1]
        packageName = package[2]
        installed = PipManager.IsInstalledPip(name)
        Log.Debug(name + " " + str(installed))
        if(not installed):
            PipManager.InstallPy(fileName, packageName)

