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
            target_url = self.path.replace("http", TARGET_SCHEME)
        else:
            target_url = "https://" + host + self.path
        headers['target_url'] = target_url
        headers["host"] = app_id + ".appspot.com"

        if settings.debug:
            url = "http://localhost:9000/hope/"
        else:
            url = "https://%s.appspot.com/hope/" % app_id

        if 'content-length' in self.headers:
            body = self.rfile.read(int(self.headers['content-length']))
        else:
            body = None

        if method == "GET" and self.guess_range_required(headers):
            r = requests.head(url=url, data=body, headers=headers, allow_redirects=False)
            size = int(r.headers['Source-Content-Length']) if 'Source-Content-Length' in r.headers else 0
            if str(r.status_code).startswith('2') and size > settings.range_required_size:
                if "range" in headers:
                    range_bytes = headers["range"].split('=')
                    start, target = range_bytes[1].split('-')[0]
                else:
                    start = 0
                    target = size - 1
                self.make_range_requests(url, headers, start, target)
            else:
                self.make_normal_requests(method, url, body, headers)

        else:
            self.make_normal_requests(method, url, body, headers)

        return None

    def send_common_headers(self, response):
        self.send_response(response.status_code)
        self.pass_headers(response)
        self.send_header('content-length', len(response.content))
        self.end_headers()

    def make_normal_requests(self, method, url, body, headers):
        r = requests.request(method=method, url=url, data=body, headers=headers, allow_redirects=False)
        self.send_common_headers(r)
        self.wfile.write(r.content)

    def make_range_requests(self, url, headers, start, target):
        first_request = True
        while start < target:
            if start + settings.range_split_size - 1 <= target:
                range_bytes = "bytes=%s-%s" % (start, start + settings.range_split_size - 1)
            else:
                range_bytes = "bytes=%s-%s" % (start, target)

            headers['range'] = range_bytes

            for i in range(3):
                r = requests.get(url=url, headers=headers, allow_redirects=False)
                if r.status_code == 206:
                    if first_request:
                        self.send_response(200)
                        self.pass_headers(r, ignore={'content-range'})
                        self.send_header('content-length', target - start + 1)
                        self.send_header('content-range', 'bytes %s-%s/*' % (start, target))
                        self.end_headers()
                        first_request = False
                    self.wfile.write(r.content)
                    break

            start += settings.range_split_size

    @staticmethod
    def guess_range_required(headers):
        extensions = ["mp4", "m4v", "flv", "mp3", "ogg", "exe", "zip", "rar", "tar.gz"]

        url = headers['target_url']
        for extension in extensions:
            if url.lower().endswith(extension):
                return True

        if 'range' in headers:
            return True

        return False

    def pass_headers(self, response, ignore=None):
        headers_to_ignore = {'content-encoding', 'content-length', 'transfer-encoding',
                             'connection', 'source-content-length'}
        if ignore:
            headers_to_ignore.update(ignore)
        for header in response.headers:
            if header not in headers_to_ignore:
                if header.startswith('set-cookie-'):
                    self.send_header('set-cookie', response.headers[header])
                else:
                    self.send_header(header, response.headers[header])

if __name__ == '__main__':
    if not settings.debug:
        setup_google_connection()

    TARGET_SCHEME = "http"
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
