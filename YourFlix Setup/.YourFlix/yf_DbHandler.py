import sqlite3

Debug = True
LastId = -1

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
   
    if Debug:
        print("CREATE TABLE '%s' (%s)" % (TABLE,_insertValues))
   
    _pointer.execute("CREATE TABLE '%s' (%s)" % (TABLE,_insertValues))

def AlterTable(CONNECTION, TABLE = None, RENAMECOLUMN = None):
    if not TABLE:
        raise Exception("TABLE: type str cannot be empty")

    if not type(TABLE) is str:
        raise TypeError("CreateDb TABLE Need to be a string, it is a %s" % str(type(TABLE)))

    _pointer = CONNECTION.cursor()
    TABLE = "ALTER TABLE %s" % TABLE
    if(RENAMECOLUMN):
        RENAMECOLUMN = "RENAME COLUMN %s" % RENAMECOLUMN
    else:
        RENAMECOLUMN = ""

    if Debug:
        print("%s %s" % (TABLE, RENAMECOLUMN))
   
    _pointer.execute("%s %s" % (TABLE, RENAMECOLUMN))

def Select(CONNECTION, SELECT = None, FROM = None, WHERE = None, ORDERBY = None, fetchall = False):
  
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
    
    SELECT = ('SELECT %s' % SELECT)
    FROM = ('FROM %s' % FROM)

    if WHERE:
        WHERE = ('WHERE %s' % WHERE)
    else:
        WHERE = ''
    
    if ORDERBY:
        ORDERBY = ('ORDER BY %s' %ORDERBY)
    else:
        ORDERBY = ''
    
    if Debug:
        print("%s %s %s %s" % (SELECT, FROM, WHERE, ORDERBY))
  
    _pointer.execute("%s %s %s %s" % (SELECT, FROM, WHERE, ORDERBY))
  
    if fetchall:
        return _pointer.fetchall()
    
    return _pointer.fetchone()

def Drop(CONNECTION, DATABASE = None):
  
    if not DATABASE:
        raise Exception("DATABASE: type str cannot be empty")
  
    _pointer = CONNECTION.cursor()
  
    if len(DATABASE) == "":
        raise Exception("CreateDb DATABASE cannot be empty")  
  
    if Debug:
        print("DROP TABLE %s" % DATABASE)
  
    _pointer.execute("DROP TABLE %s" % DATABASE)

def Insert(CONNECTION, INTO = None, VALUES = None, ROW = None):
  
    if not INTO:
        raise Exception("INTO: type str cannot be empty")
  
    if not VALUES:
        raise Exception("VALUES: type list cannot be empty")
  
    _pointer = CONNECTION.cursor()
    _insertRows = ""
    _insertValues = ""
  
    if not type(VALUES) is list:
        raise TypeError("INSERT VALUES Need to be a list, it is a %s" % str(type(VALUES)))
  
    for item in VALUES:
  
        if _insertValues != "":
            _insertValues += ", "
  
        _insertValues += FormatItem(item)
  
    if ROW:
  
        if not type(ROW) is list:
            raise TypeError("INSERT VALUES Need to be a list, it is a %s" % str(type(VALUES)))
                
        for item in ROW:
  
            if _insertRows != "":
                _insertRows += ", "
  
            _insertRows += str(item)
  
        if Debug:
            print("INSERT INTO '%s' (%s) VALUES(%s)" % (INTO, _insertRows, _insertValues))
  
        _pointer.execute("INSERT INTO '%s' (%s) VALUES(%s)" % (INTO, _insertRows, _insertValues))
  
    else:
  
        if Debug:
            print("INSERT INTO '%s' VALUES(%s)" % (INTO, _insertValues))
  
        _pointer.execute("INSERT INTO %s VALUES(%s)" % (INTO, _insertValues))
  
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
  
    if Debug:
        print("DELETE FROM '%s' WHERE %s" % (FROM, WHERE))
  
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

    if Debug:
        print('%s %s %s' % (DATABASE, SET, WHERE))
  
    _pointer.execute('%s %s %s' % (DATABASE, SET, WHERE))