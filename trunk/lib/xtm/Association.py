# Author: Edvardas Scerbavicius
# E-mail: edvardas@gmail.com
""" Association class
    http://www.topicmaps.org/xtm/#desc-association
"""

from xtm.InstanceOf import InstanceOf 
from xtm.Member import Member

class Association:
    """ Association class
        http://www.topicmaps.org/xtm/#desc-association
    """
    def __init__(self, id):
        """Initialize Association object with a given id:int"""
        self._id = id
        self._children = []

    def getId(self):
        """Return id of the Association object"""
        return self._id

    def addChild(self, child):
        """Add object (:Member or :InstanceOf) to the Association"""
        self._children.append(child)

    def getInstanceOfList(self):
        """Return list of the :InstanceOf objects for this Association"""
        return [instanceOf for instanceOf in self._children if isinstance(instanceOf, InstanceOf)]

    def getMemberList(self):
        """Return list of the :Member objects for this Association"""
        return [member for member in self._children if isinstance(member, Member)]

    def __str__(self):
        """Return XTM:str representation of Association object"""
        children = "".join([str(child) for child in self._children])
        return """<association id="%s">%s</association>""" % (self._id, children)
