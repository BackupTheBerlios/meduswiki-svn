# Author: Edvardas Scerbavicius
# E-mail: edvardas@gmail.com
""" SimpleDataStore class
    If you want to implement new DataStore: implement class with interface equal of this. 
"""

import os.path, time, re
from time import strftime, localtime
from medus.cfg import Config

class SimpleDataStore:
    """SimpleDataStore: uses file system for data storage;
       'content_path' must be added to Config before, instanciating object of this class
    """
    def __init__(self):
        """Initilize SimpleDataStore
           'content_path' must be added to Config before, instanciating object of this class
        """
        self.content_path = Config.get('content_path')

    def exists(self, id):
        """Return True, if (id) file exists"""
        return os.path.exists(os.path.join(self.content_path, id))

    def read(self, id):
        """Return (id) file content"""
        file_path = os.path.join(self.content_path, id)
        text = ''
        if os.path.isfile(file_path):
            infile = open(file_path, "r")
            text = infile.read()
            infile.close()
        return text 

    def write(self, id, content):
        """(id, content) write content to id:file"""
        outfile = open(os.path.join(self.content_path, id), "w")
        outfile.write(content)
        outfile.close()

    def remove(self, id):
        """Delete file(id) from data storage"""
        os.remove(os.path.join(self.content_path, id))

    def listdata(self):
        """Return list of wiki files(names)"""
        return [file for file in os.listdir(self.content_path) \
                if os.path.isfile(os.path.join(self.content_path, file))]

    def getchanges(self, count=None):
        """Return information about (recently modified files) changes in datastore
           (count=None) - number of files (if=None, then all files will be listed)
           -> [(filename, date, time)*]
        """
        items = [(os.path.getmtime(os.path.join(self.content_path, file)), file) \
                 for file in self.listdata()]
        items.sort()
        items.reverse()

        if count:
            count = (len(items) < count and [len(items)] or [count])[0]
        else:
            count = len(items)

        datefmt = '%A, %d %B %Y'
        timefmt = '%H:%M'

        return [(items[i][1], strftime(datefmt, localtime(items[i][0])), strftime(timefmt, localtime(items[i][0]))) \
                for i in range(0, count)]

    def search(self, str):
        "Search data store. (str) -> [(filename, number of matches)*]"
        str_re = re.compile(str, re.IGNORECASE)
        found = []

        for file in self.listdata():
            count = len(str_re.findall(self.read(file)))
            if count:
                found.append((count, file))

        found.sort()
        found.reverse()
        return found
