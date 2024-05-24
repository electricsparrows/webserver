# Server.py 

## from coding challenges.com

#1. Create a socket
import socket
import sys

# Creates the socket


if __name__ == '__main__':
    try: 
        s = socket.socket()
        print("Socket successfully created")
    except socket.error as err:
        print ("socket creation failed with error %s" %(err))

    port = 80
    host= "127.0.0.1"

    s.bind((host, port))
    print ("socket binded to %s" %(port)) 
    s.listen(1)
    print("listening")
    
    while True:
        c, addr = s.accept()
        print(f'Connection to {addr} etablished')

        # receive request
        req_received = c.recv(1024).decode()
        ack_msg = f'RECEIVED: {req_received}'
        print(ack_msg)
        #c.send(f'From server: {ack_msg}'.encode())

        # send response
        http_response = "HTTP/1.1 200 OK\r\n\r\nRequested path: <the path>\r\n"
        c.send(http_response.encode())
        
        c.close
        break
        