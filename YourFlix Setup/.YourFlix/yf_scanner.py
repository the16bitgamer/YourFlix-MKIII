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
        print("Config File Not Found")

    dbManager.FileTypes = dbManager.FileTypes + dbManager.SupportedVideos + dbManager.SupportedImg

def LoadDatabase():
    conn = sqlite3.connect(dbManager.Yf_DbLoc)
    Builder.CheckDatabase(conn)
    DirScanner.ScanDirToDb(conn)
    ProgramBuilder.BuildPrograms(conn)
    #conn.commit()
    conn.close()

def UpdateChildren(DB_CONN, MOVED_FROM, MOVED_TO, CONTENT_TO_UPDATE):

    for child in CONTENT_TO_UPDATE:
        _currentLoc = child[1].split(MOVED_FROM)[1][1:]
        _targetWeb = os.path.join(MOVED_TO, _currentLoc)
        Database.Update(DB_CONN, DATABASE = dbManager.Db_Content, SET = 'Location="%s"' % _targetWeb, WHERE = "Id == %i" % child[0])
        _childrenToUpdate = Database.Select(DB_CONN, SELECT = "Id, Location", FROM = dbManager.Db_Content, WHERE = 'Parent_Id == %i' % child[0], fetchall = True)
        
        if _childrenToUpdate:
            UpdateChildren(DB_CONN, MOVED_FROM, MOVED_TO, _childrenToUpdate)

def DeleteItemFromDatabase(DB_CONN, CONTENT_ID):
    _potentialChildren = Database.Select(DB_CONN, SELECT = "Id", FROM = dbManager.Db_Content, WHERE = 'Parent_Id == "%i"' % CONTENT_ID, fetchall=True)

    if(_potentialChildren):
        
        for item in _potentialChildren:
            DeleteItemFromDatabase(DB_CONN, item[0])

    Database.Delete(DB_CONN, FROM = dbManager.Db_Content, WHERE = "Id = %i" % CONTENT_ID)
    Database.Delete(DB_CONN, FROM = dbManager.Db_Program, WHERE = "Folder_Id = %i" % CONTENT_ID)

def AddItemToDatabase(DB_CONN, ITEM_PHYSICAL_LOC,GET_PARENTS = False):
    _split = os.path.splitext(ITEM_PHYSICAL_LOC)
    _fileType = (_split[len(_split)-1][1:]).upper()
    _item = os.path.split(ITEM_PHYSICAL_LOC)
    _itemName = _item[1]
    _itemPath = _item[0]
    
    if _itemName not in dbManager.ScannerIgnore and (_fileType in dbManager.SupportedVideos or GET_PARENTS) and os.path.normpath(ITEM_PHYSICAL_LOC) != dbManager.YF_Html:
        _webLoc = ITEM_PHYSICAL_LOC.split(dbManager.YF_Html)[1]
        _itemDbId = Database.Select(DB_CONN, SELECT = "Id", FROM = dbManager.Db_Content, WHERE = 'Location == "%s"' % _webLoc)
        
        if(_itemDbId):
            return _itemDbId[0]

        else:
            _parent_Id = AddItemToDatabase(DB_CONN, _itemPath, GET_PARENTS = True)
            _currentId = Database.Insert(DB_CONN, INTO = dbManager.Db_Content, ROW = ["Parent_Id", "File_Type", "Name", "Location"], VALUES = [_parent_Id, DirScanner.GetFileType(ITEM_PHYSICAL_LOC), _itemName, _webLoc])
            print("NAME: %s, ID %s"%(_itemName,_currentId))
            
            if DirScanner.IsYourFlixProgram(ITEM_PHYSICAL_LOC):
                _searchResult = SearchDb(DB_CONN, dbManager.Db_Program, "Id, Folder_Id, Name", 'Name == "%s"' % _itemName) 

                if not _searchResult:
                    Database.Insert(DB_CONN, INTO = dbManager.Db_Program, ROW = ["Folder_Id", "Name"], VALUES = [_currentId, _itemName])

                else:
                    Database.Delete(DB_CONN, FROM = dbManager.Db_Program, WHERE = "Id = %i" % _searchResult[0][0])
                    Database.Insert(DB_CONN, INTO = dbManager.Db_Program, ROW = ["Folder_Id", "Name"], VALUES = [_currProgId, _itemName])

            return _currentId
    
    else:
        return -1
    
def YourflixMonitor():
    _physicalLoc = os.path.join(dbManager.YF_Html,dbManager.Yf_Dir)

    LoadDatabase()
    print("Database up to date")

    print("Starting Scanner")

    watcher = inotify.adapters.InotifyTree(_physicalLoc)
    print("Scanner Started")

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
                    movedWebFolder = os.path.join(path.split(dbManager.YF_Html)[1], filename)

                else:
                    conn = sqlite3.connect(dbManager.Yf_DbLoc)
                    
                    if 'IN_MOVED_TO' in types and movedFolderFlag and movedFolderRoot == path:
                        _target = os.path.join(path, filename)
                        _targetWeb = os.path.join(path.split(dbManager.YF_Html)[1], filename)
                        _contentId = Database.Select(conn, SELECT = "Id", FROM = dbManager.Db_Content, WHERE = 'Location == "%s"' % movedWebFolder)[0]
                        Database.Update(conn, DATABASE = dbManager.Db_Content, SET = 'Location="%s"' % _targetWeb, WHERE = "Id == %i" % _contentId)
                        
                        if os.path.isdir(_target):  
                            
                            if(DirScanner.IsYourFlixProgram(_target)):
                                Database.Update(conn, DATABASE = dbManager.Db_Program, SET = 'Name="%s"' % filename,WHERE = "Folder_Id == %i" % _contentId)
                           
                            _childrenToUpdate = Database.Select(conn, SELECT = "Id, Location", FROM = dbManager.Db_Content, WHERE = 'Parent_Id == "%i"' % _contentId, fetchall = True)
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
                        _removedWebItem = os.path.join(path.split(dbManager.YF_Html)[1], filename)
                        _contentId = Database.Select(conn, SELECT = "Id", FROM = dbManager.Db_Content, WHERE = 'Location == "%s"' % _removedWebItem)
                        
                        if(_contentId):
                            DeleteItemFromDatabase(conn, _contentId[0])

                    #conn.commit()
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