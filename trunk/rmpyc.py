#!/usr/bin/python
import fnmatch, os, os.path

def rmpyc(cwd, ext):
    """Recursively removes all files from cwd with ext='*.pyc'"""
    for filename in os.listdir(cwd):
        path = os.path.join(cwd, filename)

        if os.path.isdir(path):
            rmpyc(path, ext)
            
        elif fnmatch.fnmatch(filename, ext):
            print "rm ", path
            os.remove(path)

rmpyc('.', '*.pyc')
rmpyc('.', '*.py~')

        
