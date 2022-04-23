#! /usr/bin/env python
#Import from Parent DIR
import sys, os
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

import sqlite3
from Utilities import yf_Log as Log
from Utilities import PlatformCheck as PC
from Utilities import FileFolderTool as FFT
from Resources import yf_LinuxDefaults as LinuxDefaults
from Resources import yf_DBDefaults as DBDefaults
from Database import yf_DbBuilder as Build
from Database import yf_DbUpdater as Update
from Database import yf_DbHandler as Database

def LoadDatabase():
    if(PC.GetPlatform() == "Linux"):
        Log.Debug("Checking Database Structure")
        FFT.VerifyParentFolder(LinuxDefaults.Phys_DbLoc)
        return GetDatabase(LinuxDefaults.Phys_DbLoc)
    else:
        Log.Debug("Platform Not Supported")
    return None

def VerifyDatabase(CONN):
    Log.Debug("Verifying Database Structure")
    checkStruct = True  
    updateVersion = False  
    dbVersion = -1.0

    for db in DBDefaults.Db_List:
        returned = Database.Select(CONN,
            SELECT = "name",
            FROM = "sqlite_master",
            WHERE = "type='table' AND name='%s'" % db)

        checkStruct = returned != None and checkStruct

        if(db == DBDefaults.Db_YourFlix and checkStruct):
            versionReturned = Database.Select(CONN,
                SELECT = "Version",
                FROM = db)
            if(versionReturned):
                dbVersion = versionReturned[0]
                updateVersion = dbVersion != DBDefaults.Db_Version
    
    if(not checkStruct):
        Log.Debug("Database is Missing Data, Dropping All Tables and Rebuilding")
        Build.BuildDatabase(CONN)

    elif (updateVersion):
        Log.Debug("Database Needs and Update")
        Update.UpdateDatabase(CONN, dbVersion)
    else:
        Log.Debug("Database is setup Correctly")

def GetDatabase(DBLOC):
    conn = sqlite3.connect(DBLOC)
    Log.Debug("Loaded Database @ %s" % DBLOC)
    VerifyDatabase(conn)
    return conn

def CommitDatabase(CONN):
    conn.commit()

def CloseDatabase(CONN):
    conn.close()

if __name__ == '__main__':
    LoadDatabase()