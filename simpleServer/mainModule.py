import sys
import os
import mimetypes
import urllib
import html
from os import listdir


class simpleServer(object):
    """
    This is main class of simple file server.
    """
    def response(self):
        responseHeadItemsList = []
        sysEncoding = 'utf-8' #sys.getfilesystemencoding()
        protocol = 'HTTP/1.0'
        status = self.status
        protocolAndStatus = ' '.join([protocol, status])
        servername = 'Server: simpleFileServer'
        connection = self.connection #Connection: keep-alive
		#TO DO fix error fix keepAlive 
        #if 'close' not in connection:
        #    keepAlive = 'Keep-Alive: timeout=2'
        contentType = 'Content-Type: %s \r\n' % self.contentType
        dataForResponse = self.dataForResponse
        responseHead = '\r\n'.join([protocolAndStatus, 
                                servername, connection, 
                                contentType]).encode(sysEncoding)
        completeResponse = '\r\n'.encode(sysEncoding).join([responseHead, dataForResponse])
        return completeResponse
		
		
    def getListDir(self, path):
        pageItemsList = []
        displaypath = urllib.parse.unquote(path)
        title = '\n<!DOCTYPE html>\n<html>\n<head>\n<title>Directory listing for %s </title>\n' % displaypath
        meta = '<meta charset="UTF-8">\n</head>\n<body>\n'
        h1Tag = '<h1>Directory listing for %s </h1>\n' % displaypath 
        pageItemsList.append(title)
        pageItemsList.append(meta)
        pageItemsList.append(h1Tag)
        dirItemsList = os.listdir(path)
        
        for dirItem in dirItemsList:
            nameAndPath = os.path.join(path, dirItem)
            if os.path.isdir(nameAndPath): 
                dirItem=dirItem+"/"
            pageItemsList.append('<li><a href="%s">%s</a></li>' % (urllib.parse.quote(dirItem), html.escape(dirItem, quote=False)))
        
        pageItemsList.append('</body>\n</html>\r\n\r\n')
        self.status = '200 OK'
        self.connection = 'Connection: keep-alive'
        self.contentType = 'text/html; charset=utf-8'
        self.dataForResponse = '\n'.join(pageItemsList).encode('utf-8')
        self.response()

    def do_GET(self, path):
        # Dencode path string 
        path = urllib.parse.unquote(path)
		# Need check what requested : file or dir
        if path == '/':
            path = './'
            if 'index.html' in os.listdir(path):
                lastItemInPath = 'index.html'
                self.lastItemInPath = lastItemInPath
                with open("index.html", "rb") as f:
                    self.dataForResponse = f.read()
                self.contentType = 'text/html; charset=utf-8'
                self.response()
            else:
                self.getListDir(path)
        elif path == '/favicon.ico':
            self.status = '404 File not found'
            self.connection = 'Connection: close'
            self.contentType = 'image/x-icon; charset=utf-8' 
            self.dataForResponse = ''.encode('utf-8')
            self.response()
        else:
            pathToList = path.split('/')
            if pathToList[-1] == '':
                lastItemInPath = pathToList[-2]
            else:
                lastItemInPath = pathToList[-1]
            
			# Check is it file or dir
            self.lastItemInPath = lastItemInPath
            pathOnFileSystem = '.' + path
			
            print(path)
            print(lastItemInPath)
            print(pathOnFileSystem)
            
			# IF requested dir
			
			#TO DO 
			# переделать проверку "папка или файл?" 
            if os.path.isdir(pathOnFileSystem):
                if 'index.html' in os.listdir(pathOnFileSystem):
                    with open(pathOnFileSystem + 'index.html', 'rb') as f:
                        self.dataForResponse = f.read()
                    self.status = '200 OK'
                    self.connection = 'Connection: keep-alive'
                    self.contentType = 'text/html; charset=utf-8'
                    self.response()
                else:
                    try:
                        self.getListDir(pathOnFileSystem)
                    except FileNotFoundError as err:
                        self.status = '404 File not found'
                        self.connection = 'Connection: close'
                        self.contentType = 'text/html; charset=utf-8'
                        dataForResponse = 'Message: %s' % err
                        self.dataForResponse = dataForResponse.encode('utf-8')
                        self.response()
                        
			# IF requested file	
            else:
                try:
                    with open(pathOnFileSystem, 'rb') as f:
                        self.dataForResponse = f.read()
                    self.status = '200 OK'
                    self.connection = 'Connection: keep-alive'
                    self.contentType = '%s; charset=utf-8' % mimetypes.guess_type(lastItemInPath)[0]
                    self.response()
                except:
                    print("\nError during file openning\n")
                    print(sys.exc_info()) # return info about exception
                    self.status = '404 File not found'
                    self.connection = 'Connection: close'
                    self.contentType = 'text/html; charset=utf-8'
                    self.dataForResponse = 'Message: 404 File not found'.encode('utf-8')
                    self.response()
					
                        
    def handleRequest(self, request):
        # try...except added for fix empty request issue: Recived <<<<<:  b''
        try:	
            requestHearesList = str(request).split(r'\r\n')
            self.reqMethod = requestHearesList[0].split()[0]
            self.path = requestHearesList[0].split()[1]
            self.protocol = requestHearesList[0].split()[2]
			
            if "GET" in self.reqMethod:
                self.do_GET(path = self.path)
            elif "HEAD" in self.reqMethod:
                self.status = '200 OK'
                self.connection = 'Connection: keep-alive'
                self.contentType = 'text/html; charset=utf-8'
                self.dataForResponse = ''.encode('utf-8')
                self.response()
            else:
            #TO DO
			# POST method
                print("\nUnsupported request method!\n")
                print(sys.exc_info())				
                pass
			
        except:
            print("\nError during request parse\n")
            pass
			