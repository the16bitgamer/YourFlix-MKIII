#! /usr/bin/env python
from subprocess import call
import inotify.adapters
import xml.etree.ElementTree as Xml
import os
import sqlite3
import yf_DbHandler as Database
import time
import sys

Yf_Config = '/etc/yourflix/yourflix.config'

Yf_DbLoc = '/usr/share/yourflix/yourflix.db'
YF_Html = "/var/www/html"
Yf_Dir = "Videos"

Db_Img = 'Img_Db'
Db_Content = 'Content_Db'
Db_Program = 'Program_Db'
Db_YourFlix = 'YourFlix_Db'
Db_File = 'FileType_Db'

Db_List = [Db_Img, Db_Content, Db_Program, Db_YourFlix, Db_File]

Db_Version = 1.0

global SupportedVideos
global SupportedImg
global FileTypes
global ScannerIgnore
global MetaFolder
SupportedVideos = ['MP4']
SupportedImg = ['PNG']
FileTypes = ['Folder']
ScannerIgnore = ['$RECYCLE.BIN', '.YF-IMG', '.YF-META', 'System Volume Information']
MetaFolder = ".YF-META"

global CurrentPrograms
global CurrentContent
global CurrentImg
global CurrentFileType
CurrentPrograms = None
CurrentContent = None
CurrentImg = None
CurrentFileType = None

def LoadConfig():
    global Yf_DbLoc
    global YF_Html
    global Yf_Dir
    global SupportedVideos
    global SupportedImg
    global FileTypes
    _config = Xml.parse(Yf_Config).getroot()
    Yf_DbLoc = _config.find("Database").attrib["location"]
    YF_Html = _config.find("WebRoot").attrib["location"]
    Yf_Dir = _config.find("VideoRoot").attrib["location"]
    localFiles = _config.find("FileTypes")
    SupportedVideos = localFiles.find("Video").attrib["types"].split(',')
    SupportedImg = localFiles.find("Image").attrib["types"].split(',')
    FileTypes = FileTypes + SupportedVideos + SupportedImg

def GetFileType(PATH):
    _search = None
    if os.path.isdir(PATH):  
        _search = FileTypes[0]
    elif os.path.isfile(PATH):
        _split = os.path.splitext(PATH)
        _search = (_split[len(_split)-1][1:]).upper()
        
    if(CurrentFileType):
        _searchResult = list(filter(lambda x:_search in x, CurrentFileType))
        if _searchResult:
            return _searchResult[0][0]
    else:
        raise Exception("ERROR: COULDN'T PULL FROM FILETYPE_DB ")
    
    return -1

def CleanDb():
    print("Not Done Yet")

def GetRoot(PHYSICAL_LOC):
    return os.path.dirname(PHYSICAL_LOC)

def IsYourFlixProgram(PROGRAM_LOC):
    if(GetRoot(PROGRAM_LOC) == os.path.join(YF_Html,Yf_Dir)):
        for root, dirs, files in os.walk(PROGRAM_LOC, followlinks=True):
            for name in dirs:
                if(name == MetaFolder):
                    return True
            for name in files:
                _split = os.path.splitext(name)
                _search = (_split[len(_split)-1][1:]).upper()
                if(_search in SupportedVideos):
                    os.mkdir(os.path.join(PROGRAM_LOC,MetaFolder))
                    print("Created Meta Folder for %s" % PROGRAM_LOC)
                    return True
    return 0

def SearchDb(DB_CONN, DATABASE, CONTENT, CONDITION):
    return Database.Select(DB_CONN, SELECT = CONTENT, FROM = DATABASE, WHERE = CONDITION, fetchall = True)

