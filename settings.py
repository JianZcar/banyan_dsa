import socket


class ConnectServer(socket.socket):
    def __init__(self):
        super().__init__(socket.AF_INET, socket.SOCK_STREAM)
        self.connect(('localhost', 12345))
