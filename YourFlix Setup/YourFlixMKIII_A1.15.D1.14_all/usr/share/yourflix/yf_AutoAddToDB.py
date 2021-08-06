#! /usr/bin/env python
import os
import datetime
import yf_DbHandler as Database
import yf_Database as dbManager
import yf_ProgramBuilder as programBuilder

debug = False

def DebugLog(MESSAGE):
    if(debug):
        print("AutoAddToDb - %s" % MESSAGE)

def GetVideoType(DB_CONN, PATH):
    _search = None
    
    _split = os.path.splitext(PATH)
    _search = (_split[len(_split)-1]).lower()
        
    if(_search != None):

        DebugLog("Looking for File Extention %s" % _search)

        _searchResult = Database.Select(DB_CONN,
            SELECT = 'FileType_Id',
            FROM = dbManager.Db_File,
            WHERE = 'FileType = "%s" AND FileType_Extention = "%s"' % (dbManager.VideoType, _search))

        if _searchResult:
            return _searchResult[0]

    return -1

def AddProgramToDb(DB_CONN, PROGAM_WEB_LOC, PROGRAM_NAME):
    _programData = Database.Select(DB_CONN,
        SELECT = 'Program_Id',
        FROM = dbManager.Db_Program,
        WHERE = 'Program_Web_Location = "%s"' % PROGAM_WEB_LOC)

    if(_programData):
        DebugLog("Found Program in Location: %s" % PROGAM_WEB_LOC)
        return _programData[0]

    else:
        DebugLog("Adding Program %s" % PROGRAM_NAME)

        _programName = PROGRAM_NAME
        _programWebLoc = PROGAM_WEB_LOC
        _programPhysLoc = os.path.join(dbManager.YF_Html, _programWebLoc[1:])

        _programId = _programId = Database.Insert(DB_CONN,
            INTO = dbManager.Db_Program,
            ROW = ['Program_Name', 'Program_Location', 'Program_Web_Location', 'Num_Content'],
            VALUES = [PROGRAM_NAME, _programPhysLoc, _programWebLoc, 0])

        DebugLog("Adding Program %s in Physical Loc: %s - Web Loc: %s" % (_programName, _programPhysLoc, _programWebLoc))
        
        return _programId

def FindProgram(DB_CONN, ROOT, FOLDER_LOC, FOLDER_NAME):

    if(ROOT == "/" + dbManager.Yf_Dir):
        DebugLog("Found Program @ %s" % FOLDER_LOC)
        return AddProgramToDb(DB_CONN, FOLDER_LOC, FOLDER_NAME)

    _folderLoc = os.path.dirname(FOLDER_LOC)
    _folderName = os.path.basename(_folderLoc)
    _folderRoot = os.path.dirname(_folderLoc)

    DebugLog("Looking for Program with root of: %s" % _folderRoot)

    if(_folderRoot == '/'):
        raise Exception("FindProgram ERROR: No Program Exists")

    return FindProgram(DB_CONN, _folderRoot, _folderLoc, _folderName)

def AddFolderToDb(DB_CONN, ROOT, FOLDER_LOC, FOLDER_NAME):
    if(FOLDER_NAME not in dbManager.ScannerIgnore):
        _folderData = Database.Select(DB_CONN,
                SELECT = 'Folder_Id, Program_Id',
                FROM = dbManager.Db_ContFolder,
                WHERE = 'Folder_Location = "%s"' % FOLDER_LOC)

        if(_folderData):
            DebugLog("Folder %s exists at location %s" % (FOLDER_NAME, FOLDER_LOC))
            return (_folderData[0], _folderData[1])
        
        elif(FOLDER_NAME not in dbManager.ScannerIgnore):
            _programId = None
            _programId = FindProgram(DB_CONN, ROOT, FOLDER_LOC, FOLDER_NAME)

            if(_programId != -1):
                _folderId = 0

                _folderId = Database.Insert(DB_CONN,
                    INTO = dbManager.Db_ContFolder,
                    ROW = ['Folder_Name', 'Folder_Location', 'Program_Id'],
                    VALUES = [FOLDER_NAME, FOLDER_LOC, _programId])

                DebugLog("Adding Folder: %s to Location: %s" % (FOLDER_NAME, FOLDER_LOC))

                return (_folderId, _programId)

            elif(debug):
                raise Exception("Program not found for Folder: %s in Location: %s" % (FOLDER_NAME, FOLDER_LOC))
        
        else:
            DebugLog("Folder %s has been ignored at location %s" % (FOLDER_NAME, FOLDER_LOC))
            return None

            
    
    DebugLog("Folder %s is being skipped" % (FOLDER_NAME))

def AddContentToDb(DB_CONN, ROOT, FILE_LOC, FILE_NAME):
    _contentData = Database.Select(DB_CONN,
        SELECT = 'Content_Id',
        FROM = dbManager.Db_Content,
        WHERE = 'Content_Location = "%s"' % FILE_LOC)
    
    if(not _contentData):
        _folderLoc = os.path.dirname(FILE_LOC)
        _folderName = os.path.basename(_folderLoc)
        _folderRoot = os.path.dirname(_folderLoc)
        _folderId = None

        DebugLog("ROOT: %s\nFOLDER_LOC: %s\n_folderLoc: %s\n_folderName: %s\n_folderRoot: %s\n"%(ROOT, FILE_LOC, _folderLoc, _folderName, _folderRoot))
        _folderData = AddFolderToDb(DB_CONN, _folderRoot, _folderLoc, _folderName)

        if(_folderData):
            _folderId = _folderData[0]
            _programId = _folderData[1]

            if(debug):
                print("Added Content: %s in Location: %s" % (FILE_NAME, FILE_LOC))

            _fileType = GetVideoType(DB_CONN, FILE_NAME)
            _split = os.path.splitext(FILE_NAME)
            _fileName = _split[0]
            _updateTime = datetime.datetime.now()

            _contentId = Database.Insert(DB_CONN,
                INTO = dbManager.Db_Content,
                ROW = ['Folder_Id', 'FileType_Id', 'Content_Name', 'Content_Location'],
                VALUES = [_folderId, _fileType, _fileName, FILE_LOC])
            Database.Update(DB_CONN, 
                dbManager.Db_Program, 
                SET = 'Num_Content = Num_Content + 1, Program_Last_Updated = "%s"' % (_updateTime),
                WHERE = 'Program_Id = %i' % _programId)

            programBuilder.BuildProgram(DB_CONN, _programId)

            DebugLog("Updated and rebuilt Program with Id: %i" % (_programId))

            return _contentId

    else:

        DebugLog("Content: %s already exists" % (FILE_NAME))

        return _contentData[0]

def AddMetaImgToDb(DB_CONN, ROOT, FILE_LOC):
    DebugLog("Adding Program Meta %s" % FILE_LOC)

    _folderLoc = os.path.dirname(ROOT)
    _folderName = os.path.basename(_folderLoc)
    _folderRoot = os.path.dirname(_folderLoc)
    _programId = FindProgram(DB_CONN, _folderRoot, _folderLoc, _folderName)
    programBuilder.BuildProgram(DB_CONN, _programId)