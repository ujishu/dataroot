import socket
import os, sys, io
import html
import urllib.parse
import posixpath
import mimetypes
#from http import HTTPStatus

def args():
	args = sys.argv
	if len(args) == 1:
		host, port = '0.0.0.0', 8888
	if len(args) == 2:
		host, port = '0.0.0.0', args[1]
	return host, int(port)

class Pyserver():
	def run_server(self,host=None,port=None):
		
		HOST, PORT = host, port
		listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		listen_socket.bind((HOST, PORT))
		listen_socket.listen(1)
		print('Serving HTTP on port %s ...' % PORT)
		###
		while True:
			client_connection, client_address = listen_socket.accept()
			self.client_connection = client_connection
			request = client_connection.recv(1024)
			print("REQUEST > ", request)
			path = self.parse_request(request)
			http_response = self.generalResponse()
			print("RESPONSE > ", http_response)
			self.client_connection.sendall(http_response)
			client_connection.close()

	def parse_request(self, request):
		try:
			request = str(request).split(r'\r\n')# transform req. string into list
			firstLineList = request[0].split()
			self.firstLineList = firstLineList
			if firstLineList[1] == '/':
				self.path = '.'
			else:
				self.path = '.' + firstLineList[1]
		except:
			print("error during parse_request()")
			pass

		path = self.path
		
		#print(path)
		return path

	def dirListing(self, path): #in case when index.html absent
		path = self.path
		try:
			dirItemsList = os.listdir(path)
		except OSError:
			print("dirListing error")

		pageList = []
		try:
			displaypath = urllib.parse.unquote(path)
		except UnicodeDecodeError:
			displaypath = urllib.parse.unquote(path)

		showDir = html.escape(displaypath, quote=False)
		self.sysEncoding = sys.getfilesystemencoding()

		### html page preparing 
		title = 'Directory listing for %s' % displaypath
		pageList.append('<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" '
                 '"http://www.w3.org/TR/html4/strict.dtd">')
		pageList.append('<html>\n<head>')
		pageList.append('<meta http-equiv="Content-Type" '
                 'content="text/html; charset=%s">' % self.sysEncoding)
		pageList.append('<title>%s</title>\n</head>' % title)
		pageList.append('<body>\n<h1>%s</h1>' % title)
		pageList.append('<hr>\n<ul>')

		for dirItem in dirItemsList:
			nameAndPath = os.path.join(path, dirItem)
			#displayname = dirItem
			if os.path.isdir(nameAndPath):
				dirItem = dirItem + "/"

			pageList.append('<li><a href="%s">%s</a></li>'
				% (urllib.parse.quote(dirItem), html.escape(dirItem, quote=False)))
		###

		responseString = '\n'.join(pageList).encode(self.sysEncoding)
		return responseString

	def generalResponse(self):
		if os.path.isdir(self.path):#if dir
			if 'index.html' in os.listdir(self.path): #check out index.html in direct.
				f = open("index.html", "rb")
				response = f.read()
				f.close()
				return response
			else:
				return self.dirListing(self.path)
		elif not os.path.isdir(self.path):#if requested not dir
			path = self.path
			filename = path.split('/')[-1]
			if filename == "favicon.ico":
				pass
			fileMimeType = mimetypes.guess_type(filename)[0]
			if fileMimeType == None:
				fileMimeType = 'application/octet-stream'
			print(path, filename, fileMimeType)
			#send 
			self.client_connection.sendall(fileMimeType.encode(sys.getfilesystemencoding()))
			try:
				f = open(filename, 'rb')
				response = f.read()
				f.close()
				return response
			except FileNotFoundError:
				print("FileNotFoundError")
				return b'<!DOCTYPE html>\n<html>\n<head>\n<title>404</title>\n</head>\n\
				<body>\n\n<p>File not found</p>\n\n</body>\n</html>'
			
		else:
			print("generalResponse() not work")
			
				
			#return self.dirListing(self.path)
		





server = Pyserver()
host = args()[0]
port = args()[1]
server.run_server(host, port)

"""
while True:
    client_connection, client_address = listen_socket.accept()
    request = client_connection.recv(1024)
    print(request)

    #print(server.parse_request(request))
    path = server.parse_request(request)

    http_response = server.generalResponse()
    print(http_response)
    client_connection.sendall(http_response)
    client_connection.close()
    #	print("server error")
    #	pass

    #client_connection.sendall(http_response)
    #client_connection.close()
"""