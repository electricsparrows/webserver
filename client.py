#client.py

import socket

s = socket.socket()

port = 80
host = "127.0.0.1"
s.connect((host, port))

# 1 send and receive should be a single transaction
while True:
    req = "GET / HTTP/1.1"
    s.send(req.encode())
    RECEIVED = s.recv(1024).decode()
    print(RECEIVED)
    break
    
s.close()

def get_http_message():
    msg = 'GET / HTTP/1.1'
    return msg

# request


# response