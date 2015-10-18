from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from SocketServer import ThreadingMixIn
import requests
import settings
import random
import sys
from google_connection import setup_google_connection

TARGET_SCHEME = "http"


class ThreadingHTTPServer(ThreadingMixIn, HTTPServer):
    pass


class HopeAppRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.do("GET")
        return None

    def do_HEAD(self):
        self.do("HEAD")
        return None

    def do_DELETE(self):
        self.do("DELETE")
        return None

    def do_PUT(self):
        self.do("PUT")
        return None

    def do_POST(self):
        self.do("POST")
        return None

    def do(self, method):
        host = self.headers['host']
        if host.startswith('127.0.0.1') or host.startswith('localhost'):
            self.send_response(200)
            self.end_headers()
            self.wfile.write("Hope app server")
            return None

        app_id = random.choice(settings.app_ids)
        headers = {key: value for key, value in self.headers.items()}
        if TARGET_SCHEME == 'http':
            headers['target_url'] = self.path.replace("http", TARGET_SCHEME)
        else:
            headers['target_url'] = "https://" + host + self.path
        headers["host"] = app_id + ".appspot.com"

        if settings.debug:
            url = "http://localhost:9000/hope/"
        else:
            url = "https://%s.appspot.com/hope/" % app_id

        if 'content-length' in self.headers:
            body = self.rfile.read(int(self.headers['content-length']))
        else:
            body = None

        r = requests.request(method=method, url=url, data=body, headers=headers, allow_redirects=False)
        self.send_response(r.status_code)
        self.pass_headers(r)
        self.send_header('content-length', len(r.content))
        self.end_headers()
        self.wfile.write(r.content)

        return None

    def pass_headers(self, response):
        headers_to_ignore = {'content-encoding', 'content-length', 'transfer-encoding', 'connection'}
        for header in response.headers:
            if header not in headers_to_ignore:
                if header.startswith('set-cookie-'):
                    self.send_header('set-cookie', response.headers[header])
                else:
                    self.send_header(header, response.headers[header])

if __name__ == '__main__':
    setup_google_connection()

    TARGET_SCHEME = "https"
    if len(sys.argv) == 2:
        scheme = sys.argv[1]
        if scheme not in ['http', 'https']:
            print("scheme should be either http or https")
            sys.exit(1)
        else:
            TARGET_SCHEME = scheme

    if TARGET_SCHEME == 'http':
        server = ThreadingHTTPServer(settings.app_http_server_address, HopeAppRequestHandler)
    else:
        server = ThreadingHTTPServer(settings.app_https_server_address, HopeAppRequestHandler)
    server.serve_forever()
