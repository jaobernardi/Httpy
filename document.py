from bs4 import BeautifulSoup
from . import MIMETypes
import os


class Document:
    def __init__(self, data):
        self.data = data
        self._type = None
        self.extension = None

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
            x.extension = extension
        file.close()
        return x
    
    def parse_python(self, vars):
        def execute(code, _globals={}, _locals={}):
            fake_stdout = StringIO()
            __stdout = sys.stdout
            sys.stdout = fake_stdout
            if not 'output' in _globals:
                _globals['output'] = ''
            try:
                ret = eval(code, _globals, _locals)
                result = fake_stdout.getvalue()
                sys.stdout = __stdout
                if ret:
                    result += str(ret)
                return f"{_globals['output']}", _globals
            except:
                try:
                    exec(code, _globals)
                except:
                    sys.stdout = __stdout			
                    buf = StringIO()
                    return f"{_globals['output']}", _globals
                else:
                    sys.stdout = __stdout
                    return f"{_globals['output']}", _globals
        soup = BeautifulSoup(self.data.decode("utf-8"), 'html.parser')
        u = str(soup)
        b = {}
        for pythontag in soup.find_all("python"):
            (exec_, b) = execute(str(pythontag).replace("<python>", "").replace("</python>", ""), vars)
            u = u.replace(str(pythontag), exec_)
        self.data = u.encode()

