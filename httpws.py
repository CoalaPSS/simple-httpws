import socket as sc
from typing import List, Tuple

def DEBUG_FLAG():
    print("DEBUG!")

class SocketInterface(sc.socket):
    """
    Interface para abstrair o socket.\n
    Com funções de leitura simplificada de dados.
    """
    def __init__(self, family=sc.AF_INET, type=sc.SOCK_STREAM, proto=0, fileno=None):
        super().__init__(family, type, proto, fileno)    
        self.buffer = bytearray()
    
    def accept(self):
        sock, addr = super().accept()
        fd = sock.fileno()
        sock_interface = SocketInterface(fileno=fd)
        
        sock.detach()
        return sock_interface, addr


    def read(self, size_to_read:int) -> bytes:
        while len(self.buffer) < size_to_read:
            data_recv = self.recv(4096)

            if not data_recv:
                break
            self.buffer.extend(data_recv)
        
        chunck = self.buffer[:size_to_read]
        del self.buffer[:len(chunck)]

        return bytes(chunck)
    
    def read_until(self, marker:bytes, maxbytes:int=-1) -> bytes:
        
        while self.buffer.find(marker) == -1:
            data_recv = self.recv(4096)

            if (maxbytes != -1 and len(self.buffer) >= maxbytes) or (not data_recv):
                chunck = bytes(self.buffer)
                self.buffer.clear()
                return chunck
            
            self.buffer.extend(data_recv)
        

        marker_pos = self.buffer.find(marker)

        chunck_size = marker_pos + len(marker)
        chunck = self.buffer[:chunck_size]

        del self.buffer[:chunck_size]
        return bytes(chunck)

        
    def read_line(self):
        return self.read_until(b'\n')
    
    def print_buffer(self):
        print("Socket Buffer:")
        print(self.buffer.decode('utf-8'))

STATUS_CODE_DICT = {200 : 'OK',
                    201: 'Created'}

ERROR_DICT = {
    400: 'Bad Request',
    404: 'Not Found',
    405: 'Method Not Allowed',
    500: 'Internal Server Error',
    501: 'Not Implemented',
    505: 'HTTP Version Not Supported'
    }

CONTENT_TYPE_DICT = {}

def _parse_req_line(line:bytes) -> list[str]:
    reqline = line.decode('utf-8').strip()
    args = reqline.split(' ')

    if len(args) != 3:
        return ['', '', '']

    return args

def _parse_headers(data:bytes):
    header_dict = {}
    header_lines: List[str] = []
    
    start = 0
    while start < len(data):
        end_of_line = data.find(b'\n', start)
        if end_of_line == -1:
            break

        line = data[start:end_of_line]
        start = end_of_line + 1

        header_lines.append(line.decode('utf-8'))
    
    for line in header_lines:
        if ':' in line:
            key, value = line.split(':', 1)
            header_dict[key] = value.strip()
    
    return header_dict
        
def _print_dict(dic:dict):
    for key, value in dic.items():
        print(f"({key}, {value})")

def _valid_url(url:str):
    ...

class HttpClient():
    def __init__(self, connection_socket:SocketInterface, address:str, root_dir:str):
        self.conn = connection_socket
        self.addr = address
        self.root_dir = root_dir
        self.active = True

    def read_request(self) -> dict:
        request_dict = {}
        req_line = self.conn.read_line()
        
        method, url, protocol = _parse_req_line(req_line)

        if method not in ['GET', 'POST']:
            self.send_error(405)
        
        if not _valid_url(url):
            self.send_error(404)
        
        if protocol not in ['HTTP/1.1', 'HTTP/1.0']:
            self.send_error(505)

        headers = self.conn.read_until(b'\r\n\r\n', maxbytes=8192)
        header_dict = _parse_headers(headers)

        request_dict['method'] = method
        request_dict['url'] = url
        request_dict['protocol'] = protocol
        request_dict['headers'] = header_dict

        # Lidar com dados POST depois
        
        return request_dict 
    
    def serve_file(self):
        ...

    def send_error(self, error_code:int):
        error_message = (
            f"""HTTP/1.1 {error_code} {ERROR_DICT.get(error_code)}
            Content-Type: text/html
            Content-Length: 0""")

        self.conn.sendall(error_message.encode('utf-8'))

    def handle_request(self):
        request = self.read_request()
            
    
    def get(self, path):
        def decorator(handler):
            print(handler)
        return decorator

class HttpServer():
    def __init__(self, addr:str="", port:int=8080):
        self.port = port
        self.addr = addr
        self.ssock = None
    
    def setup(self):
        self.ssock = SocketInterface(sc.AF_INET, sc.SOCK_STREAM)
        self.ssock.setsockopt(sc.SOL_SOCKET, sc.SO_REUSEADDR, 1)
        self.ssock.bind((self.addr, self.port))
        self.ssock.listen(16)
    
    def start(self):
        print(f"HTTP Web Server listening on port {self.port}")
        # Teste
        client_conn, client_addr = self.ssock.accept()
        client = HttpClient(client_conn, client_addr, "/")
        client.handle_request()
        

        # while True:
        #     client_conn, client_addr = self.ssock.accept()

        #     client = HttpClient(client_conn, client_addr, "/")

        #     client.read_request()

server = HttpServer()
server.setup()
server.start()