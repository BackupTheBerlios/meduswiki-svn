# Author: Edvardas Scerbavicius
# E-mail: edvardas@gmail.com
""" XTM file parser. """

from xml.dom import minidom

from xtm.TopicMap import TopicMap 
from xtm.Topic import Topic 
from xtm.BaseNameString import BaseNameString
from xtm.BaseName import BaseName
from xtm.Association import Association
from xtm.InstanceOf import InstanceOf
from xtm.TopicRef import TopicRef
from xtm.Scope import Scope
from xtm.Occurrence import Occurrence
from xtm.ResourceRef import ResourceRef
from xtm.Member import Member
from xtm.RoleSpec import RoleSpec 

from xtm.TopicMap import ns_xlink

class Parser:
    """ XTM file parser. """
    def __init__(self, encoding="utf-8"):
        """Initialize Parser object. (encoding="utf-8") - set TopicMap xml encoding"""
        self._encoding = encoding
        
    def parseNode(self, node):
        """get XTM object representation of dom node"""
        return getattr(self, "_parse_" + node.nodeName)(node)

    def _addChild(self, xtmObject, xtmNode):
        """(xtmObject, xtmNode), parse xtmNode and add objects to xtmObject"""
        for child in xtmNode.childNodes:
            if hasattr(self, "_parse_" + child.nodeName):
                xtmObject.addChild(self.parseNode(child))

    def parse(self, filename):
        """parse xtm file -> TopicMap object"""
        xml = minidom.parse(filename)
        child = xml.firstChild
        return self.parseNode(child)

    def parseString(self, string):
        """parse xtm string -> TopicMap object"""
        xml = minidom.parseString(string)
        child = xml.firstChild
        return self.parseNode(child)

    def _parse_topicMap(self, tmNode):
        """parse topicMap node -> TopicMap"""
        id = tmNode.getAttribute("id")
        topicMap = TopicMap(id, self._encoding)
        self._addChild(topicMap, tmNode)
        return topicMap
            
    def _parse_topic(self, topicNode):
        """parse topic node -> Topic"""
        id = topicNode.getAttribute("id")
        topic = Topic(id)
        self._addChild(topic, topicNode)
        return topic

    def _parse_occurrence(self, occurrenceNode):
        """parse occurrence node -> Occurrence"""
        occurrence = Occurrence()
        self._addChild(occurrence, occurrenceNode)
        return occurrence

    def _parse_resourceRef(self, resourceRefNode):
        """parse resourceRef node -> ResourceRef"""
        href = resourceRefNode.getAttributeNS(ns_xlink, "href")
        return ResourceRef(href) 

    def _parse_instanceOf(self, instanceOfNode):
        """parse instanceOf node -> InstanceOf"""
        instanceOf = InstanceOf()
        self._addChild(instanceOf, instanceOfNode)
        return instanceOf

    def _parse_topicRef(self, topicRefNode):
        """parse topicRef node -> TopicRef"""
        href = topicRefNode.getAttributeNS(ns_xlink, "href")
        if href[0] == '#':
            href = href[1:]
        return TopicRef(href) 

    def _parse_baseName(self, baseNameNode):
        """parse baseName node -> BaseName"""
        baseName = BaseName()
        self._addChild(baseName, baseNameNode)
        return baseName

    def _parse_scope(self, scopeNode):
        """parse scope node -> Scope"""
        scope = Scope()
        self._addChild(scope, scopeNode)
        return scope

    def _parse_baseNameString(self, baseNameStringNode):
        """parse baseNameString node -> BaseNameString"""
        name = baseNameStringNode.firstChild.nodeValue
        return BaseNameString(name)

    def _parse_association(self, associationNode):
        """parse association node -> Association"""
        id = associationNode.getAttribute("id")
        association = Association(id)
        self._addChild(association, associationNode)
        return association

    def _parse_member(self, memberNode):
        """parse member node -> Member"""
        member = Member()
        self._addChild(member, memberNode)
        return member

    def _parse_roleSpec(self, roleSpecNode):
        """parse roleSpec node -> RoleSpec"""
        roleSpec = RoleSpec()
        self._addChild(roleSpec, roleSpecNode)
        return roleSpec
