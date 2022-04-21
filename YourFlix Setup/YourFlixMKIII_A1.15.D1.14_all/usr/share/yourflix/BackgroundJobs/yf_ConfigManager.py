#! /usr/bin/env python
#Import from Parent DIR
import sys, os
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

import xml.etree.cElementTree as ET
from Resources import yf_LinuxDefaults as LinuxDefaults
from Utilities import PlatformCheck as PC
from Utilities import yf_Log as Log
from pathlib import Path

def LoadConfig():
    if(PC.GetPlatform() == "Linux"):
        Log.Debug("Loading Configuration")
        if(os.path.exists(LinuxDefaults.Phys_ConfigLoc)):
            Log.Debug("Path Exists")
            tree = ET.parse(LinuxDefaults.Phys_ConfigLoc)
            root = tree.getroot()
            updateConfig = True
            for child in root:
                if(child.tag == "Version"):
                    updateConfig = not(str(LinuxDefaults.ConfigVersion) == child.text)
                    Log.Debug("Updating Config = " + str(updateConfig))
                if(child.tag == "PhysLoc"):
                    for loc in child:
                        if(loc.tag == "Database"):
                            LinuxDefaults.Phys_DbLoc = loc.text
                        if(loc.tag == "HTML"):
                            LinuxDefaults.Phys_HtmlLoc = loc.text
                        if(loc.tag == "MetaFolderName"):
                            LinuxDefaults.MetaFolder = loc.text
                        if(loc.tag == "PyModuleLoc"):
                            LinuxDefaults.PyModulesLoc = loc.text
                if(child.tag == "PyModules"):
                    configedModules = []
                    for module in child:
                        configedModules.append(module.text.split(','))
                    LinuxDefaults.PythonModuals = configedModules
                if(child.tag == "Drives"):
                    configedModules = []
                    for module in child:
                        configedModules.append(module.text.split(','))
                    LinuxDefaults.MountedDrives = configedModules
            if(updateConfig):
                CreateConfig()
        else:
            Log.Debug("Configuration Does not Exist, creating config from Defaults")
            CreateConfig()
    else:
        Log.Debug("Incompatible Platform, please use YourFlix on Linux")

def CreateConfig():
    parentFolder = os.path.dirname(LinuxDefaults.Phys_ConfigLoc)
    if(not os.path.exists(parentFolder)):
        Path(parentFolder).mkdir(parents=True, exist_ok=True)

    root = ET.Element("YourFlix")
    ET.SubElement(root, "Version").text = str(LinuxDefaults.ConfigVersion)
    fileLoc = ET.SubElement(root, "PhysLoc")
    pyModules = ET.SubElement(root, "PyModules")
    ET.SubElement(root, "Drives")

    ET.SubElement(fileLoc, "Database").text = LinuxDefaults.Phys_DbLoc
    ET.SubElement(fileLoc, "HTML").text = LinuxDefaults.Phys_HtmlLoc
    ET.SubElement(fileLoc, "MetaFolderName").text = LinuxDefaults.MetaFolder
    ET.SubElement(fileLoc, "PyModuleLoc").text = LinuxDefaults.PyModulesLoc

    for module in LinuxDefaults.PythonModuals:
        ET.SubElement(pyModules, "Module").text = ','.join(module)

    for drives in LinuxDefaults.MountedDrives:
        ET.SubElement(pyModules, "Drive").text = ','.join(drives)

    tree = ET.ElementTree(root)
    tree.write(LinuxDefaults.Phys_ConfigLoc, encoding = "UTF-8", xml_declaration = True)

if __name__ == '__main__':
    LoadConfig()