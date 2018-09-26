#!/usr/bin/python3

"""
Very simple HTTP server in python.
Usage::
    ./dummy-web-server.py [<port>]
Send a GET request::
    curl http://localhost
Send a HEAD request::
    curl -I http://localhost
Send a POST request::
    curl -d "foo=bar&bin=baz" http://localhost
"""
import urllib
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer

from parser import DATE_FORMATS


class Server(BaseHTTPRequestHandler):

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_HEAD(self):
        self._set_headers()

    def send_result(self, value):
        print(datetime.now())
        print(value)
        print('*' * 80)
        # logger.debug('result: %s' % value)
        self.wfile.write(bytes(str(value), "utf-8"))

    def do_GET(self):
        # Doesn't do anything with posted data
        self._set_headers()
        vars = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)

        str_date = vars['date'][0]

        with open('unparsered.txt', 'w') as unparsered:
            if 'данных' in str_date.lower() or 'ожидается' in str_date.lower():
                return self.send_result(None)
            parsered = False
            for pattern, converter in DATE_FORMATS:
                if pattern.match(str_date):
                    try:
                        date_obj = converter(str_date)
                    except ValueError:
                        continue
                    else:
                        return self.send_result(date_obj.strftime('01.%m.%Y'))
                        parsered = True
                        break
            if not parsered:
                unparsered.write(str_date + '\n')
        return self.send_result(None)


def run(server_class=HTTPServer, handler_class=Server, port=9000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print('Starting httpd...')
    httpd.serve_forever()


if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
