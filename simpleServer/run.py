import socket
import sys
from mainModule import simpleServer

# TO DO
# handle commands from CLI

simpleServer = simpleServer()

HOST, PORT = '0.0.0.0', 8080

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
	
    try:
        response = simpleServer.response()
        client_connection.send(response)
    
	    # Not print too long responses
        if len(response) < 10000:
            print("Response >>>>>: ", response)
		
    except:
        print('\nError during response send.\n')
        print(sys.exc_info())
	
    client_connection.close()