# (c) Edvardas Scerbavicius 2005.01.27
# this is a test for MedusWiki version history system

from History import History, cmp_fileversions
from random import randint
import os

history = History('.')
filename = 'TestTest'


class TestHistory:

    def setup_method(self, method):
        """creates initial temporary file"""
        open(filename, 'wt').write('test0')


    def teardown_method(self, method):
        """removes temporary files"""
        for file in os.listdir('.'):
            if file.startswith(filename):
                os.remove(file)

        
    def test_dir(self):
        assert history.dir == '.'


    def test_versions(self):
        rand = randint(0,10)

        for x in range(0, rand): # every time 'save' is called, new version is created.
            assert len(history.listVersions(filename)) == x
            history.save(filename)


    def test_filenames(self):
        rand = randint(0,30)

        for x in range(0, rand):
            history.save(filename)

        templist = ['%s.%s' % (filename, x) for x in range(0, rand)]

        files = history.listVersions(filename).keys()
        files.sort(cmp_fileversions)

        assert files == templist


    def test_version_content(self):
        rand = randint(0,10)

        for x in range(0, rand):
            history.save(filename) # save old content
            open(filename, 'wt').write('test%s' % (x+1)) # create new content

        for x in range(0, rand):
            assert history.getdata(filename, version=x) == 'test%s' % x


