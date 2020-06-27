import http.server
import socketserver
from functools import partial
import sys

from doof.model import Site

# doof on a keypad
PORT = 3663

Handler = http.server.SimpleHTTPRequestHandler


def serve(site: Site):
    DoofHandler = partial(Handler, directory=str(site.output_path))
    with socketserver.TCPServer(("", PORT), DoofHandler) as httpd:
        print(f"serving at http://localhost:{PORT}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nKeyboard interrupt received, exiting.")
            sys.exit(0)

