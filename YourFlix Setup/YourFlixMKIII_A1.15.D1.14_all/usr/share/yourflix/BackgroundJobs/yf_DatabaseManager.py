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
from Resources import yf_Defaults as Defaults
from Resources import yf_DBDefaults as DBDefaults
from Database import yf_DbBuilder as Build
from Database import yf_DbUpdater as Update
from Database import yf_DbHandler as Database

def PrepareDatabase():
    conn = None
    Log.Debug("Checking Database Structure")
    FFT.VerifyParentFolder(Defaults.Phys_DbLoc)
    conn = GetDatabase(Defaults.Phys_DbLoc)

    if(conn != None):
        CommitDatabase(conn)
        CloseDatabase(conn)

def GetMountedDrives(DB_LOC):
    conn = ConnectToDatabase(DB_LOC)
    mountedDrives = Database.Select(conn,
        SELECT = "UUID, FileSystem, Mount_Loc, Is_Download_Target",
        FROM = DBDefaults.Db_Storage,
        fetchall=True)
    returnDrives = []
    for drive in mountedDrives:
        returnDrives.append(list(drive))
    return returnDrives


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
    conn = ConnectToDatabase(DBLOC)
    Log.Debug("Loaded Database @ %s" % DBLOC)
    VerifyDatabase(conn)
    return conn

def ConnectToDatabase(DB_LOC):
    if(DB_LOC != None):
        return sqlite3.connect(DB_LOC)
    else:
        Log.Debug("Database location hasn't been configured")
    return None

def CommitDatabase(CONN):
    CONN.commit()

def CloseDatabase(CONN):
    CONN.close()

if __name__ == '__main__':
    GetMountedDrives('/usr/share/yourflix/yourflix.db')