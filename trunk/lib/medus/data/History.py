# (c) Edvardas Scerbavicius 2005.01.27
# this MedusWiki version history system
#from os import listdir
from os.path import exists, join, getmtime
from os import environ
import tarlib
import tar

class History:

    def __init__(self, dir):
        """dir:directoty path"""
        self.dir = dir


    def save(self, filename):
        """add new version file to the version archive"""
        archive = join(self.dir, '%s.tar' % filename)
        filepath = join(self.dir, filename)
        copy = open(filepath).read()
        content = []
        name = str(environ.get('REMOTE_ADDR'))
        
        if exists(archive):
            fp = open(archive, 'r')
            tara = tarlib.TAR(fp, cached=1)
            content = [tar.TarEntry(entry.name, entry.getdata(), mtime=entry.mtime, uname=entry.uname) for entry in tara] # save old data
            fp.close()

        newversion = '%s.%s' % (filename, len(self.listVersions(filename)))
        content.append(tar.TarEntry(newversion, copy, mtime=getmtime(filepath), uname=name)) # append new data
        tarstr = tar.tarit(content)
        open(archive, 'w').write(tarstr)

#        open("%s.%s" % (filename, len(self.listVersions(filename))), 'w').write(copy)


    def listVersions(self, filename):
        """return sorted dict of saved file versions: file:tarlib.TarEntry"""
        archive = join(self.dir, '%s.tar' % filename)
        filedict = {}
        
        if exists(archive):
            fp = open(archive, 'r')
            filedict = dict(tarlib.TAR(fp, cached=1).items())
            fp.close()

#        filelist = [file for file in listdir(self.dir) if file.startswith("%s." % filename)]
#        filelist.sort(cmp_fileversions) #tarlib returns sorted keys
        return filedict


    def getdata(self, filename, version):
        """return file.version content"""
        archive = join(self.dir, '%s.tar' % filename)
        version = '%s.%s' % (filename, version)
        data = ''
        
        if exists(archive):
            fp = open(archive, 'r')
            tara = tarlib.TAR(fp, cached=1)
            data = tara.getit(version).getdata()
            fp.close()

        return data
            
    
def cmp_fileversions(a, b):
    """cmp('file.0', 'file.1')"""
    aint = int(a.split('.').pop()) 
    bint = int(b.split('.').pop())
    return cmp(aint, bint)
