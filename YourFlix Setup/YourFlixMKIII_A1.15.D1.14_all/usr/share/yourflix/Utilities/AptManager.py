#! /usr/bin/env python
import apt
import NetworkCheck
import yf_Log as Log
import yf_Execptions

def InstallApt(PACKAGE_NAME):
    cache = apt.cache.Cache()
    cache.update()
    cache.open()

    pkg = cache[PACKAGE_NAME]
    if pkg.is_installed:
        Log.Debug(PACKAGE_NAME+" is already installed")
    else:
        pkg.mark_install()
        cache.commit()
        Log.Debug(PACKAGE_NAME+" has been installed")

def IsInstalledApt(PACKAGE_NAME):
    cache = apt.Cache()
    if(cache[PACKAGE_NAME].is_installed):
        return True
    else:
        if(NetworkCheck.CheckGoogle()):
            return False
        else:
            raise InstallError(PACKAGE_NAME+" is not installed!\nUnable to install due to network error. Please check your Network connect to ensure "+ PACKAGE_NAME+" is installed or install it manually")