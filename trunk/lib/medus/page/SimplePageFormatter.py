# Author: Edvardas Scerbavicius
# E-mail: edvardas@gmail.com
""" SimplePageFormatter class
    If you want to implement new PageFormatter: extend this class and create new getpage method. 
"""
from medus.cfg import Config
 
class SimplePageFormatter:
    """The most simple Wiki page formatting taken from wypy
       'DataStore', 'ContentFormatter' and 'encoding' objects must be added to Config before,
       instanciating object of this class
    """
    def __init__(self):
        """Initilize PageFormatter
           'DataStore', 'ContentFormatter' and 'encoding' objects must be added to Config before,
           instanciating object of this class
        """
        self.datastore = Config.get('DataStore')
        self.formatter = Config.get('ContentFormatter')
        self.encoding = Config.get('encoding')

    def getpage(self, fields):
        """fields - dict of HTTP pears. Returns formatted page string, according to fields['job']"""
        job = fields.get('job') or 'view'
        wn = fields['wn']
        return {
           'view':'<h1>Wiki:%s</h1> (' \
           '<a href=?wn=%s&amp;job=edit>edit me</a>)<p>%s' \
           % (wn, wn, self.formatter.format(self.datastore.read(wn)) or wn),
           'edit': '<form action=?%s method=POST><h1>%s<input type=hidden name=wn' \
           ' value=%s><input type=hidden name=form value=save><input type=submit></h1>' \
           '<textarea name=text rows=15 cols=80>%s</textarea></form>' \
           % (wn, self.formatter.format(wn), wn, self.datastore.read(wn) or "Describe %s" % wn),
           }.get(job)
