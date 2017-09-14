import socket
from mainModule import simpleServer

simpleServer = simpleServer()

#HOST, PORT = '0.0.0.0', 8080
HOST, PORT = '127.0.0.1', 8080

htmlTemplate = """<!DOCTYPE html>
<html>
<head>
<title>Page Title</title>
<meta http-equiv="content-type" content="text/html; charset=windows-1251" />
<link rel="icon" href="//i3.i.ua/css/i2/favicon_16.ico" type="image/x-icon">
</head>
<body>

<h1>This is a X</h1>
<p>This is a Z</p>

</body>
</html>\r\n"""

new_htmlTemplate = htmlTemplate.encode('windows-1251')

listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listen_socket.bind((HOST, PORT))
listen_socket.listen(10)
print('Serving HTTP on port %s ...' % PORT)
while True:
    client_connection, client_address = listen_socket.accept()
    request = client_connection.recv(1024)
    print("Recived <<<<<: ", request)
    simpleServer.handleRequest(request)
    responseHeader = simpleServer.response()[0]
    dataForResponse = simpleServer.response()[1]
    print("Response >>>>>: ", responseHeader)
    print(dataForResponse)
    client_connection.send(responseHeader)
    client_connection.send(dataForResponse)
    #client_connection.send(b'HTTP/1.1 200 OK \r\nContent-Type: text/html; charset=windows-1251r \r\n\r\n')
    #client_connection.send(new_htmlTemplate)
	#client_connection.sendall(response) #"server response >>>>>".join(request)
	
    client_connection.close()