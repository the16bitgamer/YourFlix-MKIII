#! /usr/bin/env python
import os
import inspect
from inspect import getframeinfo

isDebugging = True
showPackage = True

def Debug(STRING):
    printString = str(STRING)
    if(isDebugging):
        if(showPackage):
            frame = inspect.stack()[1]
            frameinfo  = getframeinfo(frame[0])
            print(printString + "\n" + os.path.basename(frameinfo.filename) + " Line(" + str(frameinfo.lineno) + ")")
        else:
            print(printString)