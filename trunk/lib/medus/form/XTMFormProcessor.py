# Author: Edvardas Scerbavicius
# E-mail: edvardas@gmail.com
""" XTMFormProcessor class
    Extends SimpleFormProcessor
"""

from SimpleFormProcessor import SimpleFormProcessor
from medus.cfg import Config

class XTMFormProcessor(SimpleFormProcessor):
    """Obtains XTM data from forms and saves/removes it into/from xtm file
      'DataStore' and 'XTMHandler' objects must be added to Config before, instanciating object of this class
    """
    def __init__(self):
        """Initilize XTMFormProcessor
          'DataStore' and 'XTMHandler' objects must be added to Config before, instanciating object of this class
        """
        self.xtm = Config.get('XTMHandler') 
        SimpleFormProcessor.__init__(self)

    def _form_save(self, fields):
        """Process save form input. Create new XTM Topic ir such not exists"""
        wn = fields['wn']
        topic_exists = self.xtm.hasTopic(wn)

        self.datastore.write(wn, fields['text'])

        if not topic_exists:
            self.xtm.addTopic(wn)

    def _form_delete(self, fields):
        """Remove given wikifile and XTM information about it"""
        wn = fields['wn']
        file_exists = self.datastore.exists(wn)

        if self.xtm.hasTopic(wn) and not self.xtm.isBuiltIn(wn):
            self.xtm.removeTopic(wn)
            # remove all non builtin associations, that has no realy existing members
            for assid, role, topic in self.xtm.getTopicAssociations(wn):
                if not self.xtm.hasTopic(topic):
                    self.xtm.removeAssociation(assid)
       
        if file_exists:
            self.datastore.remove(wn)
      
    def _form_associate(self, fields):
        """Create new XTM association"""
        self.xtm.addAssociation(fields['wn'], fields['role'], fields['rtopic'])

    def _form_removeassoc(self, fields):
        """Remove selected XTM associations"""
        assids = ('assids' in fields and fields['assids'] or '')

        if assids: 
            if type(assids) == type([]):
                for id in assids:
                   self.xtm.removeAssociation(id)
            else:
                self.xtm.removeAssociation(assids)

    def _form_filter(self, fields):
        """Process filter query"""
        # redirect output to search template
        fields['job'] = 'search'
