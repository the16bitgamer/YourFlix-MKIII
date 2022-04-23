#! /usr/bin/env python
#Import from Parent DIR
import sys, os
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from Database import yf_DbHandler as Database
from Resources import yf_DBDefaults as dbManager

def DropExistingDatabase(CONN):
    listOfDb = dbManager.Db_Old + dbManager.Db_List

    for db in listOfDb:
        if(Database.Select(CONN, SELECT = "name", FROM = "sqlite_master", WHERE = "type='table' AND name='%s'" % db) != None):
            Database.Drop(CONN, db)

def BuildYourFlixTable(CONN):
    Database.CreateTable(CONN,
        TABLE = dbManager.Db_YourFlix,
        VALUES = [["Version", "REAL NOT NULL"]])

    Database.Insert(CONN,
        INTO = dbManager.Db_YourFlix,
        VALUES = [dbManager.Db_Version])

def BuildChannelTable(CONN):
    Database.CreateTable(CONN,
        TABLE = dbManager.Db_Channel,
        VALUES = [["Channel_Id", "INTEGER PRIMARY KEY AUTOINCREMENT"],
            ["Channel_Name", "TEXT UNIQUE NOT NULL"],
            ["Channel_Desctiption", "TEXT"]])    
    
    for _channelName in dbManager.DefaultChannels:
        Database.Insert(CONN,
            INTO = dbManager.Db_Channel,
            ROW = ["Channel_Name"],
            VALUES = [_channelName])

def BuildChannelProgramTable(CONN):
    Database.CreateTable(CONN,
        TABLE = dbManager.Db_ChProgram,
        VALUES = [["ChProg_Id", "INTEGER PRIMARY KEY AUTOINCREMENT"],
            ["Channel_Id", "INTEGER"],
            ["Program_Id", "INTEGER"]])

def BuildProgramTable(CONN):
    Database.CreateTable(CONN,
        TABLE = dbManager.Db_Program,
        VALUES = [["Program_Id", "INTEGER PRIMARY KEY AUTOINCREMENT"],
            ["Program_Name", "TEXT UNIQUE NOT NULL"],
            ["Program_Desctiption", "TEXT"],
            ["Program_Location", "TEXT NOT NULL"],
            ["Program_Web_Location", "TEXT NOT NULL"],
            ["First_Content", "INTEGER"],
            ["First_Folder", "INTEGER"],
            ["Num_Content", "INTEGER NOT NULL"],
            ["Program_Last_Updated", "DATETIME"]])

def BuildProgramImageTable(CONN):
    Database.CreateTable(CONN,
        TABLE = dbManager.Db_Img,
        VALUES = [["ProgImg_Id", "INTEGER PRIMARY KEY AUTOINCREMENT"],
            ["Program_Id", "INTEGER NOT NULL"],
            ["Image_Type", "INTEGER NOT NULL"],
            ["File_Type", "INTEGER NOT NULL"],
            ["Img_Location", "TEXT UNIQUE NOT NULL"]])

def BuildImageTypeTable(CONN):
    Database.CreateTable(CONN,
        TABLE = dbManager.Db_ImageType,
        VALUES = [["ImgType_Id", "INTEGER PRIMARY KEY AUTOINCREMENT"],
            ["Image_Type", "TEXT UNIQUE NOT NULL"]])    

    Database.Insert(CONN, INTO = dbManager.Db_ImageType, ROW = ["Image_Type"], VALUES = ['Default'])

def BuildFileTypeTable(CONN):
    Database.CreateTable(CONN,
        TABLE = dbManager.Db_File,
        VALUES = [["FileType_Id", "INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL"],
            ["FileType", "TEXT NOT NULL"],
            ["FileType_Extention", "TEXT UNIQUE NOT NULL"]])
    
    Database.Insert(CONN, 
        INTO = dbManager.Db_File,
        ROW = ["FileType", "FileType_Extention"],
        VALUES = [dbManager.FolderType, ''])
    
    for _type in dbManager.SupportedImg:
            fileExtention = "."+_type.lower()
            Database.Insert(CONN,
                INTO = dbManager.Db_File,
                ROW = ["FileType", "FileType_Extention"],
                VALUES = [dbManager.ImageType, fileExtention])
    
    for _type in dbManager.SupportedVideos:
            fileExtention = "."+_type.lower()
            Database.Insert(CONN,
                INTO = dbManager.Db_File,
                ROW = ["FileType", "FileType_Extention"],
                VALUES = [dbManager.VideoType, fileExtention])

def BuildProgramFolderTable(CONN):
    Database.CreateTable(CONN,
        TABLE = dbManager.Db_ContFolder,
        VALUES = [["Folder_Id", "INTEGER PRIMARY KEY AUTOINCREMENT"],
            ["Folder_Name", "TEXT NOT NULL"],
            ["Folder_Location", "TEXT NOT NULL"],
            ["Program_Id", "INTEGER NOT NULL"]])

def BuildContentTable(CONN):
    Database.CreateTable(CONN,
        TABLE = dbManager.Db_Content,
        VALUES = [["Content_Id", "INTEGER PRIMARY KEY AUTOINCREMENT"],
            ["Folder_Id", "INTEGER NOT NULL"],
            ["FileType_Id", "INTEGER NOT NULL"],
            ["Content_Name", "TEXT NOT NULL"],
            ["Content_Location", "TEXT UNIQUE NOT NULL"]])

def BuildDatabase(CONN):
    DropExistingDatabase(CONN)
    BuildYourFlixTable(CONN)
    BuildChannelTable(CONN)
    BuildChannelProgramTable(CONN)
    BuildProgramTable(CONN)
    BuildProgramImageTable(CONN)
    BuildImageTypeTable(CONN)
    BuildFileTypeTable(CONN)
    BuildProgramFolderTable(CONN)
    BuildContentTable(CONN)
    