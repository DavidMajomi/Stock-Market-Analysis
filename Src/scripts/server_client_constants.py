import socket


# Network related constants
HEADER = 64
PORT = 8960
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'