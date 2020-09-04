#! /usr/bin/env python

Yf_Config = '/etc/yourflix/yourflix.config'

Yf_DbLoc = '/usr/share/yourflix/yourflix.db'
YF_Html = "/var/www/html"
Yf_Dir = "Videos"

Db_Version = 1.0

Db_Img = 'Img_Db'
Db_Content = 'Content_Db'
Db_Program = 'Program_Db'
Db_YourFlix = 'YourFlix_Db'
Db_File = 'FileType_Db'

Db_List = [Db_Img, Db_Content, Db_Program, Db_YourFlix, Db_File]

SupportedVideos = ['MP4']
SupportedImg = ['PNG']
FileTypes = ['Folder']
ScannerIgnore = ['$RECYCLE.BIN', '.YF-IMG', '.YF-META', 'System Volume Information']
MetaFolder = ".YF-META"