from logging.handlers import RotatingFileHandler
import os
import logging

# AKA Project ID
app_ids = ["app_id1", "app_id2"]

# It's better to be fast and stable, and of course not blocked.
google_ip = "59.18.45.59"

# For development
using_dev_app_engine = False

# Service addresses, front server address is the one to be used in client proxy configuration.
front_server_address = ('127.0.0.1', 5000)
https_server_address = ('127.0.0.1', 5100)
app_http_server_address = ('127.0.0.1', 5200)
app_https_server_address = ('127.0.0.1', 5300)

# (connect timeout, read timeout)
timeout = (10, 30)

# For now, url extensions is used to detect a potentially large file.
# If it is large, the file will be downloaded in blocks.
large_file_extensions = ["mp4", "webm", "m4v", "flv", "mp3", "m4a", "ogg",
                         "exe", "msi", "zip", "rar", "tar.gz", "pdf"]
range_required_size = 5 * (2 ** 20)
range_split_size = 2 ** 20
range_concurrent_requests = 5

app_dir = os.path.dirname(os.path.realpath(__file__))

# Logging is not fully implemented, it is mainly for development for now.
log_file = os.path.join(app_dir, 'log.txt')
log_file_handler = RotatingFileHandler(log_file, maxBytes=2**20)
logger = logging.getLogger('hope')
logger.setLevel(logging.ERROR)
logger.addHandler(log_file_handler)

# These domains will be connected directly.
# Don't add youtube.com into it, it may break the video playback when connecting to youtube.com and googlevideo.com
# from different ips
google_domains = [
    "google.com", "gstatic.com", "appspot.com", "ytimg.com", "googlemail.com",
    "gmail.com", "blogspot.com", "googlelabs.com", "googleusercontent.com", "ggpht.com",
    "googleapis.com", "google-analytics.com"
    ]

# A website may break its session when a new request comes from a different app, this will fix it.
domain_use_specific_app = {
    "www.domainx.com": "app_idx",
    "www.domainy.com": "app_idy"
}

# User settings
try:
    from user_settings import *
except ImportError:
    pass
