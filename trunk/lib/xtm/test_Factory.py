import sys
sys.path.append('')

from xtm.Factory import Factory
from xtm.Exceptions import IdExistsError
from xtm.TopicMap import ns_xlink, ns_xtm

id = "sugar"
uri = "http://localhost/"
factory = Factory()
 
def test_createTopicMap():
    myTM = factory.createTopicMap(id)
    assert myTM.getId() == id

def test_TopicMapXML():
    xml = """<topicMap xmlns="%s" xmlns:xlink="%s" id="%s"></topicMap>""" % (ns_xtm, ns_xlink, id)
    myTM = factory.createTopicMap(id)
    assert str(myTM) == xml

def test_TopicsInTopicMapXML():
    xml = """<topicMap xmlns="%s" xmlns:xlink="%s" id="%s"><topic id="1"></topic><topic id="2"></topic></topicMap>""" \
         % (ns_xtm, ns_xlink, id)
    myTM = factory.createTopicMap(id)
    topic1 = factory.createTopic("1")
    topic2 = factory.createTopic("2")
    myTM.addChild(topic1)
    myTM.addChild(topic2)
    assert str(myTM) == xml

def test_createTopic():
    myTopic = factory.createTopic(id)
    assert myTopic.getId() == id

def test_TopicXML():
    xml ="""<topic id="%s"></topic>""" % id
    myTopic = factory.createTopic(id)
    assert str(myTopic) == xml

def test_createAssociation():
    myAssociation = factory.createAssociation(id)
    assert myAssociation.getId() == id

def test_AssociationXML():
    xml ="""<association id="%s"></association>""" % id
    myAssociation = factory.createAssociation(id)
    assert str(myAssociation) == xml

def test_createBaseNameString():
    name = "Edvardas"
    myNameString = factory.createBaseNameString(name)
    assert myNameString.name == name

def test_BaseNameStringXML():
    xml = "<baseNameString>vosvos</baseNameString>"
    myBaseNameString = factory.createBaseNameString("vosvos")
    assert str(myBaseNameString) == xml

def test_createBaseName():
    name = "Edvardas"
    myBaseName = factory.createBaseName(name)
    assert myBaseName.getBaseNameString().name == name 

def test_BaseNameXML():
    xml = "<baseName></baseName>"
    myBaseName = factory.createBaseName()
    assert str(myBaseName) == xml

def test_BaseNameXML2():
    xml = "<baseName><baseNameString>vosvos</baseNameString></baseName>"
    myBaseName = factory.createBaseName("vosvos")
    assert str(myBaseName) == xml

def test_createResourceRef():
    myResourceRef = factory.createResourceRef(uri)
    assert myResourceRef.uri == uri

def test_ResourceRefXML():
    xml = """<resourceRef xlink:href="%s"/>""" % uri
    myResourceRef = factory.createResourceRef(uri)
    assert str(myResourceRef) == xml

def test_createTopicRef():
    myTopicRef = factory.createTopicRef(id)
    assert myTopicRef.id == id

def test_TopicRefXML():
    xml = """<topicRef xlink:href="#%s"/>""" % id
    myTopicRef = factory.createTopicRef(id)
    assert str(myTopicRef) == xml      

def test_creatScope():
    myScope = factory.createScope(id)
    assert myScope.getTopicRef().id == id

def test_ScopeXML():
    xml ="""<scope><topicRef xlink:href="#%s"/></scope>""" % id
    myScope = factory.createScope(id)
    assert str(myScope) == xml      

def test_Occurrence():
    myOccurrence = factory.createOccurrence(uri)
    assert myOccurrence.getResourceRef().uri == uri

def test_OccurrenceXML():
    xml = """<occurrence><resourceRef xlink:href="%s"/></occurrence>""" % uri
    myOccurrence = factory.createOccurrence(uri)
    assert str(myOccurrence) == xml

def test_Member():
    myMember = factory.createMember(id)
    assert myMember.getTopicRef().id == id

