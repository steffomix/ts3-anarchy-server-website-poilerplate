#!/usr/bin/env python3
"""Read-only HTTP server: serves only index.html and images/*.png on port 8080."""

import http.server
import socketserver
import logging
import os
import posixpath
import re
import urllib.parse

PORT = 8080
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DIRECTORY = os.path.join(BASE_DIR, "www")
LOG_FILE = os.path.join(BASE_DIR, "log", "server.log")

# Only these paths are allowed (GET/HEAD, read-only)
_ALLOWED = re.compile(r'^(/|/index\.html|/images/[^/]+\.png)$')

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def _allowed(self):
        """Normalize and validate the request path. Returns True if allowed."""
        parsed = urllib.parse.urlsplit(self.path)
        # Decode percent-encoding and collapse any .. / . segments
        normalized = posixpath.normpath(urllib.parse.unquote(parsed.path))
        if not _ALLOWED.match(normalized):
            self.send_error(404, "Not Found")
            return False
        return True

    def do_GET(self):
        if self._allowed():
            super().do_GET()

    def do_HEAD(self):
        if self._allowed():
            super().do_HEAD()

    def do_POST(self):
        self.send_error(405, "Method Not Allowed")

    def do_PUT(self):
        self.send_error(405, "Method Not Allowed")

    def do_DELETE(self):
        self.send_error(405, "Method Not Allowed")

    def do_OPTIONS(self):
        self.send_error(405, "Method Not Allowed")

    def log_message(self, format, *args):
        logger.info("%s - %s", self.address_string(), format % args)


if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        logger.info("Serving %r on port %d", DIRECTORY, PORT)
        httpd.serve_forever()
