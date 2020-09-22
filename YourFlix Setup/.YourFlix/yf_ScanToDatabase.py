#! /usr/bin/env python
import os
import yf_Database as dbManager
import yf_DbHandler as Database
import yf_BuildContentDB as ContentManager

def BuildProgramDb(DB_CONN):
    _physicalRoot = os.path.join(dbManager.YF_Html, dbManager.Yf_Dir)
    _webRoot = "/"+dbManager.Yf_Dir
        
    if(os.path.exists(_physicalRoot)):
        
        for _item in os.listdir(_physicalRoot):

            _physicalLoc = os.path.join(_physicalRoot, _item)
            _webLoc = os.path.join(_webRoot, _item)


            if(_item not in dbManager.ScannerIgnore and os.path.isdir(_physicalLoc)):
                _programVisibility = 0
                _programId = -1
                _searchResult = Database.Select(DB_CONN, 
                    SELECT = 'Program_Id, Program_Visible',
                    FROM = dbManager.Db_Program,
                    WHERE = 'Program_Location == "%s"' % _physicalLoc)

                if(_searchResult):
                    _programId = _searchResult[0]
                    _programVisibility = _searchResult[1]
                    dbManager.Current_Program.remove(_searchResult)

                else:
                    _programId = Database.Insert(DB_CONN,
                        INTO = dbManager.Db_Program,
                        ROW = ['Program_Name', 'Program_Location', 'Program_Web_Location', 'Program_Visible', 'Num_Content'],
                        VALUES = [_item, _physicalLoc, _webLoc, _programVisibility, 0])

                if(_programId == -1):
                    raise Exception("ERROR: No Program Id Created")

                _hasContent = ContentManager.FindContent(DB_CONN, _physicalRoot, _webRoot, _item, _programId)

                if(_hasContent and _programVisibility != 1):
                    Database.Update(DB_CONN, 
                        dbManager.Db_Program, 
                        SET = 'Program_Visible = %i' % 1,
                        WHERE = 'Program_Id = %i' % _programId)

                elif(not _hasContent and _programVisibility == 1):
                    Database.Update(DB_CONN, 
                        dbManager.Db_Program, 
                        SET = 'Program_Visible = %i' % 0,
                        WHERE = 'Program_Id = %i' % _programId)

def PullFromDatabase(DB_CONN):
    dbManager.Current_Program = Database.Select(DB_CONN, SELECT = 'Program_Id, Program_Visible', FROM = dbManager.Db_Program, fetchall = True)
    
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