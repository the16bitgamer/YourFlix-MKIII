#! /usr/bin/env python
#Import from Parent DIR
import sys, os
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from Database import yf_DbHandler as Database
from Database import yf_RenameMetaFolders as metaFolders
from Resources import yf_DBDefaults as dbManager


def V1R0(CONN):
    BuildDatabase(CONN)

def V1R11(CONN):
    Database.AlterTable(CONN,
        TABLE = dbManager.Db_Img,
        RENAMECOLUMN = "Location TO Img_Location")

def V1R12(CONN):
    #SQLite doesn't support Drop Column while altering a table or Insert into a table. this is how we change a db if we need to remove a column
    Database.CreateTable(CONN,
        TABLE = 'TEMP_DB',
        VALUES = [["Program_Id", "INTEGER PRIMARY KEY AUTOINCREMENT"],
            ["Program_Name", "TEXT UNIQUE NOT NULL"],
            ["Program_Desctiption", "TEXT"],
            ["Program_Location", "TEXT NOT NULL"],
            ["Program_Web_Location", "TEXT NOT NULL"],
            ["First_Content", "INTEGER"],
            ["First_Folder", "INTEGER"],
            ["Num_Content", "INTEGER NOT NULL"]])

    Database.Insert(CONN,
        INTO = 'TEMP_DB',
        SELECT = 'Program_Id, Program_Name, Program_Desctiption, Program_Location, Program_Web_Location, First_Content, First_Folder, Num_Content',
        FROM = dbManager.Db_Program)
        
    Database.Drop(CONN, dbManager.Db_Program)

    Database.CreateTable(CONN,
        TABLE = dbManager.Db_Program,
        VALUES = [["Program_Id", "INTEGER PRIMARY KEY AUTOINCREMENT"],
            ["Program_Name", "TEXT UNIQUE NOT NULL"],
            ["Program_Desctiption", "TEXT"],
            ["Program_Location", "TEXT NOT NULL"],
            ["Program_Web_Location", "TEXT NOT NULL"],
            ["First_Content", "INTEGER"],
            ["First_Folder", "INTEGER"],
            ["Num_Content", "INTEGER NOT NULL"]])
        
    Database.Insert(CONN,        
        INTO = dbManager.Db_Program,
        SELECT = '*',
        FROM = 'TEMP_DB')

    Database.Drop(CONN, 'TEMP_DB')

def V1R13(CONN):
    metaFolders.RenameMeta()
    Database.AlterTable(CONN,
        TABLE = dbManager.Db_Program,
        ADDCOLUMN = "Program_Last_Updated DATETIME")

def UpdateDatabase(CONN, VERSION):
    dbVersion = VERSION

    if(DB_VERSION < 1):
        V1R0(CONN)
        dbVersion = dbManager.Db_Version
    if(DB_VERSION < 1.11):
        V1R11(CONN)
    if(DB_VERSION < 1.12):
        V1R12(CONN)    
    if(DB_VERSION < 1.13):
        V1R13(CONN)

    Database.Update(CONN,
        dbManager.Db_YourFlix,
        SET = "Version = %s" % str(dbManager.Db_Version))