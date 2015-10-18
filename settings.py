from logging.handlers import RotatingFileHandler
import os
import logging

app_ids = ["gae0x0000", "gae0x0001", "gae0x0002", "gae0x0003", "gae0x0004", "gae0x0005", "gae0x0006"]
google_ip = "59.18.45.59"

debug = False

front_server_address = ('127.0.0.1', 5000)
https_server_address = ('127.0.0.1', 5100)
app_http_server_address = ('127.0.0.1', 5200)
app_https_server_address = ('127.0.0.1', 5300)

timeout = 15
range_required_size = 5 * (2 ** 20)
range_split_size = 2 * (2 ** 20)

app_dir = os.path.dirname(os.path.realpath(__file__))
log_file = os.path.join(app_dir, 'log.txt')
log_file_handler = RotatingFileHandler(log_file, maxBytes=10**6)
logger = logging.getLogger('hope')
logger.setLevel(logging.INFO)
logger.addHandler(log_file_handler)

google_domains = [
    "google.com", "gstatic.com", "appspot.com", "youtube.com", "ytimg.com", "googlemail.com",
    "gmail.com", "blogspot.com", "googlelabs.com", "googleusercontent.com", "ggpht.com",
    "googleapis.com", "google-analytics.com"
    ]
