from waitress import serve
from HopeLocal import app, setup_google_connection
import settings

app.config['SCHEME'] = 'http'
setup_google_connection()
serve(app, host=settings.app_http_server_address[0], port=settings.app_http_server_address[1])
