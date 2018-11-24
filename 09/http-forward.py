from http.server import BaseHTTPRequestHandler, HTTPServer
from os import path
import http, ssl
import json
import sys

hostName = "localhost"
hostPort = int(sys.argv[1])
responseDict = {}

def httpClientFun(url,headers, timeout, content, requestType):
        url, params = cleanAddress(url)
        #print(headers)
        try:
            conn = http.client.HTTPSConnection(url, context=ssl._create_unverified_context(), timeout=timeout)
            if requestType == "POST": conn.request(requestType, params, content, headers = headers)
            else: conn.request(requestType, params, headers = headers)
            r1 = conn.getresponse()
        except:
            return (None, None, None, "True")
        headers = r1.getheaders()
        status = r1.status
        sourceCode = r1.read().decode("utf-8", "ignore")
        conn.close()
        return (headers, status, sourceCode, "False")

def cleanAddress(url):
    url = url.replace("https://","")
    url = url.replace("http://","")
    slash = url.find("/")
    if slash != -1:
        urlParsed = url[:slash]
        try:
            params = url[slash:]
        except:
            params = "/"
    else:
        urlParsed = url
        params = "/"
    return urlParsed, params

def parseHeaders(headers):
    headersDict = {}
    for item in headers:
        headersDict[item[0]] = item[1]
    return headersDict

def parseContent(sourceCode, status, connFailed):
    if connFailed == "False":
        responseDict["code"] = status
        try:
            sourceCodeJ = sourceCode.replace("\n", "")
            responseDict["json"] = json.loads(sourceCodeJ)
        except:
            responseDict["content"] = sourceCode
    if connFailed == "True":
        responseDict["code"] = "timeout"


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global responseDict
        responseDict = {}
        headers, status, sourceCode, connFailed = httpClientFun(sys.argv[2], None, 1, None, "GET")
        if connFailed == "False": responseDict["headers"] = parseHeaders(headers)
        parseContent(sourceCode, status, connFailed)
        responseDictJ = str(json.dumps(responseDict))
        responseDictJ = bytes(responseDictJ, 'utf-8')
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(responseDictJ)

    def do_POST(self):
        global responseDict
        responseDict = {}
        try:
            load = json.loads(self.rfile.read(int(self.headers['Content-Length'])))
        except:
            responseDict["code"] = "invalid json"
            connFailed = "NotExist"
            sourceCode = None
            status = None
        try:
            requestType = load["type"]
        except:
            requestType = "GET"
        if requestType == "": requestType = "GET"
        try:
            headers = load["headers"]
        except:
            headers = {}
        if headers == "": headers = {}
        try:
            timeout = load["timeout"]
        except:
            timeout = 1
        try:
            url = load["url"]
        except:
            responseDict["code"] = "invalid json"
            connFailed = "NotExist"
            sourceCode = None
            status = None
        try:
            content = load["content"]
        except:
            responseDict["code"] = "invalid json"
            connFailed = "NotExist"
            sourceCode = None
            status = None
        if "code" not in responseDict: headers, status, sourceCode, connFailed = httpClientFun(url, headers, timeout, content, requestType)
        if connFailed == "False": responseDict["headers"] = parseHeaders(headers)
        parseContent(sourceCode, status, connFailed)
        responseDictJ = str(json.dumps(responseDict))
        responseDictJ = bytes(responseDictJ, 'utf-8')
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(responseDictJ)


myServer = HTTPServer((hostName, hostPort), RequestHandler)
myServer.serve_forever()