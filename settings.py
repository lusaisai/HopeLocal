import os


app_ids = ["gae0x0006"]
google_ip = "59.18.45.59"
debug = False
front_server_address = ('127.0.0.1', 5000)
https_server_address = ('127.0.0.1', 5100)
app_http_server_address = ('127.0.0.1', 5200)
app_https_server_address = ('127.0.0.1', 5300)
app_dir = os.path.dirname(os.path.realpath(__file__))

google_domains = [
    "google.com", "gstatic.com", "appspot.com", "youtube.com", "ytimg.com", "googlemail.com",
    "gmail.com", "blogspot.com", "googlelabs.com", "googleusercontent.com", "ggpht.com",
    "googleapis.com", "google-analytics.com"
    ]
