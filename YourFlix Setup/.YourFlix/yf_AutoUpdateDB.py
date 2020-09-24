#! /usr/bin/env python
import os
import yf_Database as dbManager
import yf_DbHandler as Database

debug = True

def UpdateProgramLocation(DB_CONN, ORIG_LOC, NEW_LOC):
    _programId = None
    _programData = Database.Select(DB_CONN,
            SELECT = 'Program_Id',
            FROM = dbManager.Db_Program,
            WHERE = 'Program_Web_Location = "%s"' % ORIG_LOC)

    if(_programData):
        _programId = _programData[0]
    
    if(_programId):
        _programFolders = Database.Select(DB_CONN,
            SELECT = 'Folder_Id, Folder_Location',
            FROM = dbManager.Db_ContFolder,
            WHERE = 'Program_Id = %i' % _programId,
            fetchall = True)
        
        for _folder in _programFolders:
            print(_folder)
            _folderId = _folder[0]
            _originalFolderLoc = _folder[1]
            _newContentLocation = os.path.join(NEW_LOC, _originalFolderLoc.split(ORIG_LOC)[1][1:])
            
            UpdateFolderLocation(DB_CONN, _originalFolderLoc, _newContentLocation, FOLDER_ID = _folderId)
        
        _programMeta = Database.Select(DB_CONN,
            SELECT = 'ProgImg_Id, Img_Location',
            FROM = dbManager.Db_Img,
            WHERE = 'Program_Id = %i' % _programId,
            fetchall = True)
        
        for _meta in _programMeta:
            _folderId = _meta[0]
            _originalMetaLoc = _meta[1]
            _newContentLocation = os.path.join(NEW_LOC, _originalMetaLoc.split(ORIG_LOC)[1][1:])
            
            UpdateProgramMetaLocation(DB_CONN, _folderId, _newContentLocation)

        if(debug):
            print("Updating Program: %i to change Location to: %s" % (_programId, NEW_LOC))
    
    elif(debug):
        print("Program missing from Location %s" % (ORIG_LOC))

def UpdateProgramMetaLocation(DB_CONN, META_ID, NEW_LOC):
    
    if(debug):
        print("Updating Program Meta: %i to change Location to: %s" % (META_ID, NEW_LOC))

def UpdateFolderLocation(DB_CONN, ORIG_LOC, NEW_LOC, FOLDER_ID = None):
    _folderId = None
    
    if(not FOLDER_ID):
        _folderData = Database.Select(DB_CONN,
            SELECT = 'Folder_Id',
            FROM = dbManager.Db_ContFolder,
            WHERE = 'Folder_Location = "%s"' % ORIG_LOC)

        if(_folderData):
            _folderId = _folderData[0]

    else:
        _folderId = FOLDER_ID
    
    if(_folderId):
        _folderContent = Database.Select(DB_CONN,
                SELECT = 'Content_Id, Content_Location',
                FROM = dbManager.Db_Content,
                WHERE = 'Folder_Id = %i' % _folderId,
                fetchall = True)

        for _content in _folderContent:
            _contentId = _content[0]
            _originalContentLoc = _content[1]
            _newContentLocation = os.path.join(NEW_LOC, _originalContentLoc.split(ORIG_LOC)[1][1:])
            
            UpdateContentLocation(DB_CONN, _contentId, _newContentLocation)

        if(debug):
            print("Updating Folder: %i to change Location to: %s" % (_folderId, NEW_LOC))
    
    elif(debug):
        print("Folder missing from Location %s" % (ORIG_LOC))

def UpdateContentLocation(DB_CONN, CONTENT_ID, NEW_LOC):
    
    if(debug):
        print("Updating Content: %i to change Location to: %s" % (CONTENT_ID, NEW_LOC))