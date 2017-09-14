import sys
import os
import mimetypes
import urllib
import html
from os import listdir



class simpleServer():
    template_404 = '<!DOCTYPE html><html><head>\
				<meta http-equiv="content-type" content="text/html; charset=utf-8" />\
                <link rel="icon" href="//i3.i.ua/css/i2/favicon_16.ico" type="image/x-icon">\
                <title>404</title>\
                </head><body><h1>404 File not found</h1></body></html>'

    #sysEncoding = 'utf-8'
	
    def response(self, *arg):
        arg = (' 200 OK')
        sysEncoding = 'utf-8'

        if arg[0] == ' 200 OK':
            protocol = self.protocol
            status = arg[0]
            ps = protocol + status
            contentType = mimetypes.guess_type(self.lastItemInPath)[0]
            if type(self.dataForResponse) != 'bytes':
                responseBody = self.dataForResponse.encode(sysEncoding)
            else:
                responseBody = self.dataForResponse
            responseHeader = ('\r\n'.join([ps, contentType, '\r\n'])).encode(sysEncoding)
            return responseHeader, responseBody
			
        if arg[0] == ' 404 Not Found':
            protocol = self.protocol
            status = arg[0]
            ps = protocol + status
            contentType = 'text/html'
            responseBody = template_404.encode(sysEncoding)
            responseHeader = ('\r\n'.join([ps, contentType, '\r\n'])).encode(sysEncoding)
            return responseHeader, responseBody
			
    def completeResponse(self):
        pass
		
    def getListDir(self, path):
        pageItemsList = []
        displaypath = urllib.parse.unquote(path)
        #showDir = html.escape(displaypath, quote=False)
        title = '<!DOCTYPE html>\
        		<html>\
        		<head>\
				<meta http-equiv="content-type" content="text/html; charset=utf-8" />\
                <link rel="icon" href="//i3.i.ua/css/i2/favicon_16.ico" type="image/x-icon">\
				<title>Directory listing for %s </title></head><body>' % displaypath
        pageItemsList.append(title)
        dirItemsList = os.listdir(path)
        
        for dirItem in dirItemsList:
            nameAndPath = os.path.join(path, dirItem)
            if os.path.isdir(nameAndPath): dirItem=dirItem+"/"
            pageItemsList.append('<li><a href="%s">%s</a></li>'
            % (urllib.parse.quote(dirItem), html.escape(dirItem, quote=False)))
        pageItemsList.append('</body></html>\r\n')

        self.lastItemInPath = 'index.html'
        self.dataForResponse = '\n'.join(pageItemsList)
        self.response((' 200 OK'))

    def do_GET(self, path):
        #need check what requested : file or dir
        path = '.' + path
        if path[-1] == '/':
            if 'index.html' in os.listdir(path):
            	lastItemInPath = 'index.html'
            	self.lastItemInPath = lastItemInPath
            	f = open("index.html", "rb")
            	self.dataForResponse = f.read()
            	f.close()
            	self.response(' 200 OK')
            else:				
            	self.getListDir(path)
        else:
            f = open(path, "rb")
            self.dataForResponse = f.read()
            f.close()
            self.response(' 200 OK')
			
    def handleRequest(self, request):
        requestHearesList = str(request).split(r'\r\n')
        self.reqMethod = requestHearesList[0].split()[0]
        self.path = requestHearesList[0].split()[1]
        self.protocol = requestHearesList[0].split()[2]
        
        if "GET" in self.reqMethod:
            self.do_GET(path = self.path) 
        else:
            #TO DO
            pass
#
"""
		else:
            raw_lastItemInPath = path.split('/')
            if raw_lastItemInPath == '':
                lastItemInPath = raw_lastItemInPath[-2]
            else:
                lastItemInPath = raw_lastItemInPath[-1]
            #check is it file or dir
            self.lastItemInPath = lastItemInPath # /cat/t.jpg
                        
            if os.path.isdir(lastItemAndOsPath):
                lastItemAndOsPath += '/'
                if 'index.html' in os.listdir(lastItemAndOsPath):
                    f = open("index.html", "r")
                    self.dataForResponse = f.read()
                    f.close()
                    self.response()
                else:self.getListDir(lastItemAndOsPath) 
        else:
            f = open(path, "r")
            self.dataForResponse = f.read()
            f.close()
            self.response()
"""

