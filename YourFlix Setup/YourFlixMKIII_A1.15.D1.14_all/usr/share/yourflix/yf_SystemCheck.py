#! /usr/bin/env python
import sys
from BackgroundJobs import yf_PackageManager as PM
from BackgroundJobs import yf_ConfigManager as CM

if __name__ == '__main__':
    CM.LoadConfig()
    PM.VerifyPackageInstalls()