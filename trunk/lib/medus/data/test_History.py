# (c) Edvardas Scerbavicius 2005.01.27
# this is a test for MedusWiki version history system

from History import History
from random import randint
import os

history = History('.')
filename = 'TestTest'


class TestHistory:

    def setup_method(self, method):
        """creates temporary file"""
        open(filename, 'wt').write('test')


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
            open(filename, 'wt').write('test%s' % x)


    def test_sorted(self):
        rand = randint(0,10)

        for x in range(0, rand): # every time 'save' is called, new version is created.
            history.save(filename)

        templist = ['%s.%s' % (filename, x) for x in range(0, rand)]
        assert history.listVersions(filename) ==  templist
