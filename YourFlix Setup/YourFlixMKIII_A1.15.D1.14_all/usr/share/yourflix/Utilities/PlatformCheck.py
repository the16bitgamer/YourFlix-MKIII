#! /usr/bin/env python
from sys import platform

def GetPlatform():
    if platform == "linux" or platform == "linux2":
        return "Linux"
    elif platform == "darwin":
        return "MacOS"
    elif platform == "win32":
        return "Windows"
    return "Unknown"