#! /usr/bin/env python
import os
import yf_DbHandler as Database
import yf_Database as dbManager
import yf_ProgramBuilder as programBuilder

debug = False

def AddProgramToDb(DB_CONN, PROGAM_WEB_LOC, PROGRAM_NAME):
    _programData = Database.Select(DB_CONN,
        SELECT = 'Program_Id',
        FROM = dbManager.Db_Program,
        WHERE = 'Program_Web_Location = "%s"' % PROGAM_WEB_LOC)

    if(_programData):

        if(debug):
            print("Found Program in Location: %s" % PROGAM_WEB_LOC)

        return _programData[0]

    else:
        _programName = PROGRAM_NAME
        _programWebLoc = PROGAM_WEB_LOC
        _programPhysLoc = os.path.join(dbManager.YF_Html, _programWebLoc)
        _numContent = 0

        _programId = 0

        if(debug):
            print("Adding Program %s in Location: %s" % (_programName, _programWebLoc))
        
        return _programId

def FindProgram(DB_CONN, ROOT, FOLDER_LOC, FOLDER_NAME):

    if(ROOT == dbManager.MetaFolder):
        if(debug):
            print("Found Program @ %s" % FOLDER_LOC)
        return AddProgramToDb(DB_CONN, FOLDER_LOC, FOLDER_NAME)

    _folderLoc = os.path.dirname(ROOT)
    _folderName = os.path.basename(_folderLoc)
    _folderRoot = os.path.dirname(_folderLoc)

    if(_folderRoot == ''):
        raise Exception("FindProgram ERROR: No Program Exists")

    if(debug):
        print("Program Not found going up")

    return FindProgram(DB_CONN, _folderRoot, _folderLoc, _folderName)

def AddFolderToDb(DB_CONN, ROOT, FOLDER_LOC, FOLDER_NAME):
    _folderData = Database.Select(DB_CONN,
            SELECT = 'Folder_Id',
            FROM = dbManager.Db_ContFolder,
            WHERE = 'Folder_Location = "%s"' % FOLDER_LOC)

    if(_folderData):
        _folderLoc = os.path.dirname(ROOT)
        _folderName = os.path.basename(_folderLoc)
        _folderRoot = os.path.dirname(_folderLoc)
        _programId = None

        _programData = FindProgram(DB_CONN, _folderRoot, _folderLoc, _folderRoot)

        if(_programData):
            _programId = _programData[0]

        if(_programId):
            _folderId = 0

            if(debug):
                print("Adding Folder: %s to change Location to: %s" % (FOLDER_NAME, FOLDER_LOC))

            return (_folderId, _programId)

        elif(debug):
            raise Exception("Program not found for Folder: %s in Location: %s" % (FOLDER_NAME, FOLDER_LOC))
    
    else:

        if(debug):
            print("Folder %s exists at location %s" % (FOLDER_NAME, FOLDER_LOC))

        return (_folderData[0], _folderData[1])

def AddContentToDb(DB_CONN, ROOT, FILE_LOC, FILE_NAME):
    _contentData = Database.Select(DB_CONN,
        SELECT = 'Content_Id',
        FROM = dbManager.Db_Content,
        WHERE = 'Content_Location = "%s"' % FILE_LOC)
    
    if(not _contentData):
        _folderLoc = os.path.dirname(ROOT)
        _folderName = os.path.basename(_folderLoc)
        _folderRoot = os.path.dirname(_folderLoc)
        _folderId = None
        _folderData = AddFolderToDb(DB_CONN, _folderRoot, _folderLoc, _folderName)

        if(_folderData):
            _folderId = _folderData[0]
            _programId = _folderData[1]
            _contentId = 0

            if(debug):
                print("Added Content: %s in Location: %s" % (FILE_NAME, FILE_LOC))

            #Increase Program by 1 content num
            programBuilder.BuildProgram(DB_CONN, _programId)

            if(debug):
                print("Updated and rebuilt Program with Id: %i" % (_programId))

            return _contentId

    else

        if(debug):
            print("Content: %s already exists" % (FILE_NAME))

        return _contentData[0]

def AddMetaImgToDb(DB_CONN, ROOT, FILE_LOC, FILE_NAME):
    _metaImgData = Database.Select(DB_CONN,
        SELECT = 'ProgImg_Id',
        FROM = dbManager.Db_Img,
        WHERE = 'Img_Location = "%s"' % FILE_LOC)

    if(_metaImgData):
        _folderLoc = os.path.dirname(ROOT)
        _folderName = os.path.basename(_folderLoc)
        _folderRoot = os.path.dirname(_folderLoc)

        _programId = FindProgram(DB_CONN, _folderRoot, _folderLoc, _folderName)
        _metaId = 0
        
        if(debug):
            print("Added Meta Image %s" %FILE_NAME)
        
        return _metaId
    
    else

        if(debug):
            print("MetaImg: %s already exists" % (FILE_NAME))

        return _metaImgData[0]