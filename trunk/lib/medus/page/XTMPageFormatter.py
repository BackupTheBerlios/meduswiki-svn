# Author: Edvardas Scerbavicius
# E-mail: edvardas@gmail.com
""" XTMPageFormatter class
    Extends ZPTPageFormatter
"""

from ZPTPageFormatter import ZPTPageFormatter
from xtm.util import cmp_alpha, cmp_simple
from medus.cfg import Config

class XTMPageFormatter(ZPTPageFormatter):
    """Obtains XTM data from xtm.Handler and puts it into templates context
       'DataStore', 'ContentFormatter', 'encoding' and 'XTMHandler' objects must be added
       to Config before, instanciating object of this class
    """
    def __init__(self):
        """Initilize XTMPageFormatter
           'DataStore', 'ContentFormatter', 'encoding' and 'XTMHandler' objects must be added
           to Config before, instanciating object of this class
        """
        self.xtm = Config.get('XTMHandler')
        ZPTPageFormatter.__init__(self)

    def _context_toc(self, context, fields):
        """Add objects to the context for zpt template toc.zpt"""
        keys = self.xtm.getTopicMap().topics.keys()
        keys.sort(cmp_alpha)
        context.addGlobal ("topics", keys)
        return context

    def _context_view(self, context, fields):
        """Add objects to the context for zpt template view.zpt"""
        wn = fields['wn']
        context.addGlobal ("title", wn)
        context.addGlobal ("content", self.formatter.format(self.datastore.read(wn)).decode(self.encoding))

        associations = self.xtm.getTopicAssociations(wn)
        associations.sort(cmp_simple)
      
        context.addGlobal ("associations", associations)
        return context

    def _context_edit(self, context, fields):
        """Add objects to the context for zpt template edit.zpt"""
        wn = fields['wn']
        context.addGlobal ("title", wn)
        context.addGlobal ("content", self.datastore.read(wn).decode(self.encoding))

        roles = self.xtm.getRoles()
        roles.sort(cmp_alpha)
        context.addGlobal ("roles", roles)

        topics = self.xtm.getTopics()
        topics.sort(cmp_alpha)
        context.addGlobal ("topics", topics)
     
        associations = self.xtm.getTopicAssociations(wn)
        associations.sort(cmp_simple)
        context.addGlobal ("associations", associations)

        couldelete = (self.xtm.hasTopic(wn) and not self.xtm.isBuiltIn(wn)) and "True" or ''
        context.addGlobal ("couldelete", couldelete)

        exists = self.xtm.hasTopic(wn)
        context.addGlobal ("exists", exists)
      
        return context


    def _context_search(self, context, fields):
        """Add objects to the context for zpt template search.zpt"""

        roles = self.xtm.getRoles()
        roles.sort(cmp_alpha)
        context.addGlobal ("roles", roles)

        topics = self.xtm.getTopics()
        topics.sort(cmp_alpha)
        context.addGlobal ("topics", topics)

        role = rtopic = None
        query = fields.get("query")
        if query:
            context.addGlobal ("query", query.decode(self.encoding))
            context.addGlobal ("searchresults", self.datastore.search(query))
            context.addGlobal ("search", True)

        if fields.get('form') == 'filter':
           if fields.get('rtopic') != 'any':
               rtopic = fields['rtopic']

           if fields.get('role') != 'any':
               role = fields['role']

           filterresults = self.xtm.filter(role, rtopic)
           context.addGlobal ("filterresults", filterresults)
           context.addGlobal ("filter", True)

        # <select><option> of previous filter:
        context.addGlobal ("getrole", role)
        context.addGlobal ("gettopic", rtopic)
        return context
