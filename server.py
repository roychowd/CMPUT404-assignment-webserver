#  coding: utf-8 
import socketserver
import os
from pathlib import Path
# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


HOSTDOMAIN = "http://127.0.0.1:8080"


class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        # print ("Got a request of: %s\n" % self.data)
        # self.request.sendall(bytearray("OK",'utf-8'))
        # split at r and get the first request header
        #req of the form [OPERATION , "/" , HTTP/1,1]
        req = self.data.decode()
        # check if the POST is a GET if not raise 405 
        if ("GET" not in req):
            content = "HTTP/1.1 405 Not FOUND! \nContent-Type: text/html\n\n"
            self.request.sendall(content.encode()) 
        # Splitt in the \r 
        newreq = req.split('\r')[0].split()
        # utilized the Pathlib library found here https://docs.python.org/3/library/pathlib.html
        filepath  = str(Path("www").absolute())+newreq[1]
        isValid = False
        # if the path is a file 
        if (Path(filepath).is_file()): # file exists  
            #if css send 200 with content being the css file 
            if ("css" in newreq[1]):
                content = "HTTP/1.1 200 OK!\r\nContent-Type: text/css\r\n"
                isValid = True # set is valid true for the /.../.../ test case
            # if html sent 200 with content being the html file
            elif ("html" in newreq[1]):
                content = "HTTP/1.1 200 OK!\r\nContent-Type: text/html\r\n"
                isValid = True
            if (isValid == True):
                lengthofContent = open(filepath).read() # open the file and read it
                content += "Content-Length: " + str(len(lengthofContent)) + "\r\n\n" #append content legnth of the file in header of http
                content += open(filepath).read() # open the file and read it and addpend to content
                self.request.sendall(content.encode()) # send to server
                isValid = False # set is valid to false for next request 
            else:
                self.send404()
        elif (Path(filepath).is_dir()):
            # check if deep and the path does not end with "/"
            if ("deep" in newreq[1] and not newreq[1].endswith("/") ):
                filepath += "/" # append backslash ot url and send 301 
                content = "HTTP/1.1 301 Moved Permanently\r\nLocation: " +HOSTDOMAIN + newreq[1] + "/" + "\r\n\r\n"
                self.request.sendall(content.encode())
            newfilepath = filepath + "index.html"
            content = "HTTP/1.1 200 OK!\r\nContent-Type: text/html\r\n"
            lengthofContent = open(newfilepath).read()
            content += "Content-Length: " + str(len(lengthofContent)) + "\r\n\n"
            content +=  open(newfilepath).read()
            self.request.sendall(content.encode())
        else:
            self.send404()


    def send404(self):
        content = "HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\n\r\n" + """<html><body>404 Error Not Found</body></html>"""
        # print(content)
        self.request.sendall(content.encode())




        

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()





