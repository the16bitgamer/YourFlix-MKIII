#! /usr/bin/env python

Phys_ConfigLoc = '/etc/yourflix/yourflix.config'
Phys_DbLoc = '/usr/share/yourflix/yourflix.db'
Phys_HtmlLoc = "/var/www/html"
MetaFolder = "YF-META"

Packages = ["apache2","python3-pip","sqlite"]
PythonModuals = [ ["sqlite3","pysqlite3.tar.gz","pysqlite3"],
                    ["inotify","inotify.tar.gz","inotify"],
                    ["blkinfo", "blkinfo.tar.gz", "blkinfo"] ]