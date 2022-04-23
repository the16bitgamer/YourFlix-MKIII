#! /usr/bin/env python
ConfigVersion = 3

Phys_ConfigLoc = '/etc/yourflix/yourflix.config'
PyModulesLoc = '/etc/yourflix/lib'
Phys_DbLoc = '/usr/share/yourflix/yourflix.db'
Phys_HtmlLoc = "/var/www/html"
MetaFolder = "YF-META"

Packages = ["apache2","python3-pip","sqlite"]

#[module name], [local package file name], [network package name]
PythonModuals = [ ["sqlite3","pysqlite3.tar.gz","pysqlite3"],
                    ["inotify","inotify.tar.gz","inotify"],
                    ["blkinfo", "blkinfo.tar.gz", "blkinfo"],
                    ["sh", "sh.tar.gz", "sh"] ]

PluginPyModuales = []

#[Drive ID], [FS], [Mount Loc]
MountedDrives = []