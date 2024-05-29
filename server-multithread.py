# Server.py with multiple clients

#1. Create a socket
import socket
from pathlib import Path
import threading

#this is a helper function
def fetch_document_at_path(path):
    #filepath = os.path.join("./www")
    root = Path("./www")
    if path == "/":
        filepath = root / 'index.html'
    else:
        filepath = root / path.split('/')[-1]
    
    try:
        with open (filepath, "r") as f:
            data = f.read()
        return data
    except FileNotFoundError as e:
        #this shouldn't crash the server
        #logging
        raise e
    
# these are more processing 'steps'
def parse_request(req_msg: str) -> dict: 
    split_strs = req_msg.split()
    req = dict()
    req['req_type'] = split_strs[0]
    req['req_value'] = split_strs[1]
    req['req_http_ver'] = split_strs[2]
    return req

def get_http_response(req) -> str:
    # ideally have a dictionary of http_codes- code should derive from a series of checks
    if req.get('req_type') == 'GET' and req.get('req_http_ver') == 'HTTP/1.1':
        http_code = '200 OK'
        try: 
            body = fetch_document_at_path(req.get('req_value'))
            header = f"{req.get('req_http_ver')} {http_code}\r\n\r\n"
            
        except FileNotFoundError as e:
            http_code, body = '404 Not Found', ''
            header = f"{http_code}"
    else:
        http_code, body = '400 Bad Request', ''
        header = f"{http_code}"
    
    response_str = header + body
    return response_str
        

def create_server():
    # initiate the server
    try: 
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #ipv4, tcp
        print("Socket successfully created")
    except socket.error as err:
        print ("socket creation failed with error %s" %(err))

    port = 80
    host= "127.0.0.1"
    s.bind((host, port))
    print ("socket binded to %s" %(port)) 
    
    # activate server to listen for connections
    s.listen(3)   # server will accept 3 connections at a time before refusing new cnes.
    print("listening")
    return s



if __name__ == '__main__':
    server = create_server()

    while True:
        c, addr = server.accept()
        print(f'... Connection to {addr} etablished')

        #client.send(bytes(server.greeting()), 'ascii')
        def handle_client(c : socket):
            while True:
                req_received = c.recv(1024).decode()
                print(f'RECEIVED: {req_received}')
                if not req_received:
                    print(f'Client {addr} disconnected')
                    c.close()
                    break
                else:
                    req = parse_request(req_received)
                    c.send(get_http_response(req).encode())
        
        handle_client(c)

        # Idea is that: everytime a connection is opened --> start a new thread
        #thd1 = threading.Thread(target=handle_client)
        # complete processing
        # rejoin thread

        print('in main server loop')
