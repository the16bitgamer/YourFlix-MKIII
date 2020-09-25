#! /usr/bin/env python
import os
import yf_Database as dbManager
import yf_DbHandler as Database

debug = False

def DebugLog(MESSAGE):
    if(debug):
        print("ProgramBuilder - %s" % MESSAGE)

def GetPhotoType(DB_CONN, PATH):
    _search = None
    
    if os.path.isfile(PATH):
        _split = os.path.splitext(PATH)
        _search = (_split[len(_split)-1]).lower()
        
    if(_search != None):
        _searchResult = Database.Select(DB_CONN,
            SELECT = 'FileType_Id',
            FROM = dbManager.Db_File,
            WHERE = 'FileType = "%s" AND FileType_Extention = "%s"' % (dbManager.ImageType, _search))

        if _searchResult:
            return _searchResult[0]

    return -1

def GetImageType(DB_CONN, IMG_TYPE):
    _searchResult = Database.Select(DB_CONN, 
        SELECT = 'ImgType_Id',
        FROM = dbManager.Db_ImageType,
        WHERE = 'Image_Type == "%s"' % IMG_TYPE)

    if _searchResult:
        return _searchResult[0]

    return -1

def AddToDefaultChannel(DB_CONN, PROGRAM_ID, NUMBER_OF_CONTENT, ALL_CHANNEL_ID, FILM_CHANNEL_ID, SHOW_CHANNEL_ID):
    
    #Add Program to All Channel
    _channelResult = Database.Select(DB_CONN,
        SELECT = 'ChProg_Id, Channel_Id, Program_Id',
        FROM = dbManager.Db_ChProgram,
        WHERE = 'Program_Id = %i AND Channel_Id = %i' % (PROGRAM_ID, ALL_CHANNEL_ID))

    if(_channelResult):
        dbManager.Current_AllChannel.remove(_channelResult)
    else:
        Database.Insert(DB_CONN, 
            INTO = dbManager.Db_ChProgram, 
            ROW = ['Channel_Id, Program_Id'],
            VALUES = [ALL_CHANNEL_ID, PROGRAM_ID])

    #Add Program to Film Channel
    if(NUMBER_OF_CONTENT == 1):
        _channelResult = Database.Select(DB_CONN,
            SELECT = 'ChProg_Id, Channel_Id, Program_Id',
            FROM = dbManager.Db_ChProgram,
            WHERE = 'Program_Id = %i AND Channel_Id = %i' % (PROGRAM_ID, FILM_CHANNEL_ID))

        if(_channelResult):
            dbManager.Current_FilmsChannel.remove(_channelResult)
        else:
            Database.Insert(DB_CONN, 
                INTO = dbManager.Db_ChProgram, 
                ROW = ['Channel_Id, Program_Id'],
                VALUES = [FILM_CHANNEL_ID, PROGRAM_ID])
    #Add Program to Show Channel
    elif(NUMBER_OF_CONTENT > 1):
        _channelResult = Database.Select(DB_CONN,
            SELECT = 'ChProg_Id, Channel_Id, Program_Id',
            FROM = dbManager.Db_ChProgram,
            WHERE = 'Program_Id = %i AND Channel_Id = %i' % (PROGRAM_ID, SHOW_CHANNEL_ID))

        if(_channelResult):
            dbManager.Current_ShowsChannel.remove(_channelResult)
        else:
            Database.Insert(DB_CONN, 
                INTO = dbManager.Db_ChProgram, 
                ROW = ['Channel_Id, Program_Id'],
                VALUES = [SHOW_CHANNEL_ID, PROGRAM_ID])