def SearchProgram(DB_CONN, PHYSICAL_ROOT, WEB_ROOT, PARENT_ID, META_DATA = False):
    for item in os.listdir(PHYSICAL_ROOT):
        _physicalLoc = os.path.join(PHYSICAL_ROOT,item)
        _fileType = GetFileType(_physicalLoc)
        if(item not in ScannerIgnore and _fileType > 0):
            _scanLoc = os.path.join(WEB_ROOT,item)
            
            if IsYourFlixProgram(_physicalLoc):
                _searchResult = SearchDb(DB_CONN, Db_Content, "Id, Parent_Id, Location", 'Location == "%s"' % _scanLoc)
                _newProgram = False
                if(not _searchResult):
                    _currProgId = Database.Insert(DB_CONN, INTO = Db_Content, ROW = ["Parent_Id", "File_Type", "Name", "Location"], VALUES = [PARENT_ID, _fileType, item, _scanLoc])
                    _newProgram = True
                else:
                    CurrentContent.remove(_searchResult[0])
                    _currProgId = _searchResult[0][0]
                
                _searchResult = SearchDb(DB_CONN, Db_Program, "Id, Folder_Id, Name", 'Name == "%s"' % item) 
                if _newProgram or not _searchResult:
                    if _searchResult:
                        Database.Delete(DB_CONN, FROM = Db_Program, WHERE = "Id = %i" % _searchResult[0][0])
                    Database.Insert(DB_CONN, INTO = Db_Program, ROW = ["Folder_Id", "Name"], VALUES = [_currProgId, item])
                elif _searchResult[0][1] == _currProgId:
                    CurrentPrograms.remove(_searchResult[0])
                else:
                    Database.Delete(DB_CONN, FROM = Db_Program, WHERE = "Id = %i" % _searchResult[0][0])
                    Database.Insert(DB_CONN, INTO = Db_Program, ROW = ["Folder_Id", "Name"], VALUES = [_currProgId, item])
            else:
                _searchResult = SearchDb(DB_CONN, Db_Content, "Id, Parent_Id, Location", 'Location == "%s"' % _scanLoc)
                if(not _searchResult):
                    _currProgId = Database.Insert(DB_CONN, INTO = Db_Content, ROW = ["Parent_Id", "File_Type", "Name", "Location"], VALUES = [PARENT_ID, _fileType, item, _scanLoc])
                else:
                    CurrentContent.remove(_searchResult[0])
                    _currProgId = _searchResult[0][0]
            
            if(os.path.isdir(_physicalLoc)):
                SearchProgram(DB_CONN, _physicalLoc, _scanLoc, _currProgId)

def CompareDirToDataBase(DB_CONN):
    _pointer = DB_CONN.cursor()
    _physicalLoc = os.path.join(YF_Html,Yf_Dir)
    _webRoot = "/"+Yf_Dir
    
    global CurrentPrograms
    global CurrentContent
    global CurrentImg
    global CurrentFileType
    
    _searchResult = SearchDb(DB_CONN, Db_Content, "Id, Parent_Id, Location", 'Location == "%s"' % _webRoot)
    if not _searchResult:
        _rootId = Database.Insert(DB_CONN, INTO = Db_Content, ROW = ["Parent_Id", "File_Type", "Name", "Location"], VALUES = [-1, GetFileType(_physicalLoc), Yf_Dir, _webRoot])
    else:
        CurrentContent.remove(_searchResult[0])
        _rootId = _searchResult[0][0]
 
    SearchProgram(DB_CONN, _physicalLoc, _webRoot, _rootId)

def PullFromDatabase(DB_CONN):
    _pointer = DB_CONN.cursor()
    global CurrentPrograms
    CurrentPrograms = Database.Select(DB_CONN, SELECT = "Id, Folder_Id, Name", FROM = Db_Program, fetchall = True)
    
    global CurrentContent
    CurrentContent = Database.Select(DB_CONN, SELECT = "Id, Parent_Id, Location", FROM = Db_Content, fetchall = True)
    
    global CurrentImg
    CurrentImg = Database.Select(DB_CONN, SELECT = "Id, Program_Id", FROM = Db_Img, fetchall = True)

    global CurrentFileType
    CurrentFileType = Database.Select(DB_CONN, SELECT = "*", FROM = Db_File, fetchall = True)
        
def BuildDatabase(DB_CONN):
    for db in Db_List:
        if(Database.Select(DB_CONN, SELECT = "name", FROM = "sqlite_master", WHERE = "type='table' AND name='%s'" % db) != None):
            Database.Drop(DB_CONN, db)
    
    #Building YourFlix Table and Setting Version
    Database.CreateTable(DB_CONN, TABLE = Db_YourFlix, VALUES = [["Version", "REAL NOT NULL"]])
    Database.Insert(DB_CONN, INTO = Db_YourFlix, VALUES = [Db_Version])
    
    #Building FileType Table and Setting Set Media Types
    Database.CreateTable(DB_CONN, TABLE = Db_File, VALUES = [["Id", "INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL"],
        ["Name", "TEXT UNIQUE NOT NULL"]])
        
    for _type in FileTypes:
        Database.Insert(DB_CONN, INTO = Db_File, ROW = ["Name"], VALUES = [_type])
    
    #Building Content Table
    Database.CreateTable(DB_CONN, TABLE = Db_Content, VALUES = [["Id", "INTEGER PRIMARY KEY AUTOINCREMENT"],
        ["Parent_Id", "INTEGER NOT NULL"],
        ["File_Type", "INTEGER NOT NULL"],
        ["Name", "TEXT NOT NULL"],
        ["Location", "TEXT UNIQUE NOT NULL"]])
    
    #Building Program Table
    Database.CreateTable(DB_CONN, TABLE = Db_Program, VALUES = [["Id", "INTEGER PRIMARY KEY AUTOINCREMENT"],
        ["Folder_Id", "INTEGER NOT NULL"],
        ["Name", "TEXT UNIQUE NOT NULL"]])
    
    #Building Image Table
    Database.CreateTable(DB_CONN, TABLE = Db_Img, VALUES = [["Id", "INTEGER PRIMARY KEY AUTOINCREMENT"],
        ["Program_Id", "INTEGER NOT NULL"],
        ["File_Type", "INTEGER NOT NULL"],
        ["Name", "TEXT NOT NULL"]])
    
