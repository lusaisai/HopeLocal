import socket
import ssl
import SocketServer
import settings
import os
from front_server import HopeTunnel
from ca import setup_certs, cert_dir


class HopeHttpsRequestHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        length = int(self.request.recv(4))
        domain = self.request.recv(length)
        cert_file = os.path.join(cert_dir, domain+'.crt')
        setup_certs(domain)
        ssl_request = ssl.wrap_socket(self.request, certfile=cert_file, keyfile=cert_file, server_side=True)
        s = socket.socket()
        s.connect(settings.app_https_server_address)
        HopeTunnel.tunnelling(ssl_request, s)


if __name__ == '__main__':
    server = SocketServer.ThreadingTCPServer(settings.https_server_address, HopeHttpsRequestHandler)
    server.serve_forever()
