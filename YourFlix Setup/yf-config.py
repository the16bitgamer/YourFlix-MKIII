import os

yfPublic = "/usr/share/yourflix/"
yfEct = "/etc/yourflix/"
yfSystemD = "/lib/systemd/system/"
yfSource = "./.YourFlix/"
pythonFilesToAdd = ['yf_AutoAddToDB.py', 'yf_AutoRemoveFromDB.py', 'yf_AutoUpdateDB.py',
    'yf_BuildContentDB.py', 'yf_Database.py', 'yf_DbBuilder.py',
    'yf_DbHandler.py', 'yf_ProgramBuilder.py', 'yf_scanner.py',
    'yf_ScanToDatabase.py', 'yf_RenameMetaFolders.py']

service = 'yourflix.service'
config = 'yourflix.config'

def CheckFolder(folderLoc):
    if not os.path.isdir(folderLoc) and folderLoc != yfSource:
        try:
            os.mkdir(folderLoc)
        except OSError:
            print ("Creation of the directory %s failed" % folderLoc)
            return False
    return True

def UpdateFile(fileLoc):
    if not os.path.isfile(fileLoc):
        f = open(fileLoc, "x")
    else:
        f = open(fileLoc, "w")
    return f

def BuildSystemD():

    if(CheckFolder(yfPublic) and CheckFolder(yfSystemD) and CheckFolder(yfSource) and CheckFolder(yfEct)):

        for _file in pythonFilesToAdd:
            sourceFile = open(yfSource + _file, "r")

            file = UpdateFile(yfPublic + _file)
            file.write(sourceFile.read())

        configSource = open(yfSource + config, "r")
        file = UpdateFile(yfEct + config)
        file.write(configSource.read())
        
        serviceSource = open(yfSource + service, "r")
        file = UpdateFile(yfSystemD + service)
        file.write(serviceSource.read())
        
        os.system('sudo chmod 644 /lib/systemd/system/yourflix.service')
        os.system('sudo chmod +x /usr/share/yourflix/yf_scanner.py')
        
        print("YourFlix Auto Run has been configured, please run:\nsudo systemctl daemon-reload\n\nTo load the service.\nIf it's your first time run:\nsudo systemctl start yourflix.service\n\nor if you've updated the service run:\nsudo systemctl restart yourflix.service\n\nThe database will be automatically build and update itself. Though there is a manual scan option ;)")
    
if __name__ == '__main__':
    BuildSystemD()
