#! /usr/bin/env python

Yf_Config = '/etc/yourflix/yourflix2.config'

Yf_DbLoc = '/usr/share/yourflix/yourflix2.db'
YF_Html = "/var/www/html"
Yf_Dir = "Test_Videos"

Db_Version = 1.12

Db_Channel = 'Channel'                                                                          #Channel DB is used to Categorize the Programs on YourFlix, by default we have the All Channel, Film Channel, and TV Channel
Db_ChProgram = 'Channel_Program'                                                                #Channel Program DB is the association between the Channel DB and the Program DB
Db_Program = 'Program'                                                                          #Program DB is where we store our programs to be shown on YourFlix, a Program is a Folder with a '.YF-META' Folder in it.
Db_Img = 'Program_Image'                                                                        #Program Image is a stored list of images located in the '.YF-META' folder to be used by the web page
Db_ImageType = 'Img_Type'                                                                       #Image Type is a DB of all images which can be used by YourFlix, it's an additional tag used to determin if it's a large, small, landscape or portait image. As of version 1.1 it's just storing a default image type, but can be expaned
Db_File = 'File_Type'                                                                           #File Type is a DB which stores all supported file types for YourFlix, more can be added in the Config. By default it looks for Folders, MP4's and PNG's
Db_ContFolder = 'Content_Folder'                                                                 #Program Folder DB contains all the Folders with Content for a specific Program, for TV Shows that will be your Seasons, while Films it will just be the root
Db_Content = 'Folder_Content'                                                                   #Folder Content DB contains all supported content in a Program Folder
Db_YourFlix = 'YourFlix_Db'                                                                     #YourFlix DB is the meta information about YourFlix, it stores the DB version and more

Current_Program = None
Current_ContFolder = None
Current_Content = None

Current_MetaImages = None
Current_AllChannel = None
Current_FilmsChannel = None
Current_ShowsChannel = None

Db_List = [Db_YourFlix, Db_Channel, Db_ChProgram, Db_Program, Db_Img, Db_ImageType, Db_File, Db_ContFolder, Db_Content]

Db_Old = ['Img_Db', 'Content_Db', 'Program_Db', 'YourFlix_Db', 'FileType_Db']

FolderType = "Folder"
VideoType = "Video"
ImageType = "Image"

SupportedVideos = ['MP4', 'WebM', 'Ogg']                                                        #Default Supported Video (limited by the HTML5 Video)
SupportedImg = ['PNG', 'BMP', 'GIF', 'ICO', 'JPEG', 'JPG']                                      #Default Supported Image Types (limited by web standards, all images should be compatible with all browsers)
FileTypes = ['Folder']                                                                          #Don't touch

DefaultChannels = ['All', 'Films', 'Shows']                                                     #Default Channels which are created

ScannerIgnore = ['$RECYCLE.BIN', '.YF-IMG', '.YF-META', 'System Volume Information']            #These will be the folders which if they exist will be ignored since they are either created by the OS, or we want them ignored

MetaFolder = ".YF-META"                                                                         #This is the tagged meta folder