#!/usr/bin/python
# 
# This server, displays the index.html indicated in the fileToServe
#
# Usage: ./simple_webserver.py [<port> <pathToIndexFile>]
################################################################################

## Variables - Default Values
port = 8888 
path = "."
fileToServe = "./index.html"

## Modules to import
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from os import curdir, sep
import sys
import os.path

#This class will handle any incoming request from
#the browser 
class myHandler(BaseHTTPRequestHandler):
	
	#Handle the GET requests
	def do_GET(self):
		if self.path=="/":
			self.path="/index.html"

		try:
			#Check the file extension and
			#set the mime type accordingly

			sendReply = False
			if self.path.endswith(".html"):
				mimetype='text/html'
				sendReply = True
			if self.path.endswith(".jpg"):
				mimetype='image/jpg'
				sendReply = True
			if self.path.endswith(".gif"):
				mimetype='image/gif'
				sendReply = True


			if sendReply == True:
				#Open the static file requested and send it
				f = open(fileToServe) 
				self.send_response(200)
				self.send_header('Content-type',mimetype)
				self.end_headers()
				self.wfile.write(f.read())
				f.close()
			return


		except IOError:
			self.send_error(404,'File Not Found: %s' % self.path)

if __name__ == '__main__':
    #check for proper usage
    if len(sys.argv) > 3:
        print('Run a Web server that listens on a port and responds with webpage ')
        print('from entered path.\n')
        print('Usage:', sys.argv[0], ' [<port> <pathToIndexFile>]')
        sys.exit(1)

    #check that the port entered is a valid port
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
            if port < 1024 or port > 65535:
                raise ValueError
        except ValueError:
            print('Invalid port:', sys.argv[1])
            sys.exit(2)

    #check if fileToServe is valid file
    if len(sys.argv) > 2:
        if os.path.isfile(fileToServe):
            fileToServe = sys.argv[2]
    
    #Start Webserver
    try:
		#Create a web server and define the handler to manage the
		#incoming request
		server = HTTPServer(('', port), myHandler)
		print 'Started httpserver on port ' , port
		
		#Wait forever for incoming http requests
		server.serve_forever()

    except KeyboardInterrupt:
		print '^C received, shutting down the web server'
		server.socket.close()