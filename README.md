# Webpy
*by bernard*

Webpy is an easy and simple webserver built in python.

### How to use
 ```python
 #Import webpy
 import webpy
 port = 80
 content_dir = "web/"
 host = "127.0.0.1"
 #Create web server object
 web = webpy.WebServer(port, content_dir, host)
 #Start web server
 web.start()
 ```
