# Author: Edvardas Scerbavicius
# E-mail: edvardas@gmail.com
"""Very simple global storage for objects"""

class Config:
    """This class stores global objects, these objects could be located:
       Config.get('key')
    """
    _instances = {}

    def adddict(yourdict):
        """Update existing objects with given dictionary of objects"""
        Config._instances.update(yourdict)
    adddict = staticmethod(adddict)

    def add(key, value):
        """Add or update object (key, value)"""
        Config._instances[key] = value
    add = staticmethod(add)

    def get(key):
        """Get object by key"""
        return Config._instances[key]
    get = staticmethod(get)
