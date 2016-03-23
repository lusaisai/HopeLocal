from front_server import HopeRequestHandler
from https_server import HopeHttpsRequestHandler
from app_server import ThreadingHTTPServer, HopeAppHttpRequestHandler, HopeAppHttpsRequestHandler
import settings
import SocketServer
from threading import Thread
from ca import setup_certs
from ip_pool import MaintainIPPool


def run_front_server():
    server = SocketServer.ThreadingTCPServer(settings.front_server_address, HopeRequestHandler)
    server.serve_forever()


def run_https_server():
    server = SocketServer.ThreadingTCPServer(settings.https_server_address, HopeHttpsRequestHandler)
    server.serve_forever()


def run_app_http_server():
    server = ThreadingHTTPServer(settings.app_http_server_address, HopeAppHttpRequestHandler)
    server.serve_forever()


def run_app_https_server():
    server = ThreadingHTTPServer(settings.app_https_server_address, HopeAppHttpsRequestHandler)
    server.serve_forever()


def maintain_ip_pool():
    MaintainIPPool().run()


def run_services():
    setup_certs()
    threads = [
        Thread(target=run_front_server),
        Thread(target=run_https_server),
        Thread(target=run_app_http_server),
        Thread(target=run_app_https_server),
        Thread(target=maintain_ip_pool)
    ]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

if __name__ == '__main__':
    run_services()
