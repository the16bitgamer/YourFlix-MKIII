#! /usr/bin/env python
import sqlite3

debug = False
LastId = -1

def DebugLog(MESSAGE):
    if(debug):
        print("DbHandler - %s" % MESSAGE)

def FormatItem(ITEM):
   
    if type(ITEM) is str:
        return '"%s"' % ITEM
    
    else:
        return str(ITEM)
    
def CreateTable(CONNECTION, TABLE = None, VALUES = None):
  
    if not TABLE:
        raise Exception("TABLE: type str cannot be empty")
  
    if not VALUES:
        raise Exception("VALUES: type list cannot be empty")    
  
    _pointer = CONNECTION.cursor()
    _insertValues = ""
  
    if not type(TABLE) is str:
        raise TypeError("CreateDb TABLE Need to be a string, it is a %s" % str(type(TABLE)))
   
    if len(TABLE) == "":
        raise Exception("CreateDb TABLE cannot be empty")    
   
    if not type(VALUES) is list:
        raise TypeError("CreateDb VALUES Need to be a list of strings, it is a %s" % str(type(VALUES)))
  
    for obj in VALUES:
   
        if(_insertValues != ""):
            _insertValues += ","
   
        for item in obj:
   
            if(_insertValues != ""):
                _insertValues += " "
            _insertValues += str(item)
   
    DebugLog('CREATE TABLE "%s" (%s)' % (TABLE,_insertValues))
    _pointer.execute("CREATE TABLE '%s' (%s)" % (TABLE,_insertValues))

def AlterTable(CONNECTION, TABLE = None, RENAMECOLUMN = None, ADDCOLUMN = None):
    if not TABLE:
        raise Exception("TABLE: type str cannot be empty")

    if not type(TABLE) is str:
        raise TypeError("AlterTABLE: TABLE Need to be a string, it is a %s" % str(type(TABLE)))

    _pointer = CONNECTION.cursor()
    _table = "ALTER TABLE %s " % TABLE
    _renameColumn = ""
    _dropColumn = ""
    _addColumn = ""

    if(RENAMECOLUMN):
        _renameColumn = "RENAME COLUMN %s " % RENAMECOLUMN

    if(ADDCOLUMN):
        _addColumn = "ADD %s " % ADDCOLUMN

    _query = '%s%s%s' % (_table, _renameColumn, _addColumn)

    DebugLog(_query)   
    _pointer.execute(_query)

def Select(CONNECTION, SELECT = None, INTO = None, FROM = None, WHERE = None, ORDERBY = None, fetchall = False):
  
    if not SELECT:
        raise Exception("SELECT: type str cannot be empty")

    if not FROM:
        raise Exception("FROM: type str cannot be empty")
  
    _pointer = CONNECTION.cursor()
    _selecting = ""
  
    if not type(FROM) is str:
        raise TypeError("CreateDb FROM Need to be a string, it is a %s" % str(type(FROM)))
  
    if len(FROM) == "":
        raise Exception("CreateDb FROM cannot be empty")    
  
    if not type(SELECT) is str:
        raise TypeError("CreateDb SELECT Need to be a str, it is a %s" % str(type(SELECT)))
  
    for item in SELECT:
  
        if _selecting == "":
            _selecting += ","
  
        _selecting += str(item)
    
    SELECT = ('SELECT %s ' % SELECT)
    FROM = ('FROM %s ' % FROM)

    if WHERE:
        WHERE = ('WHERE %s ' % WHERE)
    else:
        WHERE = ''
    
    if ORDERBY:
        ORDERBY = ('ORDER BY %s ' %ORDERBY)
    else:
        ORDERBY = ''
    
    DebugLog('%s%s%s%s' % (SELECT, FROM, WHERE, ORDERBY))  
    _pointer.execute("%s%s%s%s" % (SELECT, FROM, WHERE, ORDERBY))
  
    if fetchall:
        return _pointer.fetchall()
    
    return _pointer.fetchone()

def Drop(CONNECTION, DATABASE = None):
  
    if not DATABASE:
        raise Exception("DATABASE: type str cannot be empty")
  
    _pointer = CONNECTION.cursor()
  
    if len(DATABASE) == "":
        raise Exception("CreateDb DATABASE cannot be empty")  
  
    DebugLog('DROP TABLE %s' % DATABASE)  
    _pointer.execute("DROP TABLE %s" % DATABASE)

def Insert(CONNECTION, INTO = None, VALUES = None, ROW = None, SELECT = None, FROM = None):
  
    if not INTO:
        raise Exception("INTO: type str cannot be empty")
  
    _pointer = CONNECTION.cursor()
    _into = 'INTO %s' % INTO
    _insertRows = ""
    _insertValues = ""
    _select = ""
    _from = ""
  
    if VALUES:
        if not type(VALUES) is list:
            raise TypeError("INSERT VALUES Need to be a list, it is a %s" % str(type(VALUES)))

        _insertValues = " VALUES("
        x = 0

        for item in VALUES:

            if x > 0:
                _insertValues += ', '
    
            _insertValues += FormatItem(item)
            x += 1

        _insertValues += ')'

  
    if ROW:
        if not type(ROW) is list:
            raise TypeError("INSERT VALUES Need to be a list, it is a %s" % str(type(VALUES)))

        _insertRows = " ("   
        x = 0

        for item in ROW:
  
            if x > 0:
                _insertRows += ", "
  
            _insertRows += str(item)
            x += 1
        
        _insertRows += ')'

    if SELECT:
        _select = " SELECT %s" % SELECT
    
    if FROM:
        _from = " FROM %s" % FROM

    DebugLog('INSERT %s%s%s%s%s' % (_into, _insertRows, _insertValues, _select, _from))
    _pointer.execute("INSERT %s%s%s%s%s" % (_into, _insertRows, _insertValues, _select, _from))
  
    global LastId
    LastId = _pointer.lastrowid
  
    return LastId
    
def Delete(CONNECTION, FROM = None, WHERE = None):
  
    if not FROM:
        raise Exception("INTO: type str cannot be empty")
  
    if not WHERE:
        raise Exception("VALUES: type str cannot be empty")
  
    if not type(FROM) is str:
        raise TypeError("Delete FROM Need to be a string, it is a %s" % str(type(FROM)))
  
    if not type(WHERE) is str:
        raise TypeError("Delete WHERE Need to be a string, it is a %s" % str(type(WHERE)))
  
    _pointer = CONNECTION.cursor()
  
    DebugLog('DELETE FROM "%s" WHERE %s' % (FROM, WHERE))  
    _pointer.execute("DELETE FROM '%s' WHERE %s" % (FROM, WHERE))

def Update(CONNECTION, DATABASE, SET, WHERE = None):
  
    if not DATABASE:
        raise Exception("DATABASE: type str cannot be empty")
  
    if not SET:
        raise Exception("SET: type str cannot be empty")
  
    if not type(DATABASE) is str:
        raise TypeError("Update DATABASE Need to be a string, it is a %s" % str(type(DATABASE)))
  
    if not type(SET) is str:
        raise TypeError("Update SET Need to be a string, it is a %s" % str(type(SET)))
  
    _pointer = CONNECTION.cursor()
  
    DATABASE = "UPDATE %s" % DATABASE
    SET = "SET %s" % SET
    if(WHERE):
        WHERE = "WHERE %s" % WHERE
    else:
        WHERE = ""

    DebugLog('%s %s %s' % (DATABASE, SET, WHERE))
    _pointer.execute('%s %s %s' % (DATABASE, SET, WHERE))