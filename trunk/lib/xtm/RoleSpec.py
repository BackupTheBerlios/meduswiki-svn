# Author: Edvardas Scerbavicius
# E-mail: edvardas@gmail.com
""" RoleSpec class
    http://www.topicmaps.org/xtm/#elt-roleSpec
"""

from xtm.TopicRef import TopicRef

class RoleSpec:
    """ RoleSpec class
        http://www.topicmaps.org/xtm/#elt-roleSpec
    """
    def __init__(self, id=None):
        """Initialize RoleSpec object. (id=None) - Add TopicRef object with given id"""
        self._children = []
        if id: self.setTopicRef(TopicRef(id))

    def setTopicRef(self, topicRef):
        """Add TopicRef object"""
        self.addChild(topicRef)

    def getTopicRef(self):
        """Return TopicRef object or "" """
        topicRefChildren = [topicRef for topicRef in self._children if isinstance(topicRef, TopicRef)]
        return (topicRefChildren and [topicRefChildren[0]] or [""])[0]

    def addChild(self, child):
        """Add object (:TopicRef)"""
        self._children.append(child)

    def __str__(self):
        """Return XTM:str representation of RoleSpec object"""
        return """<roleSpec>%s</roleSpec>""" % self.getTopicRef()
