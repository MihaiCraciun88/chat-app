import socket
import threading


class Server:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connections = []
    is_running = True

    def __init__(self):
        self.sock.bind(('0.0.0.0', 8888))
        self.sock.listen(1)

    def handler(self, conn, address):
        while True:
            data = conn.recv(1024)
            data_decoded = str(data, 'utf-8')
            # send to all clients except the one who send it
            for connection in self.connections:
                if self.get_id(connection) != self.get_id(conn):
                    connection.send(data)

            if data_decoded == '/stopserv':
                self.is_running = False
                data_decoded = '/close'
                self.sock.close()

            if data_decoded == '/close':
                print(self.get_id(conn) + ' disconnected')
                self.connections.remove(conn)
                conn.close()
                break

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