# Author: Edvardas Scerbavicius
# E-mail: edvardas@gmail.com
""" Topic class
    http://www.topicmaps.org/xtm/#desc-topic
"""

from xtm.BaseName import BaseName
from xtm.InstanceOf import InstanceOf 
from xtm.Occurrence import Occurrence 

class Topic: 
    """ Topic class
        http://www.topicmaps.org/xtm/#desc-topic
    """
    def __init__(self, id):
        """Initialize Topic object. (id) - set Topic id"""
        self._id = id
        self._children = []

    def getId(self):
        """Return Topic id """
        return self._id

    def addChild(self, child):
        """Add object (:BaseName or :InstanceOf or :Occurrence)"""
        self._children.append(child)

    def getBaseNameList(self):
        """Return list of the :BaseName objects for this Topic"""
        return [baseName for baseName in self._children if isinstance(baseName, BaseName)]

    def getInstanceOfList(self):
        """Return list of the :InstanceOf objects for this Topic"""
        return [instanceOf for instanceOf in self._children if isinstance(instanceOf, InstanceOf)]

    def getOccurrenceList(self):
        """Return list of the :Occurrence objects for this Topic"""
        return [occurrence for occurrence in self._children if isinstance(occurrence, Occurrence)]

    def __str__(self): 
        """Return XTM:str representation of Topic object"""
        children = "".join([str(child) for child in self._children])
        return """<topic id="%s">%s</topic>""" % (self._id, children)

