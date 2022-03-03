#! /usr/bin/env python

ConfigLoc = '/etc/yourflix/yourflix.config'
DbLoc = '/usr/share/yourflix/yourflix.db'
HtmlLoc = "/var/www/html"

Packages = ["apache2","python3-pip","sqlite"]
PythonModuals = [ ["sqlite3","pysqlite3.tar.gz","pysqlite3"],
                    ["inotify","inotify.tar.gz","inotify"],
                    ["blkinfo", "blkinfo.tar.gz", "blkinfo"] ]