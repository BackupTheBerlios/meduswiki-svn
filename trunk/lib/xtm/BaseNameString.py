# Author: Edvardas Scerbavicius
# E-mail: edvardas@gmail.com
""" BaseNameString class
    http://www.topicmaps.org/xtm/#elt-baseNameString
"""

class BaseNameString:
    """ BaseNameString class
        http://www.topicmaps.org/xtm/#elt-baseNameString
    """
    def __init__(self, name):
        """Initialize BaseNameString object with a given name:str"""
        self.name = name

    def __str__(self):
        """Return XTM:str representation of BaseNameString object"""
        return "<baseNameString>%s</baseNameString>" % self.name
