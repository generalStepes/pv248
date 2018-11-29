
#!/usr/bin/env python3
from socketserver import ThreadingMixIn
from http.server import HTTPServer, CGIHTTPRequestHandler
import socketserver
import sys
import urllib
import os
import logging

def parseFileName(item):
    filePath = (sys.argv[2] + item.path)
    fileSize = os.path.getsize(filePath)
    return filePath, fileSize

def processStuff(self):
    filePath, fileSize = parseFileName(self)
    if (filePath.endswith(".cgi")):
            self.cgi_info = '', filePath
            self.run_cgi()

    if filePath.endswith(".cgi") == False:
        self.send_response(200)
        self.send_header('Content-Length', str(fileSize))
        self.end_headers()
        fp = open(filePath, 'rb')
        read = 0
        while True:
            data = fp.read()
            self.wfile.write(data)



class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    pass

def createHandler():
    class Handler(CGIHTTPRequestHandler):
        def do_GET(self):
            processStuff(self)
        def do_POST(self):
            processStuff(self)
        def do_HEAD(self):
            processStuff(self)
    return Handler

handler = createHandler()
server = ThreadedHTTPServer(('localhost', int(sys.argv[1])), handler)
print ('Starting server, use <Ctrl-C> to stop')
server.serve_forever()
