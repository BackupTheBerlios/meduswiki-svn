#!/usr/bin/env python

import BaseHTTPServer
import CGIHTTPServer

def run(server_class=BaseHTTPServer.HTTPServer,
        handler_class=CGIHTTPServer.CGIHTTPRequestHandler):
    server_address = ('', 8000)
    handler_class.cgi_directories = ['']
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()

run()
