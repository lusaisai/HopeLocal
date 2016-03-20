import socket
from requests.packages.urllib3.util import connection
import ip_pool


def create_google_connection(address, timeout=socket._GLOBAL_DEFAULT_TIMEOUT,
                      source_address=None, socket_options=None):
    sock = None
    try:
        sock = socket.socket()
        connection._set_socket_options(sock, socket_options)
        if timeout is not socket._GLOBAL_DEFAULT_TIMEOUT:
            sock.settimeout(timeout)
        if source_address:
            sock.bind(source_address)
        sock.connect((ip_pool.google_ips_heap[0][1], 443))

        return sock
    except socket.error as err:
        if sock is not None:
            sock.close()

        if err is not None:
            raise err
        else:
            raise socket.error("getaddrinfo returns an empty list")


def setup_google_connection():
    connection.create_connection = create_google_connection