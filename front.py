import socket
import threading
import SocketServer
import settings


class HopeRequestHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        s = socket.socket()
        s.connect(settings.app_server)
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
