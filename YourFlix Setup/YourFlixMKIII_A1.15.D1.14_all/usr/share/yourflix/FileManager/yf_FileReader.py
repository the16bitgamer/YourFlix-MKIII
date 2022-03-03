#! /usr/bin/env python

def SearchForStringInFile(FILE_Name, STRING):
    with open(FILE_Name, 'r') as read_obj:
        for line in read_obj:
            if(STRING in line):
                return True
    return False

def SearchForStringArrayInFile(FILE_Name, STRING_ARR):
    pos = 0
    with open(FILE_Name, 'r') as read_obj:
        for line in read_obj:
            if STRING_ARR[pos] in line:
                if(len(STRING_ARR) == pos+1):
                    return True
                else:
                    pos += 1
            elif(pos != 0):
                return False
    return False