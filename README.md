# 🌐 Webpy
#### A simple-to-use http and https server, simillar to flask, in python.

### ✅ To-do 
- [x] HTTP and HTTPS server class
- [x] Request class
- [x] Document class
- [x] Python code execution in html
- [x] MIME type in Document class
- [ ] Default headers per server
- [x] Per host handler

### ❓ How to use
```python
from webpy.servers import HTTP_Server
from webpy import RequestMethod

# Define the port and host
host, port = "127.0.0.1", 80

# Instanciate the server object
server = HTTP_Server(host, port)
#For HTTPS servers, use HTTPS_Server(host, port, certificate_path, private_key_path)


# Create an handler for requests
@server.method(RequestMethod.GET, route="*", host="*") # Using the route and host parameters as '*' will use this handler as a fallback for the GET method.
def GET_Handler(request):
  # do stuff
  return Request.response(
      500, # Status code
      "Not Implemented", # Message
      {"Server": "Webpy/2.0", "Connection": "closed"}, # Headers
      b"" # Body
  )

@server.method(RequestMethod.GET, route="/api/", host="*")
def API_Handler(request):
  # do stuff
  return Request.response(
      500, # Status code
      "Not Implemented", # Message
      {"Server": "Webpy/2.0", "Connection": "closed"}, # Headers
      b'{"foo": "bar"}' # Body
  )

# Run the server
server.run()
