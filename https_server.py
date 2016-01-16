import socket
import ssl
import SocketServer
import settings
from tunnel import Tunnel
from ca import setup_domain_cert, get_domain_cert_file_path


class HopeHttpsRequestHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        length = int(self.request.recv(4))
        domain = self.request.recv(length)
        setup_domain_cert(domain)
        ssl_request = ssl.wrap_socket(self.request, certfile=get_domain_cert_file_path(domain),
                                      keyfile=get_domain_cert_file_path(domain), server_side=True)
        s = socket.socket()
        s.connect(settings.app_https_server_address)
        Tunnel.tunnelling(ssl_request, s)


if __name__ == '__main__':
    server = SocketServer.ThreadingTCPServer(settings.https_server_address, HopeHttpsRequestHandler)
    server.serve_forever()
