# Webpy
*by bernard*

Webpy is a eazy and simple webserver build in python.

### How to utilize
 ```python
 import webpy
 port = 80
 content_dir = "web/"
 host = "127.0.0.1"
 web = webpy.WebServer(port, content_dir, host)
 web.start()
 ```
