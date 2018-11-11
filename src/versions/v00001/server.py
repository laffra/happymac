import activity
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
import log
import sys
import threading
from urlparse import urlparse, parse_qs

port_number = 1187
reload(sys)
sys.setdefaultencoding('utf-8')

class Server(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith("/happymac?"):
            query = parse_qs(urlparse(self.path).query)
            url = urlparse(query.get('url', [''])[0]).netloc
            title = query.get('title', [''])[0]
            fav = query.get('fav', [''])[0]
            activity.update_tab(url, fav, title)

    def log_message(self, format, *args):
        return

class Runner(threading.Thread):
    def run(self):
        global port_number
        while True:
            try:
                log.log("Start server on port number %d" % port_number)
                HTTPServer(('', port_number), Server).serve_forever()
            except Exception as e:
                log.log("Port number %d already in use: %s" % (port_number, e))
                port_number += 1


def start():
    log.log("Start the server")
    Runner().start()
