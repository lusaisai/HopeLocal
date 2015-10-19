import socket
import threading
import SocketServer
import settings
import re


class HopeRequestHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        # check https
        data = self.request.recv(4096)
        try:
            method, url, others = re.split(r'\s+', data, maxsplit=2)
            domain, port = re.split(r':', url, maxsplit=1)
        except ValueError:
            method = ''
            domain = ''

        if method == 'CONNECT':
            self.request.send('HTTP/1.1 200 OK\r\n')
            self.request.send('Content-Length: 0\r\n')
            self.request.send('\r\n')
            s = socket.socket()
            if self.is_google_domain(domain):
                s.connect((settings.google_ip, 443))
            else:
                s.connect(settings.https_server_address)
                s.sendall("%s%s" % (str(len(domain)).zfill(4), domain))
        else:
            s = socket.socket()
            s.connect(settings.app_http_server_address)
            s.sendall(data)

        HopeTunnel.tunnelling(self.request, s)

    @staticmethod
    def is_google_domain(domain):
        for google_domain in settings.google_domains:
            if google_domain in domain:
                return True

        return False


class HopeTunnel(threading.Thread):
    def __init__(self, incoming, outgoing):
        super(HopeTunnel, self).__init__()
        self.incoming = incoming
        self.outgoing = outgoing
        self.logger = settings.logger

    def run(self):
        while True:
            try:
                data = self.incoming.recv(4096)
                if len(data) == 0:
                    self.close()
                    break
                else:
                    self.outgoing.sendall(data)
                    # self.logger.info("%s:%s --> %s: %s" % (threading.currentThread().getName(),
                    # self.incoming.getsockname(), self.outgoing.getsockname(), data))
            except socket.error as err:
                # self.logger.info("%s:%s --> %s: %s" % (threading.currentThread().getName(),
                # self.incoming.getsockname(), self.outgoing.getsockname(), err))
                self.close()
                break

    def close(self):
        self.incoming.close()
        self.outgoing.close()

    @classmethod
    def tunnelling(cls, s1, s2):
        t1 = cls(s1, s2)
        t1.start()
        t2 = cls(s2, s1)
        t2.start()
        t1.join()
        t2.join()


if __name__ == '__main__':
    server = SocketServer.ThreadingTCPServer(settings.front_server_address, HopeRequestHandler)
    server.serve_forever()
