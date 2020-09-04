#! /usr/bin/env python
import os
import xml.etree.ElementTree as Xml
import yf_Database as dbManager
import yf_DbHandler as Database

def GetFileType(PATH):
    _search = None

    if os.path.isdir(PATH):  
        _search = dbManager.FileTypes[0]

    elif os.path.isfile(PATH):
        _split = os.path.splitext(PATH)
        _search = (_split[len(_split)-1][1:]).upper()
        
    if(dbManager.CurrentFileType):
        _searchResult = list(filter(lambda x:_search in x, dbManager.CurrentFileType))

        if _searchResult:
            return _searchResult[0][0]

    else:
        raise Exception("ERROR: COULDN'T PULL FROM FILETYPE_DB ")
    
    return -1

def GetRoot(PHYSICAL_LOC):
    return os.path.dirname(PHYSICAL_LOC)

def IsYourFlixProgram(PROGRAM_LOC):

    if(GetRoot(PROGRAM_LOC) == os.path.join(dbManager.YF_Html,dbManager.Yf_Dir)):

        for root, dirs, files in os.walk(PROGRAM_LOC, followlinks=True):

            for name in dirs:

                if(name == dbManager.MetaFolder):
                    return True

            for name in files:
                _split = os.path.splitext(name)
                _search = (_split[len(_split)-1][1:]).upper()

                if(_search in dbManager.SupportedVideos):
                    os.mkdir(os.path.join(PROGRAM_LOC, dbManager.MetaFolder))
                    print("Created Meta Folder for %s" % PROGRAM_LOC)
                    return True

    return 0

def SearchDb(DB_CONN, DATABASE, CONTENT, CONDITION):
    return Database.Select(DB_CONN, SELECT = CONTENT, FROM = DATABASE, WHERE = CONDITION, fetchall = True)

def SearchProgram(DB_CONN, PHYSICAL_ROOT, WEB_ROOT, PARENT_ID, META_DATA = False):

    for item in os.listdir(PHYSICAL_ROOT):
        _physicalLoc = os.path.join(PHYSICAL_ROOT,item)
        _fileType = GetFileType(_physicalLoc)

        if(item not in dbManager.ScannerIgnore and _fileType > 0):
            _scanLoc = os.path.join(WEB_ROOT,item)
            
            if IsYourFlixProgram(_physicalLoc):
                _searchResult = SearchDb(DB_CONN, dbManager.Db_Content, "Id, Parent_Id, Location", 'Location == "%s"' % _scanLoc)
                _newProgram = False

                if(not _searchResult):
                    _currProgId = Database.Insert(DB_CONN, INTO = dbManager.Db_Content, ROW = ["Parent_Id", "File_Type", "Name", "Location"], VALUES = [PARENT_ID, _fileType, item, _scanLoc])
                    _newProgram = True

                else:
                    dbManager.CurrentContent.remove(_searchResult[0])
                    _currProgId = _searchResult[0][0]
                
                _searchResult = SearchDb(DB_CONN, dbManager.Db_Program, "Id, Folder_Id, Name", 'Name == "%s"' % item) 

                if _newProgram or not _searchResult:

                    if _searchResult:
                        Database.Delete(DB_CONN, FROM = dbManager.Db_Program, WHERE = "Id = %i" % _searchResult[0][0])

                    Database.Insert(DB_CONN, INTO = dbManager.Db_Program, ROW = ["Folder_Id", "Name"], VALUES = [_currProgId, item])

                elif _searchResult[0][1] == _currProgId:
                    dbManager.CurrentPrograms.remove(_searchResult[0])

                else:
                    Database.Delete(DB_CONN, FROM = dbManager.Db_Program, WHERE = "Id = %i" % _searchResult[0][0])
                    Database.Insert(DB_CONN, INTO = dbManager.Db_Program, ROW = ["Folder_Id", "Name"], VALUES = [_currProgId, item])

            else:
                _searchResult = SearchDb(DB_CONN, dbManager.Db_Content, "Id, Parent_Id, Location", 'Location == "%s"' % _scanLoc)

                if(not _searchResult):
                    _currProgId = Database.Insert(DB_CONN, INTO = dbManager.Db_Content, ROW = ["Parent_Id", "File_Type", "Name", "Location"], VALUES = [PARENT_ID, _fileType, item, _scanLoc])

                else:
                    dbManager.CurrentContent.remove(_searchResult[0])
                    _currProgId = _searchResult[0][0]
            
            if(os.path.isdir(_physicalLoc)):
                SearchProgram(DB_CONN, _physicalLoc, _scanLoc, _currProgId)

def CompareDirToDataBase(DB_CONN):
    _pointer = DB_CONN.cursor()
    _physicalLoc = os.path.join(dbManager.YF_Html,dbManager.Yf_Dir)
    _webRoot = "/"+dbManager.Yf_Dir
        
    _searchResult = SearchDb(DB_CONN, dbManager.Db_Content, "Id, Parent_Id, Location", 'Location == "%s"' % _webRoot)
    
    if not _searchResult:
        _rootId = Database.Insert(DB_CONN, INTO = dbManager.Db_Content, ROW = ["Parent_Id", "File_Type", "Name", "Location"], VALUES = [-1, GetFileType(_physicalLoc), dbManager.Yf_Dir, _webRoot])
    
    else:
        dbManager.CurrentContent.remove(_searchResult[0])
        _rootId = _searchResult[0][0]
 
    SearchProgram(DB_CONN, _physicalLoc, _webRoot, _rootId)

def PullFromDatabase(DB_CONN):
    _pointer = DB_CONN.cursor()
    
    dbManager.CurrentPrograms = Database.Select(DB_CONN, SELECT = "Id, Folder_Id, Name", FROM = dbManager.Db_Program, fetchall = True)
    
    dbManager.CurrentContent = Database.Select(DB_CONN, SELECT = "Id, Parent_Id, Location", FROM = dbManager.Db_Content, fetchall = True)
    
    dbManager.CurrentImg = Database.Select(DB_CONN, SELECT = "Id, Program_Id", FROM = dbManager.Db_Img, fetchall = True)

    dbManager.CurrentFileType = Database.Select(DB_CONN, SELECT = "*", FROM = dbManager.Db_File, fetchall = True)

def RemoveFromDatabase(DB_CONN):
    changed = False
    
    for program in dbManager.CurrentPrograms:
        Database.Delete(DB_CONN, FROM = dbManager.Db_Program, WHERE = "Id = %i" % program[0])
        print("Folder %s Removed from Db" % str(program))
        changed = True
    
    for content in dbManager.CurrentContent:
        Database.Delete(DB_CONN, FROM = dbManager.Db_Content, WHERE = "Id = %i" % content[0])
        print("Item %s Removed from Db" % str(content))
        changed = True
    
    if changed:
        print("New items added to Db")

def ScanDirToDb(DB_CONN):
    PullFromDatabase(DB_CONN)
    CompareDirToDataBase(DB_CONN)
    RemoveFromDatabase(DB_CONN)    