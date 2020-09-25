#! /usr/bin/env python
import inotify.adapters
import xml.etree.ElementTree as Xml
import os
import sqlite3
import sys
import yf_Database as dbManager
import yf_DbHandler as Database
import yf_DbBuilder as Builder
import yf_ScanToDatabase as DirScanner
import yf_ProgramBuilder as ProgramBuilder
import yf_AutoUpdateDB as dbUpdater
import yf_AutoAddToDB as dbAdder
import yf_AutoRemoveFromDB as dbRemover

debug = True

def DebugLog(MESSAGE):
    print("Scanner - %s" % MESSAGE)

def LoadConfig():
    if(os.path.exists(dbManager.Yf_Config)):
        _config = Xml.parse(dbManager.Yf_Config).getroot()
        
        dbManager.Yf_DbLoc = _config.find("Database").attrib["location"]
        dbManager.YF_Html = _config.find("WebRoot").attrib["location"]
        dbManager.Yf_Dir = _config.find("VideoRoot").attrib["location"]
        localFiles = _config.find("FileTypes")

        dbManager.SupportedVideos = localFiles.find("Video").attrib["types"].split(',')
        dbManager.SupportedImg = localFiles.find("Image").attrib["types"].split(',')
    else:
        DebugLog("Config File Not Found")

    dbManager.FileTypes = dbManager.FileTypes + dbManager.SupportedVideos + dbManager.SupportedImg

def LoadDatabase():
    conn = sqlite3.connect(dbManager.Yf_DbLoc)
    Builder.CheckDatabase(conn)
    DirScanner.ScanDirToDb(conn)
    ProgramBuilder.BuildPrograms(conn)
    conn.commit()
    conn.close()

def CheckFolderType(FOLDER_ROOT):
    _yourFlix_Root = dbManager.Yf_Dir

    DebugLog("Checking if %s is %s" %(_yourFlix_Root, FOLDER_ROOT))

    if(FOLDER_ROOT == _yourFlix_Root):
        return "Program"

    return "Folder"

def CheckFileType(DB_CONN, FILE):

    _split = os.path.splitext(FILE)
    _search = (_split[len(_split)-1]).lower()
        
    if(_search != None):

        DebugLog("Extention is: %s" % _search)
        _searchResult = Database.Select(DB_CONN,
            SELECT = 'FileType',
            FROM = dbManager.Db_File,
            WHERE = 'FileType_Extention = "%s"' % (_search))

        if _searchResult:
            return _searchResult[0]

    return dbManager.FolderType

def AddItem(DB_CONN, WEB_ROOT, PHYS_ROOT, ITEM):
    _itemPhysLoc = os.path.join(PHYS_ROOT, ITEM)
    _itemWebLoc = os.path.join(WEB_ROOT, ITEM)

    if(os.path.isdir(_itemPhysLoc)):
        _folderType = CheckFolderType(WEB_ROOT)

        if(_folderType == "Program"):
            dbAdder.AddProgramToDb(DB_CONN, _itemWebLoc, ITEM)

        elif(_folderType == "Folder"):
            dbAdder.AddFolderToDb(DB_CONN, WEB_ROOT, _itemWebLoc, ITEM)

    elif(os.path.isfile(_itemPhysLoc) and WEB_ROOT != dbManager.Yf_Dir):
        _fileType = CheckFileType(DB_CONN, ITEM)

        if(_fileType == dbManager.VideoType):
            dbAdder.AddContentToDb(DB_CONN, WEB_ROOT, _itemWebLoc, ITEM)

        elif(_fileType == dbManager.ImageType and dbManager.MetaFolder in WEB_ROOT):
            dbAdder.AddMetaImgToDb(DB_CONN, WEB_ROOT, _itemWebLoc)

