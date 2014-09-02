import argparse
import BaseHTTPServer
import sys
import markdown

__version__ = '0.0.1'

PORT = 8080

class Handler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        html = markdown.markdown(open(sys.argv[1],'rb').read())
        self.wfile.write(html)


if __name__ == '__main__':
    httpd = BaseHTTPServer.HTTPServer(("localhost", PORT), Handler)
    httpd.serve_forever()
