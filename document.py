from bs4 import BeautifulSoup


class Document:
    def __init__(self):
        self._type = None
        self.data = None
        self.name = None
        
    @property
    def type(self):
        return self._type
    
    @type.setter
    def type_set(self, newtype):
        self.type = newtype
    
    @classmethod
    def from_filename(cls, filename):
        return cls()
    
    @classmethod
    def from_data(cls, data):
        cls = cls()
        cls.data = data
        return cls
    
    @classmethod
    def from_data(cls, data):
        cls = cls()
        cls.data = data
        return cls