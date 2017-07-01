import socket

HOST = '127.0.0.1'    # The remote host
PORT = 8080         # The same port as used by the server
while True:
    data = input("enter: ")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(data.encode('utf-8'))
        data = s.recv(1024)
    print('Received', repr(data))