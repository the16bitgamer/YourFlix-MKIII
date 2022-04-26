#! /usr/bin/env python
import os
from pathlib import Path

#if the Parent folder doesn't exists create it
def VerifyParentFolder(PATH):
    parentFolder = GetFolderPath(PATH)
    if(not PathExist(parentFolder)):
        Path(parentFolder).mkdir(parents=True, exist_ok=True)

def PathExist(PATH):
    return os.path.exists(PATH)

def GetFolderPath(PATH):
    return os.path.dirname(PATH)