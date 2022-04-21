#! /usr/bin/env python
import sys
from BackgroundJobs import yf_PackageManager as PM
from BackgroundJobs import yf_StorageManager as SM
from BackgroundJobs import yf_ConfigManager as CM

#Verification script to ensure fs integrity and db integrity before starting yf
#This is to solve the 'Mike Problem' of the fs delete itself or database becomes corrupted
# while in use. This is to make management easier for si/me

if __name__ == '__main__':
    CM.LoadConfig()
    SM.CheckMountedDrives()
    #PM.VerifyPackageInstalls()