# Author: Edvardas Scerbavicius
# E-mail: edvardas@gmail.com
""" Member class
    http://www.topicmaps.org/xtm/#desc-member
"""

from xtm.TopicRef import TopicRef
from xtm.RoleSpec import RoleSpec

class Member:
    """ Member class
        http://www.topicmaps.org/xtm/#desc-member
    """
    def __init__(self, id=None):
        """Initialize Member object. (id=None) - Add TopicRef object with given id"""
        self._children = []
        if id: self.setTopicRef(TopicRef(id))

    def setTopicRef(self, topicRef):
        """Add TopicRef object"""
        self.addChild(topicRef)
    
    def getTopicRef(self):
        """Return TopicRef object or "" """
        topicRefChildren = [topicRef for topicRef in self._children if isinstance(topicRef, TopicRef)]
        return (topicRefChildren and [topicRefChildren[0]] or [""])[0]

    def setRoleSpec(self, role):
        """Add RoleSpec object"""
        self.addChild(role)

    def getRoleSpec(self):
        """Return RoleSpec object or "" """
        roleSpecChildren = [roleSpec for roleSpec in self._children if isinstance(roleSpec, RoleSpec)]
        return (roleSpecChildren and [roleSpecChildren[0]] or [""])[0]

    def addChild(self, child):
        """Add object (:TopicRef or :RoleSpec)"""
        self._children.append(child)

    def __str__(self):
        """Return XTM:str representation of Member object"""
        return """<member>%s%s</member>""" % (self.getRoleSpec(), self.getTopicRef())

