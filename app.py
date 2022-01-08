import dash

from main_app import app
from index import makeLayout

if __name__ == "__main__":
    app.layout = makeLayout
    app.config.suppress_callback_exceptions = True
    app.run_server(host = '0.0.0.0', port = '8050')
