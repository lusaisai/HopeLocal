import socket
from requests.packages.urllib3.util import connection
from settings import google_ip


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
        sock.connect((google_ip, 443))

        return sock
    except socket.error as err:
        if sock is not None:
            sock.close()

        if err is not None:
            raise err
        else:
            raise socket.error("getaddrinfo returns an empty list")