def ScanProgramMetaFolder(DB_CONN, PROGRAM_ID, PROGRAM_LOC, PROGRAM_WEB_LOC):
    _programMetaLoc = os.path.join(PROGRAM_LOC, dbManager.MetaFolder)
    _programWebLoc = os.path.join(PROGRAM_WEB_LOC, dbManager.MetaFolder)
    
    DebugLog("Scanning %s for MetaData" % _programMetaLoc)

    if(os.path.exists(_programMetaLoc)):
        for _item in os.listdir(_programMetaLoc):
            DebugLog("Found Meta Data %s" % _item)

            _physicalLoc = os.path.join(_programMetaLoc, _item)
            _webLoc = os.path.join(_programWebLoc, _item)
            _fileType = GetPhotoType(DB_CONN, _physicalLoc)
            _imageType = GetImageType(DB_CONN, "Default")

            if(_fileType != -1):
                _searchResult = Database.Select(DB_CONN,
                    SELECT = 'ProgImg_Id',
                    FROM = dbManager.Db_Img,
                    WHERE = 'Img_Location = "%s"' % _webLoc)

                if(_searchResult):
                    DebugLog("%s Exists in Database" % (_item))
                    dbManager.Current_MetaImages.remove(_searchResult)
                
                else:
                    DebugLog("%s is being added to Database" % (_item))
                    Database.Insert(DB_CONN,
                        INTO = dbManager.Db_Img,
                        ROW = ['Program_Id', 'Image_Type', 'File_Type', 'Img_Location'],
                        VALUES = [PROGRAM_ID, _imageType, _fileType, _webLoc])
    else:
        DebugLog("Meta Data Folder Does not Exist for Program with ID = %i" % PROGRAM_ID)

def ProgramFirstContentScanner(DB_CONN, PROGRAM_ID, PROGRAM_WEB_LOC):
    _folderId = -1
    _contentId = -1

    _folderSearch = Database.Select(DB_CONN,
        SELECT = 'Folder_Id',
        FROM = dbManager.Db_ContFolder,
        WHERE = 'Program_Id = %i AND Folder_Location = "%s"' % (PROGRAM_ID, PROGRAM_WEB_LOC))

    if(not _folderSearch):
        _folderSearch = Database.Select(DB_CONN,
            SELECT = 'Folder_Id',
            FROM = dbManager.Db_ContFolder,
            WHERE = 'Program_Id = %i' % PROGRAM_ID,
            ORDERBY = '%s.Folder_Name COLLATE NOCASE ASC' % dbManager.Db_ContFolder)
    
    if(_folderSearch):
        _folderId = _folderSearch[0]
        _contentSearch = Database.Select(DB_CONN,
            SELECT = 'Content_Id',
            FROM = dbManager.Db_Content,
            WHERE = 'Folder_Id = %i' % _folderId,
            ORDERBY = '%s.Content_Name COLLATE NOCASE ASC' % dbManager.Db_Content)
    
        if(_contentSearch):
            _contentId = _contentSearch[0]

    Database.Update(DB_CONN, 
        dbManager.Db_Program, 
        SET = 'First_Content = %i, First_Folder = %i' % (_folderId, _contentId),
        WHERE = 'Program_Id = %i' % PROGRAM_ID)

def PullAllChannelPrograms(DB_CONN, ALL_CHANNEL_ID, FILM_CHANNEL_ID, SHOW_CHANNEL_ID, PROGRAM_ID = None):
    _programContition = ''

    if(PROGRAM_ID):
        _programContition = 'AND Program_Id = %i' % PROGRAM_ID

    dbManager.Current_AllChannel = Database.Select(DB_CONN,
        SELECT = 'ChProg_Id, Channel_Id, Program_Id',
        FROM = dbManager.Db_ChProgram,
        WHERE = 'Channel_Id = %i %s' % (ALL_CHANNEL_ID, _programContition),
        fetchall = True)

    dbManager.Current_FilmsChannel = Database.Select(DB_CONN,
        SELECT = 'ChProg_Id, Channel_Id, Program_Id',
        FROM = dbManager.Db_ChProgram,
        WHERE = 'Channel_Id = %i %s' % (FILM_CHANNEL_ID, _programContition),
        fetchall = True)

    dbManager.Current_ShowsChannel = Database.Select(DB_CONN,
        SELECT = 'ChProg_Id, Channel_Id, Program_Id',
        FROM = dbManager.Db_ChProgram,
        WHERE = 'Channel_Id = %i %s' % (SHOW_CHANNEL_ID, _programContition),
        fetchall = True)

def RemoveUnusedChannelPrograms(DB_CONN):
    
    for allRemaining in dbManager.Current_AllChannel:
        _chProgId = allRemaining[0]

        Database.Delete(DB_CONN,
            FROM = dbManager.Db_ChProgram,
            WHERE = "ChProg_Id = %i" % _chProgId)

    for allRemaining in dbManager.Current_FilmsChannel:
        _chProgId = allRemaining[0]
        
        Database.Delete(DB_CONN,
            FROM = dbManager.Db_ChProgram,
            WHERE = "ChProg_Id = %i" % _chProgId)

    for allRemaining in dbManager.Current_ShowsChannel:
        _chProgId = allRemaining[0]
        
        Database.Delete(DB_CONN,
            FROM = dbManager.Db_ChProgram,
            WHERE = "ChProg_Id = %i" % _chProgId)

