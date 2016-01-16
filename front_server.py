import socket
import SocketServer
import settings
import re
from tunnel import Tunnel


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

        Tunnel.tunnelling(self.request, s)

    @staticmethod
    def is_google_domain(domain):
        for google_domain in settings.google_domains:
            if google_domain in domain:
                return True

        return False


if __name__ == '__main__':
    server = SocketServer.ThreadingTCPServer(settings.front_server_address, HopeRequestHandler)
    server.serve_forever()
