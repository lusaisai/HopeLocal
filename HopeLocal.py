from flask import Flask, request, make_response
import requests
import settings
import random


app = Flask(__name__, static_url_path='/\x00\x00\x00\x00\x00\x00\x00\x00/')  # do not serve static


def setup_google_connection():
    from requests.packages.urllib3.util import connection
    from google_connection import create_google_connection
    connection.create_connection = create_google_connection


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def agent(path):
    if request.host.startswith('127.0.0.1'):
        return ''

    app_id = random.choice(settings.app_ids)
    headers = {key: value for key, value in request.headers.items() if len(value) > 0}
    headers['target_url'] = request.url
    headers["Host"] = app_id + ".appspot.com"
    cookies = dict(request.cookies)

    if settings.debug:
        url = "http://localhost:9000/"
    else:
        url = "https://%s.appspot.com/" % app_id

    if request.method == "GET":
        r = requests.get(url, headers=headers, cookies=cookies, allow_redirects=False)
        response = make_response(r.content)
        setup_response_info(r, response)
        return response
    else:
        return ''


def setup_response_info(incoming, outgoing):
    headers_to_keep = {'content-encoding', 'content-length'}
    headers_to_delete = {'transfer-encoding'}
    for header in incoming.headers:
        if header not in headers_to_keep and header not in headers_to_delete:
            outgoing.headers[header] = incoming.headers[header]

    outgoing.status_code = incoming.status_code


if __name__ == '__main__':
    app.debug = settings.debug
    if not settings.debug:
        setup_google_connection()
    app.run()
