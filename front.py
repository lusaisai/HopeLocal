import socket
import threading
import SocketServer
import settings
import re


class HopeRequestHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        # check https
        data = self.request.recv(2**5)
        method, other = re.split(r'\s+', data, maxsplit=1)
        if method == 'CONNECT':
            self.request.recv(4096)
            self.request.send('HTTP/1.1 200 OK\r\n')
            self.request.send('Content-Length: 0\r\n')
            self.request.send('\r\n')
            s = socket.socket()
            s.connect(settings.https_server)
        else:
            s = socket.socket()
            s.connect(settings.app_server)
            s.sendall(data)

        t1 = HopeTunnel(self.request, s)
        t1.start()
        t2 = HopeTunnel(s, self.request)
        t2.start()
        t1.join()
        t2.join()


class HopeTunnel(threading.Thread):
    def __init__(self, incoming, outgoing):
        super(HopeTunnel, self).__init__()
        self.incoming = incoming
        self.outgoing = outgoing

    def run(self):
        while True:
            data = self.incoming.recv(4096)
            if len(data) == 0:
                break
            else:
                self.outgoing.sendall(data)


if __name__ == '__main__':
    server = SocketServer.ThreadingTCPServer(settings.front_server, HopeRequestHandler)
    server.serve_forever()
