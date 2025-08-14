import socket as sc


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
    
    def read_until(self, marker:str, maxbytes:int=-1) -> bytes:
        marker_pos = self.buffer.find(marker)

        if marker_pos != -1:
            marker_pos += len(marker)
            chunck = self.buffer[:marker_pos]
            self.buffer.clear()
            return bytes(chunck)
        
        elif (maxbytes != -1) and (len(self.buffer) >= maxbytes):
            return bytes()
        
        while self.buffer.find(marker) == -1:
            data_recv = self.recv(4096)
            self.buffer.extend(data_recv)

            if (not data_recv) or (maxbytes != -1 and len(self.buffer) >= maxbytes):
                break
        
        return self.read_until(marker, maxbytes)

ERROR_DICT = {}
CONTENT_TYPE_DICT = {}

class HttpClient():
    def __init__(self, connection_socket:SocketInterface, address:str, root_dir:str):
        self.conn = connection_socket
        self.addr = address
        self.root_dir = root_dir
        self.active = True

    def read_request(self):
        ...

    def send_response(self):
        ...

class HttpServer():
    ...