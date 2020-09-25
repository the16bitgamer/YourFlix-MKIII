#! /usr/bin/env python
import os
import yf_DbHandler as Database
import yf_Database as dbManager

debug = False

def DebugLog(MESSAGE):
    if(debug):
        print("BuildContentDb - %s" % MESSAGE)

def GetVideoType(DB_CONN, PATH):
    _search = None

    if os.path.isfile(PATH):
        _split = os.path.splitext(PATH)
        _search = (_split[len(_split)-1]).lower()
        
    if(_search != None):
        _searchResult = Database.Select(DB_CONN,
            SELECT = 'FileType_Id',
            FROM = dbManager.Db_File,
            WHERE = 'FileType = "%s" AND FileType_Extention = "%s"' % (dbManager.VideoType, _search))

        if _searchResult:
            return _searchResult[0]

    return -1

#Scans a Directory for all of it's valid content
def FindContent(DB_CONN, PHYSICAL_ROOT, WEB_ROOT, FOLDER_NAME, PROGRAM_ID):
    _currentPhysicalFolder = os.path.join(PHYSICAL_ROOT, FOLDER_NAME)
    _foundOrAddedContent = 0
    
    if os.path.isdir(_currentPhysicalFolder):
        DebugLog("Checking DIR %s" % _currentPhysicalFolder)

        _currentWebFolder = os.path.join(WEB_ROOT, FOLDER_NAME)
        _currentFolderId = -1

        for _item in os.listdir(_currentPhysicalFolder):
            DebugLog("Found %s" % _item)

            if(_item not in dbManager.ScannerIgnore):
                _physicalContent = os.path.join(_currentPhysicalFolder, _item)
                _webContent = os.path.join(_currentWebFolder, _item)

                if(os.path.isdir(_physicalContent)):
                    _foundOrAddedContent += FindContent(DB_CONN, _currentPhysicalFolder, _currentWebFolder, _item, PROGRAM_ID)

                else:

                    #Make Sure it has the same select data as the Pull data
                    _searchResult = Database.Select(DB_CONN,
                        SELECT = 'Content_Id, Folder_Id',
                        FROM = dbManager.Db_Content,
                        WHERE = 'Content_Location == "%s"' % _webContent)
                    
                    if(_currentFolderId == -1):
                        _currentFolderId = FindFolder(DB_CONN, PHYSICAL_ROOT, _currentWebFolder, FOLDER_NAME, PROGRAM_ID)

                    if(_searchResult):
                        DebugLog("Content: %s is already in DB" % _item)
                        dbManager.Current_Content.remove(_searchResult)
                        _foundOrAddedContent += 1

                    else:
                        _fileType = GetVideoType(DB_CONN, _physicalContent)
                        _split = os.path.splitext(_item)
                        _fileName = _split[0]

                        if(_fileType > -1):
                            DebugLog("Adding %s to Database" %_item)

                            Database.Insert(DB_CONN,
                                INTO = dbManager.Db_Content,
                                ROW = ['Folder_Id', 'FileType_Id', 'Content_Name', 'Content_Location'],
                                VALUES = [_currentFolderId, _fileType, _fileName, _webContent])
                            
                            Database.Update(DB_CONN, 
                                dbManager.Db_Program, 
                                SET = 'Num_Content = Num_Content + 1',
                                WHERE = 'Program_Id = %i' % PROGRAM_ID)
                            _foundOrAddedContent += 1

    return _foundOrAddedContent

#Finds Folder Id if it exists, creates one if it doesn't
def FindFolder(DB_CONN, PHYSICAL_PATH, WEB_PATH, FOLDER_NAME, PROGRAM_ID):
    DebugLog("Checking if Content Folder %s: is in Database" % FOLDER_NAME)

    _searchResult = Database.Select(DB_CONN,
        SELECT = 'Folder_Id, Program_Id',
        FROM = dbManager.Db_ContFolder,
        WHERE = 'Folder_Location == "%s"' % WEB_PATH)
    
    if(_searchResult):
        DebugLog("Folder %s has been Found" % FOLDER_NAME)

        if(PROGRAM_ID == _searchResult[1]):
            DebugLog("Folder %s Information up to date" % FOLDER_NAME)

            dbManager.Current_ContFolder.remove(_searchResult)
            return _searchResult[0]

        else:
            DebugLog("Updating Folder %s with new Program ID: %i" % (FOLDER_NAME, PROGRAM_ID))

            Database.Update(DB_CONN, 
                dbManager.Db_ContFolder, 
                SET = 'Program_Id = %i' % PROGRAM_ID,
                WHERE = 'Folder_Id = %i' % _searchResult[0])

            return _searchResult[0]

    else:
        DebugLog("Adding Folder %s to Database" % FOLDER_NAME)
        _folderId = Database.Insert(DB_CONN,
            INTO = dbManager.Db_ContFolder,
            ROW = ['Folder_Name', 'Folder_Location', 'Program_Id'],
            VALUES = [FOLDER_NAME, WEB_PATH, PROGRAM_ID])
        
        return _folderId

