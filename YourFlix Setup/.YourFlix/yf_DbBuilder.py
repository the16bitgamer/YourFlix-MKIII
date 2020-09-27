#! /usr/bin/env python
import yf_DbHandler as Database
import yf_Database as dbManager

def UpdateDatabase(DB_CONN, DB_VERSION):
    if(DB_VERSION < 1):
        BuildDatabase(DB_CONN)
        DB_VERSION = dbManager.Db_Version
        
    if(DB_VERSION < 1.11):
        Database.AlterTable(DB_CONN,
            TABLE = dbManager.Db_Img,
            RENAMECOLUMN = "Location TO Img_Location")

    if(DB_VERSION < 1.12):
        #SQLite doesn't support Drop Column while altering a table or Insert into a table. this is how we change a db if we need to remove a column
        Database.CreateTable(DB_CONN,
        TABLE = 'TEMP_DB',
        VALUES = [["Program_Id", "INTEGER PRIMARY KEY AUTOINCREMENT"],
            ["Program_Name", "TEXT UNIQUE NOT NULL"],
            ["Program_Desctiption", "TEXT"],
            ["Program_Location", "TEXT NOT NULL"],
            ["Program_Web_Location", "TEXT NOT NULL"],
            ["First_Content", "INTEGER"],
            ["First_Folder", "INTEGER"],
            ["Num_Content", "INTEGER NOT NULL"]])

        Database.Insert(DB_CONN,
            INTO = 'TEMP_DB',
            SELECT = 'Program_Id, Program_Name, Program_Desctiption, Program_Location, Program_Web_Location, First_Content, First_Folder, Num_Content',
            FROM = dbManager.Db_Program)
        
        Database.Drop(DB_CONN, dbManager.Db_Program)

        Database.CreateTable(DB_CONN,
        TABLE = dbManager.Db_Program,
        VALUES = [["Program_Id", "INTEGER PRIMARY KEY AUTOINCREMENT"],
            ["Program_Name", "TEXT UNIQUE NOT NULL"],
            ["Program_Desctiption", "TEXT"],
            ["Program_Location", "TEXT NOT NULL"],
            ["Program_Web_Location", "TEXT NOT NULL"],
            ["First_Content", "INTEGER"],
            ["First_Folder", "INTEGER"],
            ["Num_Content", "INTEGER NOT NULL"]])
        
        Database.Insert(DB_CONN,        
            INTO = dbManager.Db_Program,
            SELECT = '*',
            FROM = 'TEMP_DB')

        Database.Drop(DB_CONN, 'TEMP_DB')
    
    Database.Update(DB_CONN,
        dbManager.Db_YourFlix,
        SET = "Version = %s" % str(dbManager.Db_Version))

