# Author: Edvardas Scerbavicius
# E-mail: edvardas@gmail.com
""" TopicMap class
    http://www.topicmaps.org/xtm/#desc-topic-map
"""

from xtm.Topic import Topic
from xtm.Association import Association
from xtm.Exceptions import IdExistsError
from xml.dom import minidom

ns_xlink = "http://www.w3.org/1999/xlink"
ns_xtm = "http://www.topicmaps.org/xtm/1.0/"

class TopicMap:
    """ TopicMap class
        http://www.topicmaps.org/xtm/#desc-topic-map
    """
    def __init__(self, id, encoding="utf-8"):
        """Initialize TopicMap object. (id, encoding="utf-8") - set id and xml encoding"""
        self._id = id
        self._encoding = encoding
        self.topics = {}
        self.associations = {} # dict, so associations could be removeByid

    def exportxml(self, filename):
        """Save TopicMap xml representation to file"""
        if filename:
           try:
              f = open(filename, 'w')
              domTM = minidom.parseString(str(self))
              #content = domTM.toxml(enc)
              content = domTM.toprettyxml('\t', '\n', self._encoding)
              f.write(content)
           finally:
              f.close()

    def getId(self):
        """Return TopicMap id"""
        return self._id

    def addChild(self, child):
        """Add object (:Topic or :Association)"""
        if isinstance(child, Topic):
           self.addTopic(child)
        if isinstance(child, Association):
           self.addAssociation(child)

    def addTopic(self, topic):
        """Add Topic object. Throws IdExistsError exception if Topic with such id already exists"""
        id = topic.getId()
        if id in self.topics.keys():
            raise IdExistsError(id)

        self.topics[id] = topic

    def addAssociation(self, association):
        """Add Association object. Throws IdExistsError exception if Association with such id already exists"""
        id = association.getId()
        if id in self.associations.keys():
            raise IdExistsError(id)
        
        self.associations[id] = association

    def removeAssociation(self, id):
        """Remove Association with given id"""
        del self.associations[id]

    def getTopics(self):
        """Return list of Topics"""
        return self.topics.values()

    def getAssociations(self):
        """Return list of Associations"""
        return self.associations.values()
     
    def getChildren(self):
        """Return list list of Topics and Associations or "" """
        children = self.topics.values() + self.associations.values()
        return (children and [children] or [""])[0]

    def __str__(self):
        """Return XTM:str representation of TopicMap object"""
        childs = "".join([str(child) for child in self.getChildren()])
        return """<topicMap xmlns="%s" xmlns:xlink="%s" id="%s">%s</topicMap>""" \
               % (ns_xtm, ns_xlink, self._id, childs)

    def removeTopic(self, id):
        """Remove Topic with given id:str"""
        del self.topics[id]
