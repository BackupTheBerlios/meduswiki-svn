# Author: Edvardas Scerbavicius
# E-mail: edvardas@gmail.com
""" ZPTPageFormatter class
    If you want to implement new PageFormatter that uses ZPT:
    extend this class and create new _context_ methods. 
"""

from simpletal import simpleTAL, simpleTALES, simpleTALUtils
import os.path
from SimplePageFormatter import SimplePageFormatter
from medus.cfg import Config
 
class ZPTPageFormatter(SimplePageFormatter):
    """ ZPT page formatting
       'DataStore', 'ContentFormatter' and 'encoding' objects must be added to Config before,
       instanciating object of this class
       Local variables initialised in the Base class constructor:
         self.datastore
         self.formatter
         self.encoding
    """
    def getpage(self, fields):
        """fields - dict of HTTP pears. Returns formatted page string, according to fields['job']"""
        job = fields.get('job') or 'view'
        # Creat the context that is used by the template
        context = simpleTALES.Context(allowPythonPath=1)
        context.addGlobal ("cfg", {'version':Config.get('version'), 
                                      'link':Config.get('link'),
                                      'logo':Config.get('logo'), 
                                       'css':Config.get('css')})
        # Add objects into the template context
        context = getattr(self, "_context_" + job)(context, fields)
        # Open the template file
        templateFile = open(os.path.join(Config.get('zpt_path'), "".join([job, ".zpt"])), 'r')
        # Compile a template
        template = simpleTAL.compileHTMLTemplate (templateFile, self.encoding)
        # Close the template file
        templateFile.close()
        # Create fake file that lets print file as a string
        fastFile = simpleTALUtils.FastStringOutput()
        # Expand the template as HTML using this context
        template.expand(context, fastFile, self.encoding)
        return fastFile.getvalue() #yo people! it's ZPT content"
    
    def _context_view(self, context, fields):
        """Add objects to the context for zpt template view.zpt"""
        # Add a string to the context under the variable title
        wn = fields['wn']
        context.addGlobal ("title", wn)
        context.addGlobal ("content", self.formatter.format(self.datastore.read(wn)).decode(self.encoding))
        return context

    def _context_edit(self, context, fields):
        """add objects to the context for zpt template edit.zpt"""
        wn = fields['wn']
        context.addGlobal ("title", wn)
        context.addGlobal ("content", self.datastore.read(wn).decode(self.encoding))

        couldelete = self.datastore.exists(wn)
        context.addGlobal ("couldelete", couldelete)
        return context

    def _context_print(self, context, fields):
        """add objects to the context for zpt template print.zpt"""
        wn = fields['wn']
        context.addGlobal ("title", wn)
        context.addGlobal ("content", self.formatter.format(self.datastore.read(wn)).decode(self.encoding))
        return context
     
    def _context_toc(self, context, fields):
        """add objects to the context for zpt template toc.zpt"""
        wikipages =  self.datastore.listdata()
        wikipages.sort()
        context.addGlobal ("topics", wikipages)
        return context

    def _context_changes(self, context, fields):
        """add objects to the context for zpt template changes.zpt"""
        context.addGlobal ("changes", self.datastore.getchanges(20))
        return context

    def _context_search(self, context, fields):
        """add objects to the context for zpt template search.zpt"""
        query = fields.get('query')

        if query:
            context.addGlobal ("query", query.decode(self.encoding))
            context.addGlobal ("searchresults", self.datastore.search(query))                    

        return context
