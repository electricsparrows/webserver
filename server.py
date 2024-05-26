# Server.py 

#1. Create a socket
import socket
from pathlib import Path

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
        s = socket.socket()
        print("Socket successfully created")
    except socket.error as err:
        print ("socket creation failed with error %s" %(err))

    port = 80
    host= "127.0.0.1"
    s.bind((host, port))
    print ("socket binded to %s" %(port)) 
    
    # activate server to listen for connections
    s.listen(1)
    print("listening")
    while True:
        c, addr = s.accept()
        print(f'Connection to {addr} etablished')

        # receive request
        req_received = c.recv(1024).decode()
        print(f'RECEIVED: {req_received}')
        ## parse message
        req = parse_request(req_received)
        # send response
        #http_response = "HTTP/1.1 200 OK\r\n\r\nRequested path: <the path>\r\n"
        c.send(get_http_response(req).encode())
        c.close
        break



if __name__ == '__main__':
    create_server()
    """ req1 = "GET / HTTP/1.1"
    req2 = "GET /inde.html HTTP/1.1"
    req3 = "POST / HTTP/1.1"

    req1 = parse_request(req1)
    req2 = parse_request(req2)
    req3 = parse_request(req3)

    s1 = get_http_response(req1)
    s2 = get_http_response(req2)
    s3 = get_http_response(req3)

    print(s2, sep='\n\n') """

