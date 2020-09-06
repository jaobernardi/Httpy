from bs4 import BeautifulSoup
from . import MIMETypes
import os


class Document:
    def __init__(self, data):
        self.data = data
        self._type = None

    @property
    def type(self):
        return self._type
    
    @type.setter
    def type_set(self, newtype):
        self.type = newtype
    
    @classmethod
    def from_filename(cls, path):
        file = open(path, "rb")
        data = file.read()
        x = cls(data)
        extension = os.path.basename(path).split(".")[-1]
        if extension.lower() in MIMETypes.types:
            x._type = MIMETypes.types[extension.lower()]
        file.close()
        return x

