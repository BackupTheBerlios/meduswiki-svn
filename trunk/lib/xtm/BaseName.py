# Author: Edvardas Scerbavicius
# E-mail: edvardas@gmail.com
""" BaseName class
    http://www.topicmaps.org/xtm/#desc-base-name
"""

from xtm.BaseNameString import BaseNameString
from xtm.Scope import Scope

class BaseName:
    """ BaseName class
        http://www.topicmaps.org/xtm/#desc-base-name
    """
    def __init__(self, name=None):
        """(name=None) -- initialize BaseName object with a given name:str"""
        self._children = []
        if name: self.setBaseNameString(BaseNameString(name))

    def getBaseNameString(self):
        """Return BaseNameString object, if such exists (otherwise return "")"""
        nameStrChildren = [nameStr for nameStr in self._children if isinstance(nameStr, BaseNameString)]
        return (nameStrChildren and [nameStrChildren[0]] or [""])[0]
       
    def setBaseNameString(self, baseNameString):
        """Add object baseNameString:BaseNameString"""
        self.addChild(baseNameString)
                                                  
    def setScope(self, scope):
        """Add object scope:Scope"""
        self.addChild(scope)

    def getScope(self):
        """Return Scope object, if such exists (otherwise return "")"""
        scopeChildren = [scope for scope in self._children if isinstance(scope, Scope)]
        return (scopeChildren and [scopeChildren[0]] or [""])[0]

    def addChild(self, child):
        """Add object (:BaseNameString or :Scope) to the BaseName"""
        self._children.append(child)

    def __str__(self):
        """Return XTM:str representation of BaseName object"""
        return "<baseName>%s%s</baseName>" % (self.getScope(), self.getBaseNameString())
