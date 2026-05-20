#!/usr/bin/env python3
"""Simple HTTP file server serving the ./www directory on port 80."""

import http.server
import socketserver
<<<<<<< HEAD
import os

PORT = 8080
DIRECTORY = os.path.join(os.path.dirname(os.path.abspath(__file__)), "www")
=======
import logging
import os

PORT = 8080
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DIRECTORY = os.path.join(BASE_DIR, "www")
LOG_FILE = os.path.join(BASE_DIR, "log", "server.log")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)
>>>>>>> 1648e9f (some updates)


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

<<<<<<< HEAD

if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Serving {DIRECTORY!r} on port {PORT}")
=======
    def log_message(self, format, *args):
        logger.info("%s - %s", self.address_string(), format % args)


if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        logger.info("Serving %r on port %d", DIRECTORY, PORT)
>>>>>>> 1648e9f (some updates)
        httpd.serve_forever()
