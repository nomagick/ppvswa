#! /usr/bin/python3
"""
Simpile HTTP Server
"""
import os,sys
from http.server import HTTPServer, CGIHTTPRequestHandler

webdir = sys.argv[1] if len(sys.argv) > 1 else '.'
port = sys.argv[2] if len(sys.argv) > 2 else 80

print ('webdir "%s" , port %s' % (webdir , port))

os.chdir(webdir)
srvaddr = ('' , port)
srvobj = HTTPServer(srvaddr, CGIHTTPRequestHandler)
srvobj.serve_forever()