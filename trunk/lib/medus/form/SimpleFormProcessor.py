# Author: Edvardas Scerbavicius
# E-mail: edvardas@gmail.com
""" SimpleFormProcessor class
    If you want to implement new FormProcessor: extend this class and create new _form_ methods. 
"""
from medus.cfg import Config

class SimpleFormProcessor:
    """HTML Form processor. Every form must have hidden attribute name.
       Method _form_name will be called to process information from this form.
       'DataStore' object must be added to Config before, instanciating object of this class
    """
    def __init__(self):
        """Initilize FormProcessor
           'DataStore' object must be added to Config before, instanciating object of this class
        """
        self.datastore = Config.get('DataStore')

    def process(self, fields):
        """Process form input (fields) dict"""
        formname = fields['form']
        getattr(self, "_form_" + formname)(fields)

    def _form_save(self, fields):
        """Process save form input"""
        self.datastore.write(fields['wn'], fields['text'])

    def _form_search(self, fields):
        """Process search query"""
        # redirect output to the search:template
        fields['job'] = 'search'

    def _form_delete(self, fields):
        """Remove given wikifile"""
        wn = fields['wn']
        file_exists = self.datastore.exists(wn)

        if file_exists:
            self.datastore.remove(wn)

