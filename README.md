# 🌐 Webpy
#### A simple-to-use http and https server, simillar to flask, in python.

### ✅ To-do 
- [x] ~~HTTP and HTTPS server class~~
- [x] ~~Request class~~
- [ ] Document class
- [ ] Python formatting in html
- [ ] MIME type in Document class

### ❓ How to use
```python
from webpy.servers import HTTP_Server
from webpy import RequestMethod

# Define the port and host
host, port = "127.0.0.1", 80

# Instanciate the server object
server = HTTP_Server(host, port)

# Create an handler for requests
@server.method(RequestMethod.GET, route="*") # Using the route as '*' will send all traffic with the GET method to this handler and override any other handler
def GET_Handler(request):
  # do stuff
  return Request.response(
      500, # Status code
      "Not Implemented", # Message
      {"Server": "Webpy/2.0", "Connection": "closed"} # Headers
  )

# Run the server
server.run()
