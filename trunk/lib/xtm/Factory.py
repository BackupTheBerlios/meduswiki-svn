# Author: Edvardas Scerbavicius
# E-mail: edvardas@gmail.com
""" Factory class
    Helps to create XTM objects        
"""

from xtm.TopicMap import TopicMap
from xtm.Topic import Topic
from xtm.Association import Association
from xtm.BaseNameString import BaseNameString
from xtm.BaseName import BaseName
from xtm.ResourceRef import ResourceRef
from xtm.TopicRef import TopicRef
from xtm.Scope import Scope
from xtm.Occurrence import Occurrence
from xtm.Member import Member
from xtm.RoleSpec import RoleSpec
from xtm.InstanceOf import InstanceOf

class Factory:
    """ Factory class
        Helps to create XTM objects        
    """
    def createTopicMap(self, id):
        """Return new TopicMap objct with given id"""
        return TopicMap(id)

    def createTopic(self, id):
        """Return new Topic object with given id"""
        return Topic(id)

    def createAssociation(self, id):
        """Return new Association object with given id"""
        return Association(id)

    def createBaseNameString(self, name=""):
        """Return new BaseNameString object with given (name="")"""
        return BaseNameString(name)

    def createBaseName(self, name=""):
        """Return new BaseName object with given (name="") """
        return BaseName(name)

    def createResourceRef(self, uri=""):
        """Return new ResourceRef object with given (uri="")"""
        return ResourceRef(uri)

    def createTopicRef(self, id=""):
        """Return new TopicRef object with given (id="")"""
        return TopicRef(id)

    def createScope(self, id=""):
        """Return new Scope object with given (id="")"""
        return Scope(id)

    def createOccurrence(self, uri=""):
        """Return new Occurence object with given (uri="")"""
        return Occurrence(uri)

    def createMember(self, id=""):
        """Return new Member object with given (id="")"""
        return Member(id)

    def createRoleSpec(self, id=""):
        """Return new RoleSpec object with given (id="")"""
        return RoleSpec(id)

    def createInstanceOf(self, id=""):
        """Return new InstanceOf object with given (id="")"""
        return InstanceOf(id)
