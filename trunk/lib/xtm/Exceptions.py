# Author: Edvardas Scerbavicius
# E-mail: edvardas@gmail.com
class IdExistsError(Exception):
    """IdExistsError shows that object with such id already exists"""
    def __init__(self, id):
        Exception.__init__(self)
        self._id = id