def test_MemberXML():
    xml = """<member><topicRef xlink:href="#%s"/></member>""" % id
    myMember = factory.createMember(id)
    assert str(myMember) == xml

def test_RoleSpec():
    myRoleSpec = factory.createRoleSpec(id)
    assert myRoleSpec.getTopicRef().id == id

def test_RoleSpecXML():
    xml = """<roleSpec><topicRef xlink:href="#%s"/></roleSpec>""" % id
    myRoleSpec = factory.createRoleSpec(id)
    assert str(myRoleSpec) == xml

def test_addMemberRoleSpec():
    myMember = factory.createMember()
    myRoleSpec = factory.createRoleSpec()

    myMember.setRoleSpec(myRoleSpec)

    assert myMember.getRoleSpec().getTopicRef() == ""

def test_MemberRoleSpecXML():
    xml = """<member><roleSpec></roleSpec></member>"""
    myMember = factory.createMember()
    myRoleSpec = factory.createRoleSpec()

    myMember.setRoleSpec(myRoleSpec)

    assert str(myMember) == xml

def test_InstanceOf():
    myInstanceOf = factory.createInstanceOf(id)
    assert myInstanceOf.getTopicRef().id == id

def test_InstanceOfXML():
    xml = """<instanceOf><topicRef xlink:href="#%s"/></instanceOf>""" % id
    myInstanceOf = factory.createInstanceOf(id)
    assert str(myInstanceOf) == xml

def test_createBaseNameScope():
    myBaseName = factory.createBaseName()
    myScope = factory.createScope(id)
    myBaseName.setScope(myScope)
    assert myBaseName.getScope().getTopicRef().id == id

def test_BaseNameScopeXML():
    xml = """<baseName><scope><topicRef xlink:href="#%s"/></scope></baseName>""" % id

    myBaseName = factory.createBaseName()
    myScope = factory.createScope(id)
    myBaseName.setScope(myScope)
    assert str(myBaseName) == xml

def test_setTopicBaseName():
    name = "test_name"
    myTopic = factory.createTopic("test")
    myBaseName = factory.createBaseName(name)
    myTopic.addChild(myBaseName)
    assert myTopic.getBaseNameList()[0].getBaseNameString().name == name

def test_TopicBaseNameXML():
    name = "test_name"
    xml = """<topic id="%s"><baseName><baseNameString>%s</baseNameString></baseName></topic>""" % (id, name)

    myTopic = factory.createTopic(id)
    myBaseName = factory.createBaseName(name)
    myTopic.addChild(myBaseName)
    assert str(myTopic) == xml

def test_setTopicInstanceOf():
    myTopic = factory.createTopic(id)
    myInstanceOf = factory.createInstanceOf(id)
    myTopic.addChild(myInstanceOf)
    assert myTopic.getInstanceOfList()[0].getTopicRef().id == id

def test_TopicInstanceOfXML():
    xml = """<topic id="%s"><instanceOf><topicRef xlink:href="#%s"/></instanceOf></topic>""" % (id, id)

    myTopic = factory.createTopic(id)
    myInstanceOf = factory.createInstanceOf(id)
    myTopic.addChild(myInstanceOf)
    assert str(myTopic) == xml

def test_setOccurrenceInstanceOf():
    myOccurrence = factory.createOccurrence()
    myInstanceOf = factory.createInstanceOf(id)
    myOccurrence.setInstanceOf(myInstanceOf)
    assert myOccurrence.getInstanceOf().getTopicRef().id == id

def test_OccurrenceInstanceOfXML():
    xml = """<occurrence><instanceOf><topicRef xlink:href="#%s"/></instanceOf></occurrence>""" % id
    myOccurrence = factory.createOccurrence()
    myInstanceOf = factory.createInstanceOf(id)
    myOccurrence.setInstanceOf(myInstanceOf)
    assert str(myOccurrence) == xml

