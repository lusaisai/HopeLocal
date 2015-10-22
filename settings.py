from logging.handlers import RotatingFileHandler
import os
import logging


app_ids = ["app_id1", "app_id2"]
google_ip = "59.18.45.59"

using_dev_app_engine = False

front_server_address = ('127.0.0.1', 5000)
https_server_address = ('127.0.0.1', 5100)
app_http_server_address = ('127.0.0.1', 5200)
app_https_server_address = ('127.0.0.1', 5300)

timeout = 10

large_file_extensions = ["mp4", "webm", "m4v", "flv", "mp3", "m4a", "ogg",
                         "exe", "msi", "zip", "rar", "tar.gz"]
range_required_size = 5 * (2 ** 20)
range_split_size = 2 ** 20
range_concurrent_requests = 10

app_dir = os.path.dirname(os.path.realpath(__file__))

log_file = os.path.join(app_dir, 'log.txt')
log_file_handler = RotatingFileHandler(log_file, maxBytes=2**20)
logger = logging.getLogger('hope')
logger.setLevel(logging.ERROR)
logger.addHandler(log_file_handler)

google_domains = [
    "google.com", "gstatic.com", "appspot.com", "youtube.com", "ytimg.com", "googlemail.com",
    "gmail.com", "blogspot.com", "googlelabs.com", "googleusercontent.com", "ggpht.com",
    "googleapis.com", "google-analytics.com"
    ]

#  a website may break its session when a new request comes from a different app, this will fix it.
domain_use_specific_app = {
    "www.your_domain.com": "your_app_id"
}

try:
    from user_settings import *
except ImportError:
    pass
