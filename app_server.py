from waitress import serve
from HopeLocal import app, setup_google_connection
import logging
from logging.handlers import RotatingFileHandler
import os
import settings

APP_DIR = os.path.dirname(os.path.realpath(__file__))

file_handler = RotatingFileHandler(os.path.join(APP_DIR, 'log.txt'), maxBytes=10**6)
file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s'))
app.logger.addHandler(file_handler)
setup_google_connection()
serve(app, host=settings.app_server_address[0], port=settings.app_server_address[1])
