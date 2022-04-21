#! /usr/bin/env python

import sys
sys.path.insert(0, './Resources')
sys.path.insert(0, './FileManager')
sys.path.insert(0, './Utilities')
sys.path.insert(0, './BackgroundJobs')
import yf_PackageManager as PM

#System Check is used to verify the file and system integrity and install/fixes packages to ensure YourFlix will work correctly
#Phase 1 Verify Database Integrity and rebuilds database if the Database file is missing (note this does not include programing)
#Phase 2 Verifies that critical files and python packages are installed and will install them for us if they are not (python has local file stores as a fail safe should've installed during main install)
#Phase 3 Verifies File integrity (check if all targeted files used by YourFlix have the correct formatting and restores them if a backup exists and backs them up when done)
#Phase 4 Verifies Mountable Drives (used if database hadn't failed and re-mounts drives if an error occurs from backups)

if __name__ == '__main__':
    print("Starting YourFlix Job Manager")
    PM.VerifyPackageInstalls()