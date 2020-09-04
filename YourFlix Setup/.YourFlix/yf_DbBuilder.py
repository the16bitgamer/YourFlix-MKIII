#! /usr/bin/env python
import yf_DbHandler as Database
import yf_Database as dbManager

def BuildDatabase(DB_CONN):
    #Checks to see if Database exists and if it does drop it
    for db in Db_List:
        if(Database.Select(DB_CONN, SELECT = "name", FROM = "sqlite_master", WHERE = "type='table' AND name='%s'" % db) != None):
            Database.Drop(DB_CONN, db)
    
    #Building YourFlix Table and Setting Version
    Database.CreateTable(DB_CONN, TABLE = dbManager.Db_YourFlix, VALUES = [["Version", "REAL NOT NULL"]])
    Database.Insert(DB_CONN, INTO = dbManager.Db_YourFlix, VALUES = [dbManager.Db_Version])
    
    #Building FileType Table and Setting Set Media Types
    Database.CreateTable(DB_CONN, TABLE = dbManager.Db_File, VALUES = [["Id", "INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL"],
        ["Name", "TEXT UNIQUE NOT NULL"]])
    
    #Sets up the db File types
    for _type in FileTypes:
        Database.Insert(DB_CONN, INTO = dbManager.Db_File, ROW = ["Name"], VALUES = [_type])
    
    #Building Content Table
    Database.CreateTable(DB_CONN, TABLE = dbManager.Db_Content, VALUES = [["Id", "INTEGER PRIMARY KEY AUTOINCREMENT"],
        ["Parent_Id", "INTEGER NOT NULL"],
        ["File_Type", "INTEGER NOT NULL"],
        ["Name", "TEXT NOT NULL"],
        ["Location", "TEXT UNIQUE NOT NULL"]])
    
    #Building Program Table
    Database.CreateTable(DB_CONN, TABLE = dbManager.Db_Program, VALUES = [["Id", "INTEGER PRIMARY KEY AUTOINCREMENT"],
        ["Folder_Id", "INTEGER NOT NULL"],
        ["Name", "TEXT UNIQUE NOT NULL"]])
    
    #Building Image Table
    Database.CreateTable(DB_CONN, TABLE = dbManager.Db_Img, VALUES = [["Id", "INTEGER PRIMARY KEY AUTOINCREMENT"],
        ["Program_Id", "INTEGER NOT NULL"],
        ["File_Type", "INTEGER NOT NULL"],
        ["Name", "TEXT NOT NULL"]])

def CheckDatabase(DB_CONN):
    checkStruct = True
    
    #Checks to see if an DB Exists if a DB isn't present or has been updated we update or rebuild
    for db in dbManager.Db_List:
        _returned = Database.Select(DB_CONN, SELECT = "name", FROM = "sqlite_master", WHERE = "type='table' AND name='%s'" % db)
        checkStruct = _returned != None and checkStruct
    
        if(db == dbManager.Db_YourFlix and checkStruct):
            versionReturned = Database.Select(DB_CONN,SELECT = "Version",FROM = db)
            _updateVersion = versionReturned[len(versionReturned)-1] != dbManager.Db_Version
    
    if(not checkStruct):
        print("Database is Missing Data, Dropping All Tables and Rebuilding")
        BuildDatabase(DB_CONN)

    elif (_updateVersion):
        print("Database Needs and Update")

    else:
        print("Database is setup Correctly")