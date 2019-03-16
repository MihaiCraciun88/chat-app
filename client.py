import socket
import threading


class Client:
    address = '127.0.0.1'
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __init__(self):
        self.sock.connect((self.address, 8888))

        inputThread = threading.Thread(target=self.send)
        inputThread.daemon = True
        inputThread.start()

        while True:
            data = self.sock.recv(1024)
            if not data:
                break
            print(str(data, 'utf-8'))

    def send(self):
        while True:
            self.sock.send(bytes(input(''), 'utf-8'))


if __name__== '__main__':
    client = Client()