
#!/usr/bin/env python3
from socketserver import ThreadingMixIn
from http.server import HTTPServer, CGIHTTPRequestHandler
import socketserver
import sys
import urllib
import os
import logging
import json

def parseFileNameGet(item):
    slash = item.path.find("/")
    if slash != -1:
        addr = item.path[:slash]
        print(addr)
    filePath = (sys.argv[2] + item.path)
    try:
        fileSize = os.path.getsize(filePath)
    except:
        fileSize = None
        filePath = None
    return filePath, fileSize

def parseFileNamePost(item):
    filePath = (sys.argv[2] + "/" + item)
    fileSize = os.path.getsize(filePath)
    return filePath, fileSize

def findPath(relPath):
    relPath = os.path.join(sys.argv[2], relPath)
    path = os.path.abspath(relPath)
    pathBool = os.path.isfile(path)
    return path, relPath, pathBool

def processStuff(self, requestType):
        parsedURL = urllib.parse.urlparse(self.path)
        path, relPath, pathBool = findPath(parsedURL.path[1:])

        if requestType == "GET":
            paramsPath = relPath + "?" + parsedURL.query
            paramsPath = paramsPath.strip("?")

        if requestType == "POST":
            load = json.loads(self.rfile.read(int(self.headers['Content-Length'])))
            params = ""
            for item in load:
                params += item + "=" + load[item] + "&"
            try:
                params += parsedURL.query
            except:
                pass
            params = params.strip("&")
            paramsPath = relPath + "?" + params
            paramsPath = paramsPath.strip("?")
            print(paramsPath)
        if (pathBool == True and relPath is not None and relPath.endswith(".cgi")):
            self.cgi_info = '', paramsPath
            self.run_cgi()

        if pathBool == True and relPath is not None and relPath.endswith(".cgi") == False:
            fileSize = os.path.getsize(relPath)
            self.send_response(200)
            self.send_header('Content-Length', str(fileSize))
            self.end_headers()
            fp = open(relPath, 'rb')
            read = 0
            while True:
                data = fp.read()
                self.wfile.write(data)
        if pathBool == False:
            self.send_error(404,'File Not Found: %s' % self.path)




class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    pass

def createHandler():
    class Handler(CGIHTTPRequestHandler):
        def do_GET(self):
            processStuff(self, "GET")
        def do_POST(self):
            processStuff(self, "POST")
        def do_HEAD(self):
            processStuff(self)
    return Handler

handler = createHandler()
server = ThreadedHTTPServer(('localhost', int(sys.argv[1])), handler)
print ('Starting server, use <Ctrl-C> to stop')
server.serve_forever()
