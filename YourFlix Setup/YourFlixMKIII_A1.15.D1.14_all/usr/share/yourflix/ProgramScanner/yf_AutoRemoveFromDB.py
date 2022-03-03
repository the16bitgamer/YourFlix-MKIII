#! /usr/bin/env python
import datetime
import yf_DbHandler as Database
import yf_Database as dbManager
import yf_ProgramBuilder as programBuilder

debug = False

def DebugLog(MESSAGE):
    print("AutoRemoveFromDB - %s" % MESSAGE)

def RemoveProgramFromDb(DB_CONN, PROGRAM_WEB_LOCATION):
    _programData = Database.Select(DB_CONN,
        SELECT = 'Program_Id',
        FROM = dbManager.Db_Program,
        WHERE = 'Program_Web_Location = "%s"' % PROGRAM_WEB_LOCATION)

    if(_programData):
        _programId = _programData[0]
        _programFolders = Database.Select(DB_CONN,
            SELECT = 'Folder_Id',
            FROM = dbManager.Db_ContFolder,
            WHERE = 'Program_Id = %i' % _programId,
            fetchall = True)
        
        if(_programFolders):
            DebugLog("%i Porgam Folders Found Removing them" % len(_programFolders)) 

            for _folder in _programFolders:
                _folderId = _folder[0]
                RemoveFolderFromDb(DB_CONN, FOLDER_ID = _folderId)

        _programMetaImg = Database.Select(DB_CONN,
            SELECT = 'ProgImg_Id',
            FROM = dbManager.Db_Img,
            WHERE = 'Program_Id = %i' % _programId,
            fetchall = True)

        if(_programMetaImg):
            DebugLog("%i Meta Images Found Removing them" % len(_programMetaImg)) 

            for _metaImg in _programMetaImg:
                _metaId = _metaImg[0]
                RemoveMetaImgFromDb(DB_CONN, META_ID = _metaId)

        _channelPrograms = Database.Select(DB_CONN,
            SELECT = 'ChProg_Id',
            FROM = dbManager.Db_ChProgram,
            WHERE = 'Program_Id = %i' % _programId,
            fetchall = True)

        if(_channelPrograms):
            DebugLog("%i Channel Programs Found Removing them" % len(_channelPrograms)) 

            for _channelProgram in _channelPrograms:
                _channelPorgramId = _channelProgram[0]

                RemoveChannelProgramFroDb(DB_CONN, _channelPorgramId)

        Database.Delete(DB_CONN,
            FROM = dbManager.Db_Program,
            WHERE = 'Program_Id = %i' % _programId)

        DebugLog("Program with ID: %i has been removed" % _programId)

    DebugLog("Program Already Removed")

def RemoveFolderFromDb(DB_CONN, FOLDER_LOCATION = None, FOLDER_ID = None):
    _folderId = FOLDER_ID

    if(not _folderId):
        _folderData = Database.Select(DB_CONN,
            SELECT = 'Folder_Id',
            FROM = dbManager.Db_ContFolder,
            WHERE = 'Folder_Location = "%s"' % FOLDER_LOCATION)
        
        if(_folderData):
            _folderId = _folderData[0]
    
    if(_folderId):
        _folderContents = Database.Select(DB_CONN,
            SELECT = 'Content_Id',
            FROM = dbManager.Db_Content,
            WHERE = 'Folder_id = %i' % _folderId,
            fetchall = True)

        if(_folderContents):
            
            for _content in _folderContents:
                _contentId = _content[0]
                RemoveContentFromDb(DB_CONN, CONTENT_ID = _contentId, FOLDER_ID = _folderId)
                
        Database.Delete(DB_CONN,
            FROM = dbManager.Db_ContFolder,
            WHERE = 'Folder_Id = %i' % _folderId)
    
    else:
        DebugLog("Folder Already Removed")

def RemoveContentFromDb(DB_CONN, FILE_LOCATION = None, CONTENT_ID = None, FOLDER_ID = None):
    _contentId = CONTENT_ID
    _folderId = FOLDER_ID
    
    if(not _contentId):
        _contentData = Database.Select(DB_CONN,
            SELECT = 'Content_Id, Folder_Id',
            FROM = dbManager.Db_Content,
            WHERE = 'Content_Location = "%s"' % FILE_LOCATION)

        if(_contentData):
            _contentId = _contentData[0]
            _folderId = _contentData[1]
    
    if(_contentId and _folderId):
        Database.Delete(DB_CONN,
            FROM = dbManager.Db_Content,
            WHERE = 'Content_Id = %i' % _contentId)
        DebugLog("Content with ID: %i has been Removed" % _contentId)
        
        _contentData = Database.Select(DB_CONN,
            SELECT = 'Content_Id, Folder_Id',
            FROM = dbManager.Db_Content,
            WHERE = 'Content_Id = %i' % _contentId,
            fetchall = True)

        if(len(_contentData) >= 1):
            RemoveFolderFromDb(DB_CONN, FOLDER_ID = _folderId)

        _programData = Database.Select(DB_CONN,
            SELECT = 'Program_Id',
            FROM = dbManager.Db_ContFolder,
            WHERE = 'Folder_Id = %i' % _folderId)
            
        if(_programData):
            _programId = _programData[0]
            _updateTime = datetime.datetime.now()

            Database.Update(DB_CONN, 
                dbManager.Db_Program, 
                SET = 'Num_Content = Num_Content - 1, Program_Last_Updated = "%s"' % (_updateTime),
                WHERE = 'Program_Id = %i' % _programId)

            DebugLog("Program with ID: %i is one less Content in it's DB" % _programId)

            programBuilder.BuildProgram(DB_CONN, _programId)

    else:
        DebugLog("Content Already Removed\nContent ID: %s\nFolder ID: %s" % (str(_contentId), str(_folderId)))

def RemoveChannelProgramFroDb(DB_CONN, CHANNEL_ID):
    if(CHANNEL_ID):
        Database.Delete(DB_CONN,
            FROM = dbManager.Db_ChProgram,
            WHERE = 'ChProg_Id = %i' % CHANNEL_ID)

        DebugLog("Channel Program with ID: %i has been removed" % CHANNEL_ID)
    else:
        DebugLog("Channel Program Removal Error, No ChannelProgram with ID %s" % str(CHANNEL_ID))

def RemoveMetaImgFromDb(DB_CONN, FILE_LOCATION = None, META_ID = None):
    _metaImgData = META_ID

    if(not _metaImgData):
        _metaImgData = Database.Select(DB_CONN,
            SELECT = 'ProgImg_Id',
            FROM = dbManager.Db_Img,
            WHERE = 'Img_Location = "%s"' % FILE_LOCATION)
        
        if(_metaImgData):
            _programId = _metaImgData[0]

    if(_metaImgData):
        Database.Delete(DB_CONN,
            FROM = dbManager.Db_Img,
            WHERE = 'ProgImg_Id = %i' % _metaImgData)

        DebugLog("Meta with ID: %i has been removed" % _metaImgData)
    
    else:
        DebugLog("MetaImg Removal Error, No Meta with ID %s" % str(_metaImgData))