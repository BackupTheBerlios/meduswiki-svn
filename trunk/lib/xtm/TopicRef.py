# Author: Edvardas Scerbavicius
# E-mail: edvardas@gmail.com
""" TopicRef class
    http://www.topicmaps.org/xtm/#elt-topicRef
"""

class TopicRef:
    """ TopicRef class
        http://www.topicmaps.org/xtm/#elt-topicRef
    """
    def __init__(self, id=None):
        """Initialize TopicRef object. (id=None) - set TopicRef id"""
        self.id = id

    def __str__(self):
        """Return XTM:str representation of TopicRef object"""
        return """<topicRef xlink:href="#%s"/>""" % self.id
