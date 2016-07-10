import settings
import SocketServer
import ip_pool


class InfoTCPHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        self.request.settimeout(2 * settings.ip_check_interval)
        while True:
            data = self.request.recv(4096)
            if data == "info":
                self.request.sendall("Google IP: %s, RTT: %s" % tuple(reversed(ip_pool.google_ips_heap[0])))
            else:
                self.request.sendall("Unrecognized query: %s" % data)

if __name__ == '__main__':
    server = SocketServer.ThreadingTCPServer(settings.info_server_address, InfoTCPHandler)
    server.serve_forever()
