import sys
import os
import mimetypes
import urllib
import html
from os import listdir



class simpleServer():
    
    def response(self, *arg):
        arg = ['200 OK']
        if arg[0] != '404 Not Found':
            protocol = self.protocol
            status = '200 OK'
            contentType = mimetypes.guess_type(self.lastItemInPath)[0]
            dataForResponse = self.dataForResponse
            sysEncoding = sys.getfilesystemencoding()
            completeResponse = '\r\n'.join([protocol, status, contentType, dataForResponse]).encode(sysEncoding)
            return completeResponse
        if arg[0] == '404 Not Found':
            protocol = self.protocol
            status = '404 Not Found'
            contentType = 'text/html'
            dataForResponse = '<p>404 Not found</p>'
            sysEncoding = sys.getfilesystemencoding()
            completeResponse = '\r\n'.join([protocol, status, contentType, dataForResponse]).encode(sysEncoding)
            return completeResponse
    
    def getListDir(self, path):
        pageItemsList = []
        displaypath = urllib.parse.unquote(path)
        #showDir = html.escape(displaypath, quote=False)
        title = '<!DOCTYPE html>\
        		<html>\
        		<head><title>Directory listing for %s </title></head><body>' % displaypath
        pageItemsList.append(title)
        dirItemsList = os.listdir(path)
        
        for dirItem in dirItemsList:
            nameAndPath = os.path.join(path, dirItem)
            if os.path.isdir(nameAndPath): dirItem=dirItem+"/"
            pageItemsList.append('<li><a href="%s">%s</a></li>'
            % (urllib.parse.quote(dirItem), html.escape(dirItem, quote=False)))
        pageItemsList.append('</body></html>')

        self.lastItemInPath = 'index.html'
        self.dataForResponse = '\n'.join(pageItemsList)
        self.response()

    def do_GET(self, path):
        #need check what requested : file or dir
        if path == '/':
            path = '.'
            if 'index.html' in os.listdir(path):
            	lastItemInPath = 'index.html'
            	self.lastItemInPath = lastItemInPath
            	f = open("index.html", "r")
            	self.dataForResponse = f.read()
            	f.close()
            	self.response()
            else:
            	self.getListDir(path)
        elif path == '/favicon.ico':
        	path = '.'
        	if 'index.html' in os.listdir(path):
        		lastItemInPath = 'index.html'
        		self.lastItemInPath = lastItemInPath
        		f = open("index.html", "r")
        		self.dataForResponse = f.read()
        		f.close()
        		self.response()
        	else:
        		self.getListDir(path)

        else:
            raw_lastItemInPath = path.split('/')
            if raw_lastItemInPath == '':
                lastItemInPath = raw_lastItemInPath[-2]
            else:
                lastItemInPath = raw_lastItemInPath[-1]
            #check is it file or dir
            self.lastItemInPath = lastItemInPath
            lastItemAndOsPath = os.path.join(path, lastItemInPath)
            
            if os.path.isdir(lastItemAndOsPath):
                lastItemAndOsPath += '/'
                if 'index.html' in os.listdir(lastItemAndOsPath):
                    f = open("index.html", "r")
                    self.dataForResponse = f.read()
                    f.close()
                    self.response()
                else:self.getListDir(lastItemAndOsPath)
            else:
                f = open(lastItemInPath, "r")
                self.dataForResponse = f.read()
                f.close()
                self.response()
            
                
        
        
        
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