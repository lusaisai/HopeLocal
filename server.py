from waitress import serve
from HopeLocal import app, setup_google_connection

setup_google_connection()
serve(app, host='127.0.0.1', port=5000)