def CheckDatabase(DB_CONN):
    checkStruct = True
    
    for db in Db_List:
        _returned = Database.Select(DB_CONN, SELECT = "name", FROM = "sqlite_master", WHERE = "type='table' AND name='%s'" % db)
        checkStruct = _returned != None and checkStruct
    
        if(db == Db_YourFlix and checkStruct):
            versionReturned = Database.Select(DB_CONN,SELECT = "Version",FROM = db)
            _updateVersion = versionReturned[len(versionReturned)-1] != Db_Version
    
    if(not checkStruct):
        print("Database is Missing Data, Dropping All Tables and Rebuilding")
        BuildDatabase(DB_CONN)
    elif (_updateVersion):
        print("Database Needs and Update")
    else:
        print("Database is setup Correctly")

def RemoveFromDatabase(DB_CONN):
    changed = False
    for program in CurrentPrograms:
        Database.Delete(DB_CONN, FROM = Db_Program, WHERE = "Id = %i" % program[0])
        print("Folder %s Removed from Db" % str(program))
        changed = True
    for content in CurrentContent:
        Database.Delete(DB_CONN, FROM = Db_Content, WHERE = "Id = %i" % content[0])
        print("Item %s Removed from Db" % str(content))
        changed = True
    if changed:
        print("New items added to Db")

def LoadDatabase():
    conn = sqlite3.connect(Yf_DbLoc)
    CheckDatabase(conn)
    PullFromDatabase(conn)
    CompareDirToDataBase(conn)
    RemoveFromDatabase(conn)
    conn.commit()
    conn.close()

def UpdateChildren(DB_CONN, MOVED_FROM, MOVED_TO, CONTENT_TO_UPDATE):
    for child in CONTENT_TO_UPDATE:
        _currentLoc = child[1].split(MOVED_FROM)[1][1:]
        _targetWeb = os.path.join(MOVED_TO, _currentLoc)
        Database.Update(DB_CONN, DATABASE = Db_Content, SET = 'Location="%s"' % _targetWeb, WHERE = "Id == %i" % child[0])
        _childrenToUpdate = Database.Select(DB_CONN, SELECT = "Id, Location", FROM = Db_Content, WHERE = 'Parent_Id == %i' % child[0], fetchall = True)
        
        if _childrenToUpdate:
            UpdateChildren(DB_CONN, MOVED_FROM, MOVED_TO, _childrenToUpdate)

def DeleteItemFromDatabase(DB_CONN, CONTENT_ID):
    _potentialChildren = Database.Select(DB_CONN, SELECT = "Id", FROM = Db_Content, WHERE = 'Parent_Id == "%i"' % CONTENT_ID, fetchall=True)
    if(_potentialChildren):
        for item in _potentialChildren:
            DeleteItemFromDatabase(DB_CONN, item[0])
    Database.Delete(DB_CONN, FROM = Db_Content, WHERE = "Id = %i" % CONTENT_ID)
    Database.Delete(DB_CONN, FROM = Db_Program, WHERE = "Folder_Id = %i" % CONTENT_ID)