def BuildDatabase(DB_CONN):
    #Checks to see if Database exists and if it does drop it
    listOfDb = dbManager.Db_Old + dbManager.Db_List

    for db in listOfDb:
        if(Database.Select(DB_CONN, SELECT = "name", FROM = "sqlite_master", WHERE = "type='table' AND name='%s'" % db) != None):
            Database.Drop(DB_CONN, db)
    
    #Building YourFlix Table and Setting Version
    Database.CreateTable(DB_CONN,
        TABLE = dbManager.Db_YourFlix,
        VALUES = [["Version", "REAL NOT NULL"]])

    Database.Insert(DB_CONN,
        INTO = dbManager.Db_YourFlix,
        VALUES = [dbManager.Db_Version])
    
    #Building Channel Table
    Database.CreateTable(DB_CONN,
        TABLE = dbManager.Db_Channel,
        VALUES = [["Channel_Id", "INTEGER PRIMARY KEY AUTOINCREMENT"],
            ["Channel_Name", "TEXT UNIQUE NOT NULL"],
            ["Channel_Desctiption", "TEXT"]])    
    
    for _channelName in dbManager.DefaultChannels:
        Database.Insert(DB_CONN,
            INTO = dbManager.Db_Channel,
            ROW = ["Channel_Name"],
            VALUES = [_channelName])

    #Building Channel Program Table
    Database.CreateTable(DB_CONN,
        TABLE = dbManager.Db_ChProgram,
        VALUES = [["ChProg_Id", "INTEGER PRIMARY KEY AUTOINCREMENT"],
            ["Channel_Id", "INTEGER"],
            ["Program_Id", "INTEGER"]])

    #Building Program Table
    Database.CreateTable(DB_CONN,
        TABLE = dbManager.Db_Program,
        VALUES = [["Program_Id", "INTEGER PRIMARY KEY AUTOINCREMENT"],
            ["Program_Name", "TEXT UNIQUE NOT NULL"],
            ["Program_Desctiption", "TEXT"],
            ["Program_Location", "TEXT NOT NULL"],
            ["Program_Web_Location", "TEXT NOT NULL"],
            ["First_Content", "INTEGER"],
            ["First_Folder", "INTEGER"],
            ["Num_Content", "INTEGER NOT NULL"]])

    #Building Program Image Table
    Database.CreateTable(DB_CONN,
        TABLE = dbManager.Db_Img,
        VALUES = [["ProgImg_Id", "INTEGER PRIMARY KEY AUTOINCREMENT"],
            ["Program_Id", "INTEGER NOT NULL"],
            ["Image_Type", "INTEGER NOT NULL"],
            ["File_Type", "INTEGER NOT NULL"],
            ["Img_Location", "TEXT UNIQUE NOT NULL"]])

    #Building Image Type Table
    Database.CreateTable(DB_CONN,
        TABLE = dbManager.Db_ImageType,
        VALUES = [["ImgType_Id", "INTEGER PRIMARY KEY AUTOINCREMENT"],
            ["Image_Type", "TEXT UNIQUE NOT NULL"]])    

    Database.Insert(DB_CONN, INTO = dbManager.Db_ImageType, ROW = ["Image_Type"], VALUES = ['Default'])

    #Building FileType Table and Setting Set Media Types
    Database.CreateTable(DB_CONN,
        TABLE = dbManager.Db_File,
        VALUES = [["FileType_Id", "INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL"],
            ["FileType", "TEXT NOT NULL"],
            ["FileType_Extention", "TEXT UNIQUE NOT NULL"]])
    
    #adding Folder to DB
    Database.Insert(DB_CONN, 
        INTO = dbManager.Db_File,
        ROW = ["FileType", "FileType_Extention"],
        VALUES = [dbManager.FolderType, ''])
    
    #Adding Supported Images
    for _type in dbManager.SupportedImg:
            fileExtention = "."+_type.lower()
            Database.Insert(DB_CONN,
                INTO = dbManager.Db_File,
                ROW = ["FileType", "FileType_Extention"],
                VALUES = [dbManager.ImageType, fileExtention])
    
    #Adding Supported Videos
    for _type in dbManager.SupportedVideos:
            fileExtention = "."+_type.lower()
            Database.Insert(DB_CONN,
                INTO = dbManager.Db_File,
                ROW = ["FileType", "FileType_Extention"],
                VALUES = [dbManager.VideoType, fileExtention])
    
    #Building Program Folder Table
    Database.CreateTable(DB_CONN,
        TABLE = dbManager.Db_ContFolder,
        VALUES = [["Folder_Id", "INTEGER PRIMARY KEY AUTOINCREMENT"],
            ["Folder_Name", "TEXT NOT NULL"],
            ["Folder_Location", "TEXT NOT NULL"],
            ["Program_Id", "INTEGER NOT NULL"]])

    #Building Content Table
    Database.CreateTable(DB_CONN,
        TABLE = dbManager.Db_Content,
        VALUES = [["Content_Id", "INTEGER PRIMARY KEY AUTOINCREMENT"],
            ["Folder_Id", "INTEGER NOT NULL"],
            ["FileType_Id", "INTEGER NOT NULL"],
            ["Content_Name", "TEXT NOT NULL"],
            ["Content_Location", "TEXT UNIQUE NOT NULL"]])

def CheckDatabase(DB_CONN):
    checkStruct = True  
    _updateVersion = False  
    _dbVersion = -1.0

    #Checks to see if an DB Exists if a DB isn't present or has been updated we update or rebuild
    for db in dbManager.Db_List:
        _returned = Database.Select(DB_CONN,
            SELECT = "name",
            FROM = "sqlite_master",
            WHERE = "type='table' AND name='%s'" % db)

        checkStruct = _returned != None and checkStruct

        if(db == dbManager.Db_YourFlix and checkStruct):
            _versionReturned = Database.Select(DB_CONN,
                SELECT = "Version",
                FROM = db)
            print(_versionReturned[0])
            if(_versionReturned):
                _dbVersion = _versionReturned[0]
                _updateVersion = _dbVersion != dbManager.Db_Version
    
    if(not checkStruct):
        print("Db Builder - Database is Missing Data, Dropping All Tables and Rebuilding")
        BuildDatabase(DB_CONN)

    elif (_updateVersion):
        print("Db Builder - Database Needs and Update")
        UpdateDatabase(DB_CONN, _dbVersion)
    else:
        print("Db Builder - Database is setup Correctly")