def PullAllMetaData(DB_CONN):
    dbManager.Current_MetaImages = Database.Select(DB_CONN,
        SELECT = 'ProgImg_Id',
        FROM = dbManager.Db_Img,
        fetchall = True)

def RemoveUnusedMetaData(DB_CONN):
    for allRemaining in dbManager.Current_MetaImages:
        _metaId = allRemaining[0]

        Database.Delete(DB_CONN,
            FROM = dbManager.Db_Img,
            WHERE = "ProgImg_Id = %i" % _metaId)

def BuildProgram(DB_CONN, PROGRAM_ID):
    _programData = Database.Select(DB_CONN,
        SELECT = 'Program_Id, Program_Web_Location, Program_Location, Num_Content',
        FROM = dbManager.Db_Program,
        WHERE = 'Num_Content >= 1 AND Program_Id = %i' % PROGRAM_ID)

    _allChannelId = Database.Select(DB_CONN,
        SELECT = 'Channel_Id',
        FROM = dbManager.Db_Channel,
        WHERE = 'Channel_Name = "%s"' % dbManager.DefaultChannels[0])[0]
    
    _filmChannelId = Database.Select(DB_CONN,
        SELECT = 'Channel_Id',
        FROM = dbManager.Db_Channel,
        WHERE = 'Channel_Name = "%s"' % dbManager.DefaultChannels[1])[0]
    
    _showChannelId = Database.Select(DB_CONN,
        SELECT = 'Channel_Id',
        FROM = dbManager.Db_Channel,
        WHERE = 'Channel_Name = "%s"' % dbManager.DefaultChannels[2])[0]

    PullAllMetaData(DB_CONN)
    PullAllChannelPrograms(DB_CONN, _allChannelId, _filmChannelId, _showChannelId, PROGRAM_ID)

    if(_programData):
        _programId = _programData[0]
        _programWeb = _programData[1]
        _programLoc = _programData[2]
        _numContent = _programData[3]

        ScanProgramMetaFolder(DB_CONN, _programId, _programLoc, _programWeb)
        ProgramFirstContentScanner(DB_CONN, _programId, _programWeb)
        AddToDefaultChannel(DB_CONN, _programId, _numContent, _allChannelId, _filmChannelId, _showChannelId)
    
    RemoveUnusedMetaData(DB_CONN)
    RemoveUnusedChannelPrograms(DB_CONN)

def BuildPrograms(DB_CONN):
    _programData = Database.Select(DB_CONN,
        SELECT = 'Program_Id, Program_Web_Location, Program_Location, Num_Content',
        FROM = dbManager.Db_Program,
        WHERE = 'Num_Content >= 1',
        fetchall = True)

    _allChannelId = Database.Select(DB_CONN,
        SELECT = 'Channel_Id',
        FROM = dbManager.Db_Channel,
        WHERE = 'Channel_Name = "%s"' % dbManager.DefaultChannels[0])[0]
    
    _filmChannelId = Database.Select(DB_CONN,
        SELECT = 'Channel_Id',
        FROM = dbManager.Db_Channel,
        WHERE = 'Channel_Name = "%s"' % dbManager.DefaultChannels[1])[0]
    
    _showChannelId = Database.Select(DB_CONN,
        SELECT = 'Channel_Id',
        FROM = dbManager.Db_Channel,
        WHERE = 'Channel_Name = "%s"' % dbManager.DefaultChannels[2])[0]

    PullAllMetaData(DB_CONN)
    PullAllChannelPrograms(DB_CONN, _allChannelId, _filmChannelId, _showChannelId)

    for _program in _programData:
        _programId = _program[0]
        _programWeb = _program[1]
        _programLoc = _program[2]
        _numContent = _program[3]

        ScanProgramMetaFolder(DB_CONN, _programId, _programLoc, _programWeb)
        ProgramFirstContentScanner(DB_CONN, _programId, _programWeb)
        AddToDefaultChannel(DB_CONN, _programId, _numContent, _allChannelId, _filmChannelId, _showChannelId)
    
    RemoveUnusedMetaData(DB_CONN)
    RemoveUnusedChannelPrograms(DB_CONN)