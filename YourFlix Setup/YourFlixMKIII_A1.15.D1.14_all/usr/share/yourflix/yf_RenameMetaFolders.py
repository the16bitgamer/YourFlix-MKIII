import os
import yf_Database as dbManager
import yf_ProgramBuilder as ProgramBuilder

debug = False

def DebugLog(MESSAGE):
    if(debug):
        print("RenameMetaFolder - %s" % MESSAGE)

def RenameMeta():
    _physicalRoot = os.path.join(dbManager.YF_Html, dbManager.Yf_Dir)
    _webRoot = "/" + dbManager.Yf_Dir
            
    if(os.path.exists(_physicalRoot)):
            
        for _item in os.listdir(_physicalRoot):
            if(_item not in dbManager.ScannerIgnore):
                for _old in dbManager.Meta_Old:
                    _oldFolder = os.path.join(_physicalRoot, _item, _old)
                    _newFolder = os.path.join(_physicalRoot, _item, dbManager.MetaFolder)

                    
                    if(os.path.exists(_oldFolder)):
                        os.rename(_oldFolder, _newFolder)

RenameMeta()