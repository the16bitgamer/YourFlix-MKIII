#! /usr/bin/env python
import sys
import sqlite3

from BackgroundJobs import yf_DatabaseManager as DM
from BackgroundJobs import yf_ConfigManager as CM
from BackgroundJobs import yf_StorageManager as SM
from Utilities import yf_Log as Log

if __name__ == '__main__':
    CM.LoadConfig()
    DM.PrepareDatabase()
    SM.CheckMountedDrives()
    CM.UpdateConfig()