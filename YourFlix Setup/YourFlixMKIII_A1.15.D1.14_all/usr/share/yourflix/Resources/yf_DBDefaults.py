#! /usr/bin/env python

Db_Version = 1.14

Db_Channel = 'Channel'
Db_ChProgram = 'Channel_Program'
Db_Program = 'Program'
Db_Img = 'Program_Image'
Db_ImageType = 'Img_Type'
Db_File = 'File_Type'
Db_ContFolder = 'Content_Folder'
Db_Content = 'Folder_Content'
Db_YourFlix = 'YourFlix_Db'

Current_Program = None
Current_ContFolder = None
Current_Content = None

Current_MetaImages = None
Current_AllChannel = None
Current_FilmsChannel = None
Current_ShowsChannel = None

Db_List = [Db_YourFlix, Db_Channel, Db_ChProgram, Db_Program, Db_Img, Db_ImageType, Db_File, Db_ContFolder, Db_Content]
Db_Old = ['Img_Db', 'Content_Db', 'Program_Db', 'YourFlix_Db', 'FileType_Db']
Meta_Old = ['.YF-IMG', '.YF-META']

FolderType = "Folder"
VideoType = "Video"
ImageType = "Image"

DefaultChannels = ['All', 'Films', 'Shows']

SupportedVideos = ['MP4', 'WebM', 'Ogg']
SupportedImg = ['PNG', 'BMP', 'GIF', 'ICO', 'JPEG', 'JPG']
FileTypes = ['Folder']

ScannerIgnore = Meta_Old + ['$RECYCLE.BIN', MetaFolder, 'System Volume Information']
