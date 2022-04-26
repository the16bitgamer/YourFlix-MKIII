#! /usr/bin/env python
#Import from Parent DIR
import sys, os
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

import xml.etree.cElementTree as ET
from Resources import yf_Defaults as Defaults
from Resources import yf_LinuxDefaults as LinuxDefaults
from Resources import yf_DBDefaults as DBDefaults
from Resources import yf_Defaults as Defaults
from Utilities import PlatformCheck as PC
from Utilities import yf_Log as Log
from Utilities import FileFolderTool as FFT

def LoadConfig():
    if(PC.GetPlatform() == "Linux"):
        Defaults.ConfigVersion = LinuxDefaults.ConfigVersion
        Defaults.MetaFolder = LinuxDefaults.MetaFolder
        Defaults.Phys_ConfigLoc = LinuxDefaults.Phys_ConfigLoc
        Defaults.Phys_DbLoc = LinuxDefaults.Phys_DbLoc
        Defaults.Phys_HtmlLoc = LinuxDefaults.Phys_HtmlLoc
        Defaults.PyModulesLoc = LinuxDefaults.PyModulesLoc
    else:
        Log.Debug("Incompatible Platform, please use YourFlix on Linux")

    Log.Debug("Loading Configuration")
    if(FFT.PathExist(Defaults.Phys_ConfigLoc)):
        Log.Debug("Path Exists")
        tree = ET.parse(Defaults.Phys_ConfigLoc)
        root = tree.getroot()
        updateConfig = True
        for child in root:
            if(child.tag == "Version"):
                updateConfig = not(str(Defaults.ConfigVersion) == child.text)
                Log.Debug("Updating Config = " + str(updateConfig))
            if(child.tag == "PhysLoc"):
                for loc in child:
                    if(loc.tag == "Database"):
                        Defaults.Phys_DbLoc = loc.text
                    if(loc.tag == "HTML"):
                        Defaults.Phys_HtmlLoc = loc.text
                    if(loc.tag == "MetaFolderName"):
                        Defaults.MetaFolder = loc.text
                    if(loc.tag == "PyModuleLoc"):
                        Defaults.PyModulesLoc = loc.text
            if(child.tag == "PluginPyModules"):
                configedModules = []
                for module in child:
                    configedModules.append(module.text.split(','))
                Defaults.PluginPyModuales = configedModules
            if(child.tag == "Drives"):
                configedModules = []
                for module in child:
                    configedModules.append(module.text.split(','))
                Defaults.MountedDrives = configedModules

        if(updateConfig):
            CreateConfig()
    else:
        Log.Debug("Configuration Does not Exist, creating config from Defaults")
        CreateConfig()

def CreateConfig():
    FFT.VerifyParentFolder(LinuxDefaults.Phys_ConfigLoc)
    UpdateConfig()

def UpdateConfig():
    root = ET.Element("YourFlix")
    ET.SubElement(root, "Version").text = str(Defaults.ConfigVersion)
    fileLoc = ET.SubElement(root, "PhysLoc")
    pyModules = ET.SubElement(root, "PluginPyModules")
    mountedDrives = ET.SubElement(root, "Drives")

    ET.SubElement(fileLoc, "Database").text = Defaults.Phys_DbLoc
    ET.SubElement(fileLoc, "HTML").text = Defaults.Phys_HtmlLoc
    ET.SubElement(fileLoc, "MetaFolderName").text = Defaults.MetaFolder
    ET.SubElement(fileLoc, "PyModuleLoc").text = Defaults.PyModulesLoc

    for module in Defaults.PluginPyModuales:
        ET.SubElement(pyModules, "Module").text = ','.join(module)

    for drives in Defaults.MountedDrives:
        ET.SubElement(mountedDrives, "Drive").text = ','.join(drives)

    tree = ET.ElementTree(root)
    tree.write(Defaults.Phys_ConfigLoc, encoding = "UTF-8", xml_declaration = True)

if __name__ == '__main__':
    LoadConfig()