# Author: Edvardas Scerbavicius
# E-mail: edvardas@gmail.com
""" ResourceRef class
    http://www.topicmaps.org/xtm/#elt-resourceRef
"""

class ResourceRef:
    """ ResourceRef class
        http://www.topicmaps.org/xtm/#elt-resourceRef
    """
    def __init__(self, uri=""):
        """Initialize ResourceRef object. (uri="") - set resource uri"""
        self.uri = uri

    def __str__(self):
        """Return XTM:str representation of ResourceRef object"""
        return """<resourceRef xlink:href="%s"/>""" % self.uri

    
