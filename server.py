import socket
import threading
from includes import *


class Server:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connections = []
    is_running = True

    def __init__(self):
        self.sock.bind(('0.0.0.0', 8888))
        self.sock.listen(1)

    def handler(self, conn, address):
        protocol = Protocol()
        while True:
            data = protocol.receive(conn.recv(1024))

            if data['message'] == '/stopserver':
                for connection in self.connections:
                    connection.send(protocol.send(Protocol.DISCONNECT, 0, ''))
                self.is_running = False
                self.sock.close()
                break

            if data['message'] == '/close':
                print(self.get_id(conn) + ' disconnected')
                self.connections.remove(conn)
                conn.close()
                break

            for connection in self.connections:
                # send to all clients except the one who send it
                if self.get_id(connection) != self.get_id(conn):
                    message = protocol.send(Protocol.CHAT, Protocol.PLAIN_TEXT, self.get_id(conn) + ': ' + data['message'])
                    connection.send(message)

    def get_id(self, connection):
        address = connection.getpeername()
        return str(address[0]) + ':' + str(address[1])

    def run(self):
        while self.is_running:
            try:
                conn, address = self.sock.accept()
                connThread = threading.Thread(target=self.handler, args=(conn, address))
                connThread.daemon = True
                connThread.start()
                self.connections.append(conn)
                print(self.get_id(conn) + ' connected')
            except Exception:
                pass


if __name__== '__main__':
    server = Server()
    server.run()