from waitress import serve
from HopeLocal import app, setup_google_connection
import settings

app.config['SCHEME'] = 'https'
setup_google_connection()
serve(app, host=settings.app_https_server_address[0], port=settings.app_https_server_address[1])
