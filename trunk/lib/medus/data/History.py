# (c) Edvardas Scerbavicius 2005.01.27
# this MedusWiki version history system
#from os import listdir
from os.path import exists, join
import tarlib
import tar

class History:

    def __init__(self, dir):
        """dir:directoty path"""
        self.dir = dir


    def save(self, filename):
        """add new version file to the version archive"""
        archive = join(self.dir, '%s.tar' % filename)
        copy = open(join(self.dir, filename)).read()
        content = []
        
        if exists(archive):
            fp = open(archive, 'r')
            tara = tarlib.TAR(fp, cached=1)
            content = [(entry.name, entry.getdata()) for entry in tara] # save old data
            fp.close()

        content.append(('%s.%s' % (filename, len(self.listVersions(filename))), copy)) # append new data
        tarstr = tar.tar(content)
        open(archive, 'w').write(tarstr)

#        open("%s.%s" % (filename, len(self.listVersions(filename))), 'w').write(copy)


    def listVersions(self, filename):
        """return sorted list of saved file versions"""
        archive = join(self.dir, '%s.tar' % filename)
        filelist = []
        
        if exists(archive):
            fp = open(archive, 'r')
            tara = tarlib.TAR(fp, cached=1)
            filelist = tara.keys()
            fp.close()

#        filelist = [file for file in listdir(self.dir) if file.startswith("%s." % filename)]
#        filelist.sort(cmp_fileversions) #tarlib returns sorted keys
        return filelist
            
    
def cmp_fileversions(a, b):
    """cmp('file.0', 'file.1')"""
    aint = int(a.split('.').pop()) 
    bint = int(b.split('.').pop())
    return cmp(aint, bint)
