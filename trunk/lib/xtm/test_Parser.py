import sys
sys.path.append('')
## sys.path.append("../..")

from xtm.Parser import Parser
from xtm.TopicMap import ns_xlink as xlink

id = "1"
parser = Parser()

# visad testuoti pilna TopicMap'a
def test_parseTopicMap():
   string = """<topicMap xmlns:xlink="%s" id="%s"></topicMap>""" % (xlink, id)
   assert parser.parseString(string).getId() == id 

def test_Topic():
   string = """<topicMap xmlns:xlink="%s" id="%s"><topic id="%s"></topic></topicMap>""" % (xlink, id, id)
   assert parser.parseString(string).topics[id].getId() == id

def test_Association():
   string = """<topicMap xmlns:xlink="%s" id="%s"><association id="%s"></association></topicMap>""" % (xlink, id, id)
   assert parser.parseString(string).getAssociations()[0].getId() == id

def test_BaseNameString():
   name = "vosvos"
   string = """<topicMap xmlns:xlink="%s" id="%s"><topic id="%s"><baseName><baseNameString>%s</baseNameString></baseName></topic></topicMap>""" \
            % (xlink, id, id, name)
   assert parser.parseString(string).topics[id].getBaseNameList()[0].getBaseNameString().name == name

def test_InstanseOf():
   string = """<topicMap xmlns:xlink="%s" id="%s"><topic id="%s"><instanceOf><topicRef xlink:href="#group"/></instanceOf></topic></topicMap>""" \
            % (xlink, id, id)
   assert parser.parseString(string).topics[id].getInstanceOfList()[0].getTopicRef().id == "group"

def test_Scope():
   string = """<topicMap xmlns:xlink="%s" id="%s"><topic id="%s"><baseName><scope><topicRef xlink:href="#this"/></scope><baseNameString>Quicklinks</baseNameString></baseName></topic></topicMap>""" \
            % (xlink, id, id) 
   assert parser.parseString(string).topics[id].getBaseNameList()[0].getScope().getTopicRef().id == "this"

def test_Occurrence():
   string = """<topicMap xmlns:xlink="%s" id="%s"><topic id="%s"><occurrence><resourceRef xlink:href="index"/></occurrence></topic></topicMap>""" \
            % (xlink, id, id) 
   assert parser.parseString(string).topics[id].getOccurrenceList()[0].getResourceRef().uri == "index"

def test_OccurrenceInstanceOf():
   string = """<topicMap xmlns:xlink="%s" id="%s"><topic id="%s"><occurrence><instanceOf><topicRef xlink:href="#cms"/></instanceOf></occurrence></topic></topicMap>""" \
            % (xlink, id, id) 
   assert parser.parseString(string).topics[id].getOccurrenceList()[0].getInstanceOf().getTopicRef().id == "cms"

def test_AssociationInstanceOf():
   string = """<topicMap xmlns:xlink="%s" id="%s"><association id="%s"><instanceOf><topicRef xlink:href="#cms"/></instanceOf></association></topicMap>""" \
            % (xlink, id, id) 
   assert parser.parseString(string).associations.values()[0].getInstanceOfList()[0].getTopicRef().id == "cms"

def test_AssociationMember():
   string = """<topicMap xmlns:xlink="%s" id="%s"><association id="%s"><member><roleSpec><topicRef xlink:href="#pointer"/></roleSpec></member></association></topicMap>""" \
            % (xlink, id, id) 
   assert parser.parseString(string).associations.values()[0].getMemberList()[0].getRoleSpec().getTopicRef().id == "pointer"

def test_AssociationMemberTopicRef():
   string = """<topicMap xmlns:xlink="%s" id="%s"><association id="%s"><member><topicRef xlink:href="#pointer"/></member></association></topicMap>""" \
            % (xlink, id, id) 
       # self.assertEquals(self.parser.parseString(string)[id].getMemberList()[0].getTopicRef().id, "pointer")
   assert parser.parseString(string).associations.values()[0].getMemberList()[0].getTopicRef().id == "pointer"

def test_parsefile():
    string = """<topicMap xmlns:xlink="%s" id="%s"></topicMap>""" % (xlink, id)
    f = open("test21212.xml", 'wt')
    f.write(string)
    f.close()
    assert parser.parse("test21212.xml").getId() == id
    import os
    os.remove("test21212.xml")