def test_setTopicOccurrence():
    myTopic = factory.createTopic("test")
    myOccurrence = factory.createOccurrence(uri)
    myTopic.addChild(myOccurrence)
    assert myTopic.getOccurrenceList()[0].getResourceRef().uri == uri

def test_TopicOccurrenceXML():
    xml = """<topic id="%s"><occurrence><resourceRef xlink:href="%s"/></occurrence></topic>""" % (id, uri)
    myTopic = factory.createTopic(id)
    myOccurrence = factory.createOccurrence(uri)
    myTopic.addChild(myOccurrence)
    assert str(myTopic) == xml

def test_setAssociationInstanceOf():
    myAssociation = factory.createAssociation("test")
    myInstanceOf = factory.createInstanceOf(id)
    myAssociation.addChild(myInstanceOf)
    assert myAssociation.getInstanceOfList()[0].getTopicRef().id == id

def test_AssociationInstanceOfXML():
    xml = """<association id="%s"><instanceOf><topicRef xlink:href="#%s"/></instanceOf></association>""" % (id, id)
    myAssociation = factory.createAssociation(id)
    myInstanceOf = factory.createInstanceOf(id)
    myAssociation.addChild(myInstanceOf)
    assert str(myAssociation) == xml

def test_addAssociationMember():
    myAssociation = factory.createAssociation("test")
    myMember = factory.createMember()
    myAssociation.addChild(myMember)
    assert type(myAssociation.getMemberList()[0]) == type(myMember)

def test_AssociationMemberXML():
    xml = """<association id="%s"><member></member></association>""" % id

    myAssociation = factory.createAssociation(id)
    myMember = factory.createMember()

    myAssociation.addChild(myMember)
    assert str(myAssociation) == xml

def test_addChild2TopicMap():
    myTopicMap = factory.createTopicMap("vosvos")
    myTopic = factory.createTopic("test")
    myTopicMap.addChild(myTopic)
    assert myTopicMap.topics["test"] == myTopic

def test_TopicMapgetTopics():
    myTopicMap = factory.createTopicMap("vosvos")
    myTopic = factory.createTopic("test")
    myTopicMap.addChild(myTopic)
     
    for topic in myTopicMap.topics.values():
        assert type(topic) == type(myTopic)

def test_TopicMapgetAssociationss():
    myTopicMap = factory.createTopicMap("vosvos")
    myAssociation = factory.createAssociation("test")
    myTopicMap.addChild(myAssociation)
     
    for association in myTopicMap.associations.values():
        assert type(association) == type(myAssociation)

def test_AddSameIDTopic():
    myTM = factory.createTopicMap(id)
    topic = factory.createTopic("1")
    myTM.addChild(topic)
    try:
        myTM.addChild(topic)
    except IdExistsError:
        assert True
    else:
        assert False

def test_2BaseName():
    xml = "<baseName></baseName>"
    myBaseName = factory.createBaseName()
    myTopic = factory.createTopic("1")
    myTopic.addChild(myBaseName)
    myTopic.addChild(myBaseName)
    assert str(myTopic.getBaseNameList()[1]) == xml

def test_2InstanceOf():
    xml = "<instanceOf></instanceOf>"
    myInstanceOf = factory.createInstanceOf()
    myTopic = factory.createTopic("1")
    myTopic.addChild(myInstanceOf)
    myTopic.addChild(myInstanceOf)
    assert str(myTopic.getInstanceOfList()[1]) == xml

def test_exportXML():
    myTM = factory.createTopicMap(id)
    topic = factory.createTopic("1")
    myTM.addChild(topic)
    assert myTM.exportxml("mytm21212.xml") == None
    import os
    os.remove("mytm21212.xml")

def test_removeTopic():
    myTM = factory.createTopicMap(id)
    topic = factory.createTopic("1")
    myTM.addChild(topic)
    myTM.removeTopic("1")
    assert not "1" in myTM.topics.keys() 
