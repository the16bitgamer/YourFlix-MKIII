#! /usr/bin/env python
import blkinfo

def GetMountedDrives():
    for drive in all_my_disks:
        if("ram" not in drive["name"]):
            print(drive)