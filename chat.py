import sys
import socket
import threading
from includes import *


class Chat:
    address = '127.0.0.1'
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    protocol = Protocol()

    def __init__(self, address):
        if address:
            self.address = address
        self.sock.connect((self.address, 8888))

        inputThread = threading.Thread(target=self.send)
        inputThread.daemon = True
        inputThread.start()

        while True:
            try:
                data = self.protocol.receive(self.sock.recv(1024))
                if data['action'] == Protocol.CHAT:
                    print(data['message'])
                if data['action'] == Protocol.DISCONNECT:
                    break
            except Exception as e:
                print(e)
                print('Connection closed')
                break

    def send(self):
        while True:
            data = self.protocol.send(Protocol.CHAT, Protocol.PLAIN_TEXT, input(''))
            self.sock.send(data)


if __name__== '__main__':
    address = None
    if len(sys.argv) > 1:
        address = sys.argv[1]
    chat = Chat(address)
