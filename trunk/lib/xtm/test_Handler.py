import sys, os
sys.path.append('')

from xtm.Handler import Handler
from xtm.Factory import Factory
from xtm.TopicMap import ns_xlink as xlink

name = "shit happens"
tmFactory = Factory()

def init():
    global tmHandler, tm
    tmHandler = None #?
    tmHandler = Handler()
    tm = tmFactory.createTopicMap("1")
    
def test_addTopicMap():
    init()
    tmHandler.setTopicMap(tm)      
    assert tmHandler.getId() == "1"
              
def test_hasTopic():
    init()
    topic = tmFactory.createTopic(name)
    tm.addChild(topic)

    tmHandler.setTopicMap(tm)      
    assert tmHandler.hasTopic(name)

def test_addTopic():
    """topic is created from paramaters"""
    string = """<topicMap xmlns:xlink="%s" id="%s"></topicMap>""" % (xlink, "2122")
    f = open("test21212.xml", 'wt')
    f.write(string)
    f.close()

    tmHandler = Handler("test21212.xml")
    tmHandler.addTopic("name")
    assert tmHandler.hasTopic("name")
    os.remove("test21212.xml")


def test_addAssociation():
    """association is created from parameters"""
    tmHandler = Handler()
    tmHandler.addTopic("role")

    tmHandler.addTopic("knows", '', '', "role")
    tmHandler.addTopic("unknown", '', '', "role")
    tmHandler.addAssociation("knows", 'nonmexistant', "unknown")

    assert tmHandler.getTopicAssociations("knows")[0][2] == 'unknown'


def test_OppositeRole():
    """must return opposite role, or 'unknown' if not found"""
    init()
    role = tmFactory.createTopic("role")
    instanceOf = tmFactory.createTopic("type")
    classOf = tmFactory.createTopic("typeOf")
    role1 = tmFactory.createTopic("IsDevelopedBy")
    role2 = tmFactory.createTopic("HasDeveloped")
    oppositeRole = tmFactory.createTopic("oppositeRole")

    tm.addChild(oppositeRole)
    tm.addChild(instanceOf)
    tm.addChild(classOf)
    tm.addChild(role)
    tm.addChild(role1)
    tm.addChild(role2)
    tmHandler.setTopicMap(tm)

    tmHandler.addAssociation("IsDevelopedBy", "type", "role", "typeOf")
    tmHandler.addAssociation("HasDeveloped", "type", "role", "typeOf")
    tmHandler.addAssociation("HasDeveloped", "oppositeRole", "IsDevelopedBy", "oppositeRole")

    assert tmHandler.getOppositeRole('HasDeveloped') == "IsDevelopedBy"


def test_getOppositeRole():
    """must return Role of opposite object of association"""
    init()
    tmHandler.addAssociation("is_developed_by", "oppositeRole", "has_developed", "oppositeRole")
    tmHandler.addTopic("Word")
    tmHandler.addTopic("Microsoft")
    tmHandler.addAssociation("Word", "is_developed_by", "Microsoft")
     
    assert tmHandler.getTopicAssociations("Microsoft")[0][1] == "has_developed"


def test_getTopicAssociations():
    """must return packed informations about all associations of given topic id"""
    init()
    topic = tmFactory.createTopic("nuts1")
    topic2 = tmFactory.createTopic("nuts2")
    tm.addChild(topic)
    tm.addChild(topic2)

    tmHandler.setTopicMap(tm)      
    tmHandler.addTopic("knows", '', '', "role")
    tmHandler.addTopic("unknown", '', '', "role")

    tmHandler.addAssociation("nuts1", "knows" ,"nuts2", "unknown")

    assert tmHandler.getTopicAssociations("nuts2")[0][1] == 'unknown' 
    assert tmHandler.getTopicAssociations("nuts2")[0][2] == 'nuts1' 


def test_getRoles():
    """must return list [ role_id, roleid2,...] of all possible roles
    """
    init()
    role = tmFactory.createTopic("role")
    instanceOf = tmFactory.createTopic("type")
    classOf = tmFactory.createTopic("typeOf")

    role1 = tmFactory.createTopic("IsDevelopedBy")
    role2 = tmFactory.createTopic("HasDeveloped")

    tm.addChild(instanceOf)
    tm.addChild(classOf)
    tm.addChild(role)
    tm.addChild(role1)
    tm.addChild(role2)
    tmHandler.setTopicMap(tm)

    tmHandler.addAssociation("IsDevelopedBy", "type", "role", "typeOf")
    tmHandler.addAssociation("HasDeveloped", "type", "role", "typeOf")

    assert tmHandler.getRoles() == ['IsDevelopedBy', 'HasDeveloped']

def test_removeTopic():
    """must remove Topic from topic map (no physical file removing)"""
    init()
    tmHandler.addTopic("Word")
    assert tmHandler.hasTopic("Word")
    tmHandler.removeTopic("Word")
    assert not tmHandler.hasTopic("Word")

def test_removeAssociation():
    """must remove Association from topic map"""

    tmHandler = Handler()
    tmHandler.addTopic("role")
    tmHandler.addTopic("knows", '', '', "role")
    tmHandler.addTopic("unknown", '', '', "role")
    tmHandler.addAssociation("knows", 'oppositeRole', "unknown")

    assid = tmHandler.getTopicAssociations("knows")[0][0]

    tmHandler.removeAssociation(assid)

    assert not assid in tmHandler._tm.associations.keys()

def test_isBuiltIn():
    """must return true if topic is XTM instanceOf builtIn"""
    init()
    tmHandler.addTopic("role", '', '', "builtIn")
    tmHandler.addTopic("shit")

    assert tmHandler.isBuiltIn("role") == True
    assert tmHandler.isBuiltIn("shit") == False


def test_search():
    """(role|None, rtopic|None)->[(ltopic, role, rtopic),... ]"""
    init()
    tmHandler.addAssociation("IsDevelopedBy", "type", "role", "typeOf")
    tmHandler.addAssociation("HasDeveloped", "type", "role", "typeOf")

    tmHandler.addAssociation("Edvardas", "AuthorOf", "MedusWiki", "AuthoredBy")
    tmHandler.addAssociation("Petras", "AuthorOf", "ShitWiki", "AuthoredBy")
    tmHandler.addAssociation("Edvardas", "Rides", "Bicycle", "IsRiddenBy")

    assert tmHandler.filter() == []
    assert tmHandler.filter("AuthoredBy", "Edvardas") == [("MedusWiki", "AuthoredBy", "Edvardas")]
    assert tmHandler.filter("AuthoredBy", None) == [("MedusWiki", "AuthoredBy", "Edvardas"), \
                                                   ("ShitWiki", "AuthoredBy", "Petras")]
    assert tmHandler.filter(None, "Edvardas") == [("MedusWiki", "AuthoredBy", "Edvardas"), \
                                                 ("Bicycle", "IsRiddenBy", "Edvardas")] 
