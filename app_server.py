from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from SocketServer import ThreadingMixIn
import socket
import re
import requests
from ca import setup_certs
import settings
import random
from google_connection import setup_google_connection
from multiprocessing import Process
from threading import Thread, Semaphore, Lock
import time
from enum import Enum


class RangeRequestStatus(Enum):
    ready = 0
    retrying = 1
    succeeded = 2
    failed = 3


class ThreadingHTTPServer(ThreadingMixIn, HTTPServer):
    pass


class HopeAppRequestHandler(BaseHTTPRequestHandler):
    TARGET_SCHEME = None

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

    # It breaks when started without console, so make it silent.
    def log_message(self, message, *args):
        try:
            settings.logger.info(('"Host: %s" ' + message) % ((self.headers['host'],) + args))
        except RuntimeError:
            pass
        return

    def do(self, method):
        host = self.headers['host']
        if host.startswith('127.0.0.1') or host.startswith('localhost'):
            self.send_response(200)
            self.end_headers()
            self.wfile.write("Hope app server")
            return None

        headers = {key: value for key, value in self.headers.items()}
        url = self.setup_google_headers(headers)

        if 'content-length' in self.headers:
            body = self.rfile.read(int(self.headers['content-length']))
        else:
            body = None

        if method == "GET" and self.guess_range_required(headers):
            r = requests.head(url=url, data=body, headers=headers, allow_redirects=False)
            size = int(r.headers['Source-Content-Length']) if 'Source-Content-Length' in r.headers else 0
            if str(r.status_code).startswith('2') and size > settings.range_required_size:
                if "range" in headers:
                    range_bytes = headers["range"].split('=')[1].split('-')
                    start = int(range_bytes[0])
                    target = int(range_bytes[1]) if range_bytes[1] else start + size - 1
                else:
                    start = 0
                    target = size - 1
                self.make_range_requests(headers, start, target, r)
            else:
                self.make_normal_requests(method, url, body, headers)

        else:
            self.make_normal_requests(method, url, body, headers)

        return None

    def setup_google_headers(self, headers):
        host = self.headers['host']
        app_id = self.get_app_id()
        if self.TARGET_SCHEME == 'http':
            target_url = self.path.replace("http", self.TARGET_SCHEME)
        else:
            target_url = "https://" + host + self.path

        headers['target_url'] = target_url
        headers["host"] = app_id + ".appspot.com"

        if settings.using_dev_app_engine:
            url = "http://localhost:9000/hope/"
        else:
            url = "https://%s.appspot.com/hope/" % app_id
            setup_google_connection()

        return url

    def get_app_id(self):
        for key, value in settings.domain_use_specific_app.items():
            if key in self.headers['host']:
                return value

        return random.choice(settings.app_ids)

    def send_common_headers(self, response):
        self.send_response(response.status_code)
        self.pass_headers(response)
        self.send_header('content-length', len(response.content))
        self.end_headers()

    def make_normal_requests(self, method, url, body, headers):
        try:
            r = requests.request(method=method, url=url, data=body, headers=headers,
                                 allow_redirects=False, timeout=settings.timeout)
            self.send_common_headers(r)
            self.wfile.write(r.content)
            self.wfile.close()
        except requests.exceptions.RequestException, socket.error:
            self.wfile.close()

    def make_range_requests(self, headers, start, target, head_response):
        try:
            is_original_range_request = True if 'range' in headers else False
            headers.pop('if_modified_since', None)
            range_bytes = "bytes=%s-%s" % (start, start + settings.range_split_size - 1)
            headers['range'] = range_bytes

            # first request
            url = self.setup_google_headers(headers)  # reset google app to avoid OverQuotaError
            r = requests.get(url=url, headers=headers, allow_redirects=False)
            if r.status_code == 206:
                if is_original_range_request:
                    self.send_response(206)
                    self.pass_headers(r, ignore={'content-range'})
                    self.send_header('content-range', 'bytes %s-%s/*' % (start, target))
                else:
                    self.send_response(200)
                    self.pass_headers(head_response)

                self.send_header('content-length', target - start + 1)
                self.end_headers()
                self.wfile.write(r.content)
            else:
                self.send_error(500)
                self.end_headers()
                self.wfile.close()
            start += settings.range_split_size

            # the rest range requests
            requests_left, size_left = divmod(target - start + 1, settings.range_split_size)
            total_requests = requests_left if size_left == 0 else requests_left + 1
            data_splits = [RangeRequestStatus.ready] * total_requests
            data_lock = Lock()
            threads = []
            semaphore = Semaphore(settings.range_concurrent_requests)
            for index in range(total_requests):
                range_bytes = "bytes=%s-%s" % (start, min(start + settings.range_split_size - 1, target))
                headers_copy = dict(headers)
                headers_copy['range'] = range_bytes
                threads.append(Thread(target=self.fetch_range_data, args=(semaphore, headers_copy, data_splits,
                                                                          data_lock, index)))
                start += settings.range_split_size

            threads.append(Thread(target=self.write_range_data, args=(data_splits, data_lock)))
            for thread in threads:
                thread.start()
            for thread in threads:
                thread.join()

            self.wfile.close()
        except requests.exceptions.RequestException, socket.error:
            self.wfile.close()

    @staticmethod
    def range_progress_inspect(data_splits):
        inspect = []
        for item in data_splits:
            if isinstance(item, RangeRequestStatus):
                inspect.append(item.name)
            else:
                inspect.append(len(item))
        sent_count = 0
        for item in inspect:
            if item == RangeRequestStatus.succeeded.name:
                sent_count += 1
            else:
                break
        print(['sent * %s' % sent_count] + inspect[sent_count:])

    def write_range_data(self, data_splits, data_lock):
        for index in range(len(data_splits)):
            while True:
                data_lock.acquire()

                # self.range_progress_inspect(data_splits)

                content = data_splits[index]
                if content is RangeRequestStatus.ready or content is RangeRequestStatus.retrying:
                    data_lock.release()
                    if RangeRequestStatus.failed in data_splits:
                        self.wfile.close()
                        return
                    else:
                        time.sleep(0.5)
                else:
                    try:
                        self.wfile.write(content)
                        data_splits[index] = RangeRequestStatus.succeeded
                        # if index == len(data_splits) - 1:
                        #     self.range_progress_inspect(data_splits)
                        data_lock.release()
                        break
                    except socket.error:
                        data_lock.release()
                        self.wfile.close()
                        return None

    def fetch_range_data(self, semaphore, headers, data, data_lock, index):
        semaphore.acquire()
        if self.wfile.closed:
            data_lock.acquire()
            data[index] = RangeRequestStatus.failed
            data_lock.release()
            semaphore.release()
            return None

        for _ in range(5):
            url = self.setup_google_headers(headers)  # reset google app to avoid OverQuotaError
            try:
                r = requests.get(url=url, headers=headers, allow_redirects=False, timeout=settings.timeout)
            except requests.exceptions.RequestException:
                data_lock.acquire()
                data[index] = RangeRequestStatus.retrying
                data_lock.release()
                continue

            data_lock.acquire()
            if r.status_code == 206:
                data[index] = r.content
                data_lock.release()
                break
            else:
                data[index] = RangeRequestStatus.retrying
                data_lock.release()

        data_lock.acquire()
        if data[index] is RangeRequestStatus.retrying:
            data[index] = RangeRequestStatus.failed
        data_lock.release()

        semaphore.release()

    @staticmethod
    def guess_range_required(headers):
        url = re.sub(r'\?.*', '', headers['target_url']).lower()
        for extension in settings.large_file_extensions:
            if url.endswith(extension):
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


class HopeAppHttpRequestHandler(HopeAppRequestHandler):
    TARGET_SCHEME = 'http'


class HopeAppHttpsRequestHandler(HopeAppRequestHandler):
    TARGET_SCHEME = 'https'


def run_app_http_server():
    server = ThreadingHTTPServer(settings.app_http_server_address, HopeAppHttpRequestHandler)
    server.serve_forever()


def run_app_https_server():
    server = ThreadingHTTPServer(settings.app_https_server_address, HopeAppHttpsRequestHandler)
    server.serve_forever()

if __name__ == '__main__':
    setup_certs()
    processes = [
        Process(target=run_app_http_server),
        Process(target=run_app_https_server)
    ]

    for process in processes:
        process.start()
    for process in processes:
        process.join()