def DeleteItem(DB_CONN, WEB_ROOT, ITEM):
    _itemWebLoc = '/' + os.path.join(WEB_ROOT, ITEM)    
    _fileType = CheckFileType(DB_CONN, ITEM)

    if(_fileType == dbManager.FolderType):
        _folderType = CheckFolderType(WEB_ROOT)

        if(_folderType == "Program"):
            dbRemover.RemoveProgramFromDb(DB_CONN, _itemWebLoc)

        elif(_folderType == "Folder"):
            dbRemover.RemoveFolderFromDb(DB_CONN, FOLDER_LOCATION = _itemWebLoc)
    
    elif(_fileType == dbManager.VideoType):
        dbRemover.RemoveContentFromDb(DB_CONN, FILE_LOCATION = _itemWebLoc)

    elif(_fileType == dbManager.ImageType and dbManager.MetaFolder in WEB_ROOT):
        dbRemover.RemoveMetaImgFromDb(DB_CONN, FILE_LOCATION = _itemWebLoc)

def UpdateFolder(DB_CONN, ROOT, OLD_FOLDER_LOC, NEW_FOLDER_LOC, FOLDER_NAME):
    _folderPhysRoot = os.path.join(dbManager.YF_Html, ROOT)
    _folderWebLoc = os.path.join(ROOT, FOLDER_NAME)

    if(os.path.isdir(NEW_FOLDER_LOC)):
        _folderType = CheckFolderType(ROOT)
        _originalWebLoc = OLD_FOLDER_LOC.split(dbManager.YF_Html)[1]

        if(_folderType == "Program"):
            dbUpdater.UpdateProgramLocation(DB_CONN, _originalWebLoc, _folderWebLoc)

        elif(_folderType == "Folder"):
            dbUpdater.UpdateFolderLocation(DB_CONN, _originalWebLoc, _folderWebLoc)
    else:
        DeleteItem(DB_CONN, ROOT, FOLDER_NAME)

def YourflixMonitor():
    _physicalLoc = os.path.join(dbManager.YF_Html, dbManager.Yf_Dir)

    LoadDatabase()
    DebugLog("Database up to date")

    DebugLog("Starting Scanner")

    _watcher = inotify.adapters.InotifyTree(_physicalLoc)
    DebugLog("Scanner Started")

    _movedFolderFlag = False
    _movedFolderRoot = None
    _movedFolder = None
    _movedFileName = None

    for event in _watcher.event_gen():

        if event is not None:
                (header, types, path, filename) = event
                
                #Folder Moved
                if 'IN_MOVED_FROM' in types:
                    _movedFolderFlag = True
                    _movedFolderRoot = path
                    _movedFolder = os.path.join(path, filename)
                    _movedFileName = filename

                else:
                    _conn = sqlite3.connect(dbManager.Yf_DbLoc)
                    _webRoot = "/" + path.split(dbManager.YF_Html + "/")[1]
                    
                    #Update Folder
                    if 'IN_MOVED_TO' in types:

                        if _movedFolderFlag and _movedFolderRoot == path:
                            _target = os.path.join(path, filename)
                            
                            UpdateFolder(_conn, _webRoot, _movedFolder, _target, filename)

                            _movedFolderFlag = False
                            _movedFolderRoot = None
                            _movedFolder = None
                            _movedFileName = None

                        if(not _movedFolderFlag):
                            _folderType = CheckFolderType(_webRoot)

                            if(_folderType == "Program"):
                                DebugLog("Adding Program %s" % filename)
                                DirScanner.AddProgram(_conn, filename, path, _webRoot)                            
                                ProgramBuilder.BuildPrograms(_conn)

                            elif(_folderType == "Folder"):
                                DebugLog("Adding Folder %s" % filename)
                                DirScanner.AddContentFolder(_conn, path, _webRoot, filename)

                    elif _movedFolderFlag:
                        DeleteItem(_conn, _webRoot, _movedFileName)
                        
                        _movedFolderFlag = False
                        _movedFolderRoot = None
                        _movedFolder = None
                        _movedFileName = None
                    
                    #File/Folder Created/Changed
                    if 'IN_CREATE' in types:
                        AddItem(_conn, _webRoot, path, filename)
                    
                    #File/Folder Deleted
                    if 'IN_DELETE' in types:
                        DeleteItem(_conn, _webRoot, filename)

                    _conn.commit()
                    _conn.close()

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