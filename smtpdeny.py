#! /usr/bin/env python
import SocketServer, subprocess, sys
from threading import Thread

HOSTNAME = 'smtpdeny.voinetworks.net'
HOST = 'localhost'
PORT = 2500

class SingleTCPHandler(SocketServer.BaseRequestHandler):
    "One instance per connection.  Override handle(self) to customize action."
    def handle(self):
        # self.request is the client connection
        reply = "220 " + HOSTNAME + " ESMTP\n"
        self.request.send(reply)
        data = self.request.recv(1024)  # clip input at 1Kb
        reply = "550 5.7.1 SMTP restricted.\nIf you feel this is in error please open a ticket at http://support.voinetworks.net/\n"
        self.request.send(reply)
        self.request.close()

class SimpleServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    # Ctrl-C will cleanly kill all spawned threads
    daemon_threads = True
    # much faster rebinding
    allow_reuse_address = True

    def __init__(self, server_address, RequestHandlerClass):
        SocketServer.TCPServer.__init__(self, server_address, RequestHandlerClass)

if __name__ == "__main__":
    server = SimpleServer((HOST, PORT), SingleTCPHandler)
    # terminate with Ctrl-C
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        sys.exit(0)
