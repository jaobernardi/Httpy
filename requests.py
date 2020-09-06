from . import RequestMethod, StreamDirection


class Request:
    def __init__(self, body: bytes, method: RequestMethod, status_code: int, path, headers: dict, arguments: dict, stream_direction: StreamDirection=StreamDirection.UNKNOWN, status_msg = "OK"):
        self.body = body
        self.method = method
        self.status_code = status_code
        self.stream_direction = stream_direction
        self.path = path
        self.headers = headers
        self.arguments = arguments
        self.status_msg = status_msg

    @classmethod
    def from_request(cls, request):
        print(request)
        path = request.split(b"\n")[0].split(b" ")[1].decode()
        print(path, "?" in path)
        if "?" in path:
            path, args = path.split("?")
        else:
            path, args = (path, "")
        arguments = {}
        if "&" in args:
            for key in args.split("&"):
                arguments[key.split("=")[0]] = key.split("=")[1]
        method = RequestMethod(request.split(b"\n")[0].split(b" ")[0].decode())
        status_code = 0
        headers = {}
        for head in request.split(b"\r\n\r\n")[0].split(b"\r\n")[1:]:            
            headers[head.split(b": ")[0].decode()] = head.split(b": ")[1].decode()
        
        return cls(request.split(b"\r\n\r\n")[1], method, status_code, path, headers, arguments, StreamDirection.UPSTREAM)
    
    @classmethod
    def response(cls, status_code, status_msg, headers, body=b""):
        x = cls(body, RequestMethod.GET, status_code, "", headers, {}, StreamDirection.DOWNSTREAM, status_msg)
        return x.build()
    
    def build(self):
        out = []
        if self.stream_direction == StreamDirection.DOWNSTREAM:
            out.append(f"HTTP/1.1 {self.status_code} {self.status_msg}")
        else:
            out.append(f"{self.method.value} {self.path} HTTP/1.1")
        for headname in self.headers:
            out.append(headname+": "+self.headers[headname])
        out.append("")
        out.append("")
        return "\r\n".join(out).encode()+self.body