def AddItemToDatabase(DB_CONN, ITEM_PHYSICAL_LOC,GET_PARENTS = False):
    _split = os.path.splitext(ITEM_PHYSICAL_LOC)
    _fileType = (_split[len(_split)-1][1:]).upper()
    _item = os.path.split(ITEM_PHYSICAL_LOC)
    _itemName = _item[1]
    _itemPath = _item[0]
    
    if _itemName not in ScannerIgnore and (_fileType in SupportedVideos or GET_PARENTS) and os.path.normpath(ITEM_PHYSICAL_LOC) != YF_Html:
        _webLoc = ITEM_PHYSICAL_LOC.split(YF_Html)[1]
        _itemDbId = Database.Select(DB_CONN, SELECT = "Id", FROM = Db_Content, WHERE = 'Location == "%s"' % _webLoc)
        if(_itemDbId):
            return _itemDbId[0]
        else:
            _parent_Id = AddItemToDatabase(DB_CONN, _itemPath, GET_PARENTS = True)
            _currentId = Database.Insert(DB_CONN, INTO = Db_Content, ROW = ["Parent_Id", "File_Type", "Name", "Location"], VALUES = [_parent_Id, GetFileType(ITEM_PHYSICAL_LOC), _itemName, _webLoc])
            print("NAME: %s, ID %s"%(_itemName,_currentId))
            
            if IsYourFlixProgram(ITEM_PHYSICAL_LOC):
                _searchResult = SearchDb(DB_CONN, Db_Program, "Id, Folder_Id, Name", 'Name == "%s"' % _itemName) 
                if not _searchResult:
                    Database.Insert(DB_CONN, INTO = Db_Program, ROW = ["Folder_Id", "Name"], VALUES = [_currentId, _itemName])
                else:
                    Database.Delete(DB_CONN, FROM = Db_Program, WHERE = "Id = %i" % _searchResult[0][0])
                    Database.Insert(DB_CONN, INTO = Db_Program, ROW = ["Folder_Id", "Name"], VALUES = [_currProgId, _itemName])
            return _currentId
    else:
        return -1
    
def YourflixMonitor():
    _physicalLoc = os.path.join(YF_Html,Yf_Dir)
    print("Starting Scanner")
    watcher = inotify.adapters.InotifyTree(_physicalLoc)
    print("Scanner Started")
    LoadDatabase()
    print("Database up to date")
    movedFolderFlag = False  
    movedFolderRoot = None 
    movedFolder = None  
    movedWebFolder = None    
    orphanedChild = None
    for event in watcher.event_gen():
        if event is not None:
                (header, types, path, filename) = event              
                
                #Folder Moved
                if 'IN_MOVED_FROM' in types:
                    movedFolderFlag = True
                    movedFolderRoot = path
                    movedFolder = os.path.join(path, filename)
                    movedWebFolder = os.path.join(path.split(YF_Html)[1], filename)
                else:
                    conn = sqlite3.connect(Yf_DbLoc)
                    if 'IN_MOVED_TO' in types and movedFolderFlag and movedFolderRoot == path:
                        _target = os.path.join(path, filename)
                        _targetWeb = os.path.join(path.split(YF_Html)[1], filename)
                        _contentId = Database.Select(conn, SELECT = "Id", FROM = Db_Content, WHERE = 'Location == "%s"' % movedWebFolder)[0]
                        Database.Update(conn, DATABASE = Db_Content, SET = 'Location="%s"' % _targetWeb, WHERE = "Id == %i" % _contentId)
                        if os.path.isdir(_target):  
                            if(IsYourFlixProgram(_target)):
                                Database.Update(conn, DATABASE = Db_Program, SET = 'Name="%s"' % filename,WHERE = "Folder_Id == %i" % _contentId)
                            _childrenToUpdate = Database.Select(conn, SELECT = "Id, Location", FROM = Db_Content, WHERE = 'Parent_Id == "%i"' % _contentId, fetchall = True)
                            UpdateChildren(conn, movedWebFolder, _targetWeb, _childrenToUpdate)
                        movedFolderFlag = False  
                        movedFolderRoot = None 
                        movedFolder = None  
                        movedWebFolder = None
                    
                    #File/Folder Created/Changed
                    if 'IN_CREATE' in types:
                        _createdItem = os.path.join(path, filename)
                        AddItemToDatabase(conn, _createdItem)
                    
                    if 'IN_DELETE' in types:
                        _removedWebItem = os.path.join(path.split(YF_Html)[1], filename)
                        _contentId = Database.Select(conn, SELECT = "Id", FROM = Db_Content, WHERE = 'Location == "%s"' % _removedWebItem)
                        if(_contentId):
                            DeleteItemFromDatabase(conn, _contentId[0])
                    conn.commit()
                    conn.close()
        pass

if __name__ == '__main__':
    args = (sys.argv[1:])
    LoadConfig()
    if(args):
        if(args[0] == "scan"):
            LoadDatabase()
        else:
            YourflixMonitor()
    else:
        YourflixMonitor()