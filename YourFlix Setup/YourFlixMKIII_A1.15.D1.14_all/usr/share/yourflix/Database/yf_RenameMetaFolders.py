import os
from Resources import yf_DBDefaults as dbManager
from Resources import yf_LinuxDefaults as LinuxDefaults
from Utilities import PlatformCheck as PC

def RenameMeta():
    _physicalRoot = ""
    if(PC.GetPlatform() == "Linux"):
        _physicalRoot = LinuxDefaults.Phys_HtmlLoc
            
    if(os.path.exists(_physicalRoot)):
            
        for _item in os.listdir(_physicalRoot):
            if(_item not in dbManager.ScannerIgnore):
                for _old in dbManager.Meta_Old:
                    _oldFolder = os.path.join(_physicalRoot, _item, _old)
                    _newFolder = os.path.join(_physicalRoot, _item, dbManager.MetaFolder)

                    
                    if(os.path.exists(_oldFolder)):
                        os.rename(_oldFolder, _newFolder)

RenameMeta()