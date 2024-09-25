#!/usr/bin/env python3
import os
from app import create_app

app = create_app()


if __name__ == "__main__":
    # app.run(host='192.168.8.100', debug=True)
    # setting the host to 0.0.0.0 due to a server issue on render.com
    host = '0.0.0.0'

    # setting the env. variable default to 10000 if not set
    port = int(os.environ.get('port', 9000))

    # Run the flask app
    app.run(host=host, port=port)