# Author: Edvardas Scerbavicius
# E-mail: edvardas@gmail.com
""" Handler class
    Adds specific for MedusWiki funcionality to the TopicMap object
"""

from xtm.TopicMap import TopicMap 
from xtm.Topic import Topic
from xtm.Association import Association
from xtm.Member import Member
from xtm.RoleSpec import RoleSpec
from xtm.Parser import Parser
from xtm.Occurrence import Occurrence
from xtm.BaseName import BaseName
from xtm.InstanceOf import InstanceOf
import os.path

class Handler:
    """ Handler class
        Adds specific for MedusWiki funcionality to the TopicMap object
    """
    def __init__(self, filename=None):
        """Initialize Handler object. Input - path to xtm file
        (filename=None) - if xtm file exists, then parse it, otherwise create new TopicMap
        """
        if filename and os.path.exists(filename):
            parser = Parser()
            self._tm = parser.parse(filename)
        else:
            self._tm = TopicMap("0")

        self._filename = filename

    def setTopicMap(self, tm):
        """(tm:TopicMap) - change currently wrapped TopicMap with given one"""
        self._tm = tm

    def getTopics(self):
        """Return list of topic id's """
        return self._tm.topics.keys()

    def getTopicMap(self):
        """Return TopicMap"""
        return self._tm

    def getId(self):
        """Return id of decorated TopicMap"""
        return self._tm.getId()

    def hasTopic(self, name):
        """(name:str) - return True if such topic exists"""
        return name in self._tm.topics

    def addTopic(self, topicid, occurrence_uri=None, name=None, instance_of=None):
        """(topicid:str, occurence_uri:str, name:str; instance_of:str)
        (topicid, occurrence_uri=None, name=None, instance_of=None)
        create new topic, and add it to the topicmap"""
        topic = Topic(topicid)
           
        if occurrence_uri:
            topic.addChild(Occurrence(occurrence_uri))

        if name:
            topic.addChild(BaseName(name))

        if instance_of:
            topic.addChild(InstanceOf(instance_of))

        self._tm.addTopic(topic)
        self._tm.exportxml(self._filename)

    def removeTopic(self, topicid):
        """(topicid:str) - remove topic from topicmap"""
        self._tm.removeTopic(topicid)
        self._tm.exportxml(self._filename)

    def removeAssociation(self, assid):
        """(assid:str) - remove association"""
        self._tm.removeAssociation(assid)
        self._tm.exportxml(self._filename)

    def isBuiltIn(self, id):
        """(id:str) - return True if topic is XTM instanceOf 'builtIn'"""
        instances = self._tm.topics[id].getInstanceOfList()
        if instances:
            for instance in instances:
               if instance.getTopicRef().id == 'builtIn':
                   return True
        return False

    def addAssociation(self, ltopicid, lrole, rtopicid, rrole=None):
        """(ltopicid:str, lrole:str, rtopicid:str, rrole=None):
        - create new association"""
        # create uid
        ids = [int(id) for id in self._tm.associations.keys()]
        uid = (ids and (max(ids) + 1) or 0)

        association = Association(uid)
        lmember = Member(ltopicid)
        rmember = Member(rtopicid)

        #if lrole:
        lmember.setRoleSpec(RoleSpec(lrole))

        if rrole:
            rmember.setRoleSpec(RoleSpec(rrole))
        else:
            rmember.setRoleSpec(RoleSpec(self.getOppositeRole(lrole)))

        association.addChild(lmember)
        association.addChild(rmember)

        self._tm.addAssociation(association)
        self._tm.exportxml(self._filename)

    def getOppositeRole(self, topicid):
        """(topicid:str) - return topicid, of opposite role. Opposite topic is topic, that has association
        'oppositeRole' with given one.
        If such topic doesn't exists return 'relatedTo'
        """
        for assid, role, topic in self.getTopicAssociations(topicid):
            ass = self._tm.associations[assid]

            for member in ass.getMemberList():
                if member.getRoleSpec() and member.getTopicRef().id == topic:
                    if member.getRoleSpec().getTopicRef().id == 'oppositeRole':
                        return topic

        return 'relatedTo'


    def getTopicAssociations(self, topicid):
        """(topicid: str) - return information about topic associations -> [(assid, role, topic)*] 
        MedusWiki adds restriction to XTM association, that it could have only two members
        """
        rvalue = []

        for assid, association in self._tm.associations.items():
            that = topicid # associated topic
            found = False
            for member in association.getMemberList():
                topic = member.getTopicRef().id
                if topic == topicid:
                    found = True
                    if member.getRoleSpec():
                        role = member.getRoleSpec().getTopicRef().id
                    else:
                        role = ""
                else:
                    that = topic

            if found:
                rvalue.append((assid, role, that))

        return rvalue

    def getRoles(self): # maybe it's better to filter roles with zpt tal:condition="instanceOf role"?
        """return list of all possible roles -> [role_id1, role_id2,*]
        role is a topic that has association('type'-'typeOf') with topic #role
        """
        roles = []

        for assid, role, topic in self.getTopicAssociations('role'):
            if role == "typeOf":
                roles.append(topic)

        return roles

    def filter(self, role=None, rtopic=None):
        """ return list of information about associations that fits given arguments. 
        (role|None, rtopic|None)->[(ltopic, role, rtopic),*]
        filter('AuthoredBy', 'Edvardas') == [('MedusWiki', 'AuthoredBy', 'Edvardas')]
        filter('AuthoredBy', None) == [('MedusWiki', 'AuthoredBy', 'Edvardas'), \
        ('ShitWiki', 'AuthoredBy', 'Petras')]
        """
        if not (role or rtopic): return []

        rvalue = []
        for assid, association in self._tm.associations.items():

            members = []
            for member in association.getMemberList():
                members.append(member)

            firstid = members[0].getTopicRef().id
            firstrole = members[0].getRoleSpec().getTopicRef().id
            secondid = members[1].getTopicRef().id
            secondrole = members[1].getRoleSpec().getTopicRef().id

            if role and not rtopic:
                if secondrole == role:
                    rvalue.append((secondid, secondrole, firstid))

                if firstrole == role:
                    rvalue.append((firstid, firstrole, secondid))

            elif rtopic and not role:
                if firstid == rtopic:
                    rvalue.append((secondid, secondrole, firstid))

                if secondid == rtopic:
                    rvalue.append((firstid, firstrole, secondid))

            else:
                if firstid == rtopic and secondrole == role:
                    rvalue.append((secondid, secondrole, firstid))

                if secondid == rtopic and firstrole == role:
                    rvalue.append((firstid, firstrole, secondid))

        return rvalue
