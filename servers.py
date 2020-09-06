import socket
import threading

from . import RequestMethod
from .requests import Request


# Server class
class Server:
    def __init__(self, host, port):
        self._host = host
        self._port = port

    @property
    def host(self):
        return self._host
    
    @host.setter
    def host_set(self, newhost):
        if not isinstance(newhost, str):
            raise Exception("Placeholder")
        self._host = newhost
        
    @host.deleter
    def host_delete(self):
        raise Exception("You cannot delete the host attribute")
    
    @property
    def port(self):
        return self._port
    
    @port.setter
    def port_set(self, newport):
        if not isinstance(newport, int):
            raise Exception("Placeholder")
        self._port = newport

    @port.deleter
    def port_delete(self):
        raise Exception("You cannot delete the port attribute")


# HTTP Server class
class HTTP_Server(Server):
    def __init__(self, host, port):
        super().__init__(host, port)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.functions = {}
        self.threads = []

    def method(self, method: RequestMethod, route="*"):
        def wrapper(function):
            if method not in self.functions:
                self.functions[method] = {}           
            self.functions[method].update({route: function})
        return wrapper

    def _call_methods(self, method: RequestMethod, route, request):
        if method in self.functions:
            if route in self.functions[method]:
                return self.functions[method][route](request)
            elif "*" in self.functions[method]:
                return self.functions[method]["*"](request)
        return Request.response(502, "Not Implemented", {"Server": "Webpy/2.0", "Connection": "closed"})

    def handler(self, connection, address):
        data = b""
        while True:
            incoming = connection.recv(1024)
            data += incoming
            if incoming.endswith(b"\r\n\r\n") or not incoming or incoming == b"": break
            print(incoming)
        x = Request.from_request(data)
        response = self._call_methods(x.method, x.path, x)
        connection.send(response)
        connection.close()
    def run(self):
        self.socket.bind((self.host, self.port))
        self.socket.listen(50)
        while True:
            conn, addr = self.socket.accept()
            thread = threading.Thread(target=self.handler, args=(conn, addr))
            self.threads.append(thread)
            thread.start()

# HTTPS Server class
class HTTPS_Server(Server):
    def __init__(self, host, port, certfile, keyfile):
        super().__init__(host, port)
        self.context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        self.context.load_cert_chain(certfile=certfile, keyfile=keyfile)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.functions = {}
        self.threads = []

    def method(self, method: RequestMethod, route="*"):
        def wrapper(function):
            if method not in self.functions:
                self.functions[method] = {}           
            self.functions[method].update({route: function})
        return wrapper

    def _call_methods(self, method: RequestMethod, route, request):
        if method in self.functions:
            if "*" in self.functions[method]:
                return self.functions[method]["*"](request)
            elif route in self.functions[method]:
                return self.functions[method][route](request)
        return Request.response(502, "Not Implemented", {"Server": "Webpy/2.0", "Connection": "closed"})

    def handler(self, connection, address):
        data = b""
        while True:
            incoming = connection.read()
            data += incoming
            if incoming.endswith(b"\r\n\r\n") or not incoming or incoming == b"": break
            print(incoming)
        x = Request.from_request(data)
        response = self._call_methods(x.method, x.path, x)
        connection.send(response)
        connection.shutdown()

    def run(self):
        self.socket.bind((self.host, self.port))
        self.socket.listen(50)
        while True:
            conn, addr = self.socket.accept()
            conn = self.context.wrap_socket(newsocket, server_side=True)
            thread = threading.Thread(target=self.handler, args=(conn, addr))
            self.threads.append(thread)
            thread.start()
