#! /usr/bin/env python
import os
import yf_Database as dbManager
import yf_DbHandler as Database
import yf_BuildContentDB as ContentManager

debug = False

def DebugLog(MESSAGE):
    if(debug):
        print("ScanToDatabase - %s" % MESSAGE)

def GetProgramId(DB_CONN, FOLDER_LOC):
    _programData = Database.Select(DB_CONN,
        SELECT = 'Program_Id',
        FROM = dbManager.Db_Program,
        WHERE = 'Program_Web_Location = "%s"' % FOLDER_LOC)

    if(_programData):
        return _programData[0]

    raise Exception("FindProgram ERROR: No Program Exists @ %s" + FOLDER_LOC)

def FindProgram(DB_CONN, ROOT, FOLDER_LOC):

    if(ROOT == "/" + dbManager.Yf_Dir):
        DebugLog("Found Program @ %s" % FOLDER_LOC)
        return GetProgramId(DB_CONN, FOLDER_LOC)

    _folderLoc = os.path.dirname(FOLDER_LOC)
    _folderName = os.path.basename(_folderLoc)
    _folderRoot = os.path.dirname(_folderLoc)

    DebugLog("ROOT: %s\nFOLDER_LOC: %s\n_folderLoc: %s\n_folderName: %s\n_folderRoot: %s\n"%(ROOT, FOLDER_LOC, _folderLoc, _folderName, _folderRoot))

    if(_folderRoot == '/'):
        raise Exception("FindProgram ERROR: No Program Exists")

    return FindProgram(DB_CONN, _folderRoot, _folderLoc)

def BuildProgramDb(DB_CONN):
    _physicalRoot = os.path.join(dbManager.YF_Html, dbManager.Yf_Dir)
    _webRoot = "/"+dbManager.Yf_Dir
        
    if(os.path.exists(_physicalRoot)):
        
        for _item in os.listdir(_physicalRoot):
            AddProgram(DB_CONN, _item, _physicalRoot, _webRoot)

def AddProgram(DB_CONN, ITEM, PHYSICAL_ROOT, WEB_ROOT):

    DebugLog("Adding Program %s to Database" %ITEM)

    _physicalLoc = os.path.join(PHYSICAL_ROOT, ITEM)
    _webLoc = os.path.join(WEB_ROOT, ITEM)

    if(ITEM not in dbManager.ScannerIgnore and os.path.isdir(_physicalLoc)):
        _programId = -1
        _searchResult = Database.Select(DB_CONN, 
            SELECT = 'Program_Id',
            FROM = dbManager.Db_Program,
            WHERE = 'Program_Location == "%s"' % _physicalLoc)

        if(_searchResult):
            _programId = _searchResult[0]
            dbManager.Current_Program.remove(_searchResult)

        else:
            _programId = Database.Insert(DB_CONN,
                INTO = dbManager.Db_Program,
                ROW = ['Program_Name', 'Program_Location', 'Program_Web_Location', 'Num_Content'],
                VALUES = [ITEM, _physicalLoc, _webLoc, 0])

        if(_programId == -1):
            raise Exception("ERROR: No Program Id Created")

        ContentManager.FindContent(DB_CONN, PHYSICAL_ROOT, WEB_ROOT, ITEM, _programId)

def AddContentFolder(DB_CONN, PHYSICAL_ROOT, WEB_ROOT, ITEM):
    _webLoc = os.path.join(WEB_ROOT, ITEM)
    _programId = FindProgram(DB_CONN, WEB_ROOT, _webLoc)
    
    ContentManager.FindContent(DB_CONN, PHYSICAL_ROOT, WEB_ROOT, ITEM, _programId)

def PullFromDatabase(DB_CONN):
    dbManager.Current_Program = Database.Select(DB_CONN, SELECT = 'Program_Id', FROM = dbManager.Db_Program, fetchall = True)
    
    dbManager.Current_ContFolder = Database.Select(DB_CONN, SELECT = 'Folder_Id, Program_Id', FROM = dbManager.Db_ContFolder, fetchall = True)
    
    dbManager.Current_Content = Database.Select(DB_CONN, SELECT = 'Content_Id, Folder_Id', FROM = dbManager.Db_Content, fetchall = True)

def RemoveFromDatabase(DB_CONN):
    changed = False
    
    for content in dbManager.Current_Content:
        print("Content %s Removed from Db" % str(content))

        _contentId = content[0]
        _folderId = content[1]
        
        _programId = Database.Select(DB_CONN,
            SELECT = 'Program_Id',
            FROM = dbManager.Db_ContFolder,
            WHERE = 'Folder_Id = %i' % _folderId)[0]

        Database.Update(DB_CONN, 
            dbManager.Db_Program, 
            SET = 'Num_Content = Num_Content - 1',
            WHERE = 'Program_Id = %i' % _programId)

        Database.Delete(DB_CONN,
            FROM = dbManager.Db_Content,
            WHERE = "Content_Id = %i" % _contentId)

        changed = True

    for contentFolder in dbManager.Current_ContFolder:
        print("Folder %s Removed from Db" % str(contentFolder))

        _folderId = contentFolder[0]

        Database.Delete(DB_CONN,
            FROM = dbManager.Db_ContFolder,
            WHERE = "Folder_Id = %i" % _folderId)
        changed = True  

    for program in dbManager.Current_Program:
        print("Program %s Removed from Db" % str(program))

        _programId = program[0]

        Database.Delete(DB_CONN,
            FROM = dbManager.Db_Program,
            WHERE = "Program_Id = %i" % _programId)

        changed = True
    
    if changed:
        print("New items added to Db")

def ScanDirToDb(DB_CONN):
    PullFromDatabase(DB_CONN)
    BuildProgramDb(DB_CONN)
    RemoveFromDatabase(DB_CONN)