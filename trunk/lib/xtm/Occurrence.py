# Author: Edvardas Scerbavicius
# E-mail: edvardas@gmail.com
""" Occurrence class
    http://www.topicmaps.org/xtm/#desc-occurrence
"""

from xtm.ResourceRef import ResourceRef
from xtm.InstanceOf import InstanceOf

class Occurrence:
    """ Occurrence class
        http://www.topicmaps.org/xtm/#desc-occurrence
    """
    def __init__(self, uri=""):
        """Initialize Occurrence object. (uri="") - Add ResourceRef object with given uri"""
        self._children = []
        if uri: self.setResourceRef(ResourceRef(uri))

    def getResourceRef(self):
        """Return ResourceRef object or "" """
        resourceRefChildren = [resourceRef for resourceRef in self._children if isinstance(resourceRef, ResourceRef)]
        return (resourceRefChildren and [resourceRefChildren[0]] or [""])[0]

    def setResourceRef(self, resourceRef):
        """Add ResourceRef object"""
        self.addChild(resourceRef)

    def getInstanceOf(self):
        """Return InstanceOf object or "" """
        instanceOfChildren = [instanceOf for instanceOf in self._children if isinstance(instanceOf, InstanceOf)]
        return (instanceOfChildren and [instanceOfChildren[0]] or [""])[0]

    def setInstanceOf(self, instanceOf):
        """Add InstanceOf object"""
        self.addChild(instanceOf)

    def addChild(self, child):
        """Add object (:ResourceRef or :InstanceOf)"""
        self._children.append(child)

    def __str__(self):
        """Return XTM:str representation of Occurrence object"""
        return """<occurrence>%s%s</occurrence>""" % (self.getInstanceOf(), self.getResourceRef())
