from front_server import HopeRequestHandler
from https_server import HopeHttpsRequestHandler
from app_server import ThreadingHTTPServer, HopeAppHttpRequestHandler, HopeAppHttpsRequestHandler
import settings
import SocketServer
from multiprocessing import Process
from ca import setup_certs


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


if __name__ == '__main__':
    setup_certs()
    processes = [
        Process(target=run_front_server),
        Process(target=run_https_server),
        Process(target=run_app_http_server),
        Process(target=run_app_https_server)
    ]
    for process in processes:
        process.start()
