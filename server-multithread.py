# Server.py with multiple clients

#1. Create a socket
import socket
from pathlib import Path
import threading
import sys

class Server(threading.Thread):
    def __init__(self, port=80, host="127.0.0.1"):
        super().__init__()
        self.name = f'{self.__class__.__name__.lower()}'#-{next(self._ids)}
        #self.log_level = log_level
        #self.logger = self._init_logging()
        #self.cmd_queue = cmd_queue

        try: 
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #ipv4, tcp
            print("Socket successfully created")
        except socket.error as err:
            print ("socket creation failed with error %s" %(err))
 
        self.socket.bind((host, port))
        print ("socket binded to %s" %(port)) 
        

    def run(self):
        # activate server to listen for connections
        conn_threads = []
        server = self.socket
        server.listen(3)   # server will accept 3 connections at a time before refusing new cnes.
        print("listening")
        while True:
            c, addr = server.accept()
            print(f'... Connection to {addr} etablished')

            def handle_client(c : socket):
                while True:
                    '''keep processing message unless get no message content. Then close the socket'''
                    req_received = c.recv(1024).decode()
                    print(f'RECEIVED: {req_received}')
                    if not req_received:
                        print(f'Client {addr} disconnected')
                        c.close()
                        return
                    else:
                        req = self.__parse_request(req_received)
                        c.send(self.__get_http_response(req).encode())
        
            # each connection is handled by a new thread
            thd = threading.Thread(target=handle_client, args=(c,))
            thd.start()
            conn_threads.append(thd)


    def __get_http_response(self, req : dict) -> str:
        '''returns http response based on given request'''
        # ideally have a dictionary of http_codes- code should derive from a series of checks
        if req.get('req_type') == 'GET' and req.get('req_http_ver') == 'HTTP/1.1':
            http_code = '200 OK'
            try: 
                body = self.__fetch_document_at_path(req.get('req_value'))
                header = f"{req.get('req_http_ver')} {http_code}\r\n\r\n"
                
            except FileNotFoundError as e:
                http_code, body = '404 Not Found', ''
                header = f"{http_code}"
        else:
            http_code, body = '400 Bad Request', ''
            header = f"{http_code}"
        response_str = header + body
        return response_str

    @staticmethod
    def __fetch_document_at_path(path: str) -> str:
        '''return contents of document at specified relative filepath'''
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
        
    @staticmethod    
    def __parse_request(req_msg: str) -> dict:
        '''Parses http request string into a dictionary object''' 
        split_strs = req_msg.split()
        req = dict()
        req['req_type'] = split_strs[0]
        req['req_value'] = split_strs[1]
        req['req_http_ver'] = split_strs[2]
        return req     
        

    def stop_server():
        while True:
            cmd = input("Type ctrl-c to stop server")
            if cmd == "C":
                return True
            else:
                return False


if __name__ == '__main__':
    server = Server()
    server.start()    
