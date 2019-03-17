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

            if data == b'/stopserver':
                self.is_running = False

            if data == b'/close':
                print(self.get_id(conn) + ' disconnected')
                self.connections.remove(conn)
                conn.close()
                break

            for connection in self.connections:
                if not self.is_running:
                    self.connections.remove(connection)
                    connection.close()
                    continue

                # send to all clients except the one who send it
                if self.get_id(connection) != self.get_id(conn):
                    connection.send(bytes(self.get_id(conn) + ': ', 'utf-8') + data)

            if not self.is_running:
                self.sock.close()
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