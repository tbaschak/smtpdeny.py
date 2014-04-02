#! /usr/bin/env python
import SocketServer, subprocess, sys
from threading import Thread
import logging

HOSTNAME = 'smtpdeny.voinetworks.net'
HOST = '127.0.0.1'
PORT = 2500

class SingleTCPHandler(SocketServer.BaseRequestHandler):
    def setup(self):
        logger.info(str(self.client_address[0]) + ' connected')

    "One instance per connection.  Override handle(self) to customize action."
    def handle(self):
        # self.request is the client connection
        self.request.send("220 " + HOSTNAME + " ESMTP\n")
        data = self.request.recv(1024)  # clip input at 1Kb
        reply = "550 5.7.1 SMTP restricted.\n\nIf you feel this is in error,\nplease open a ticket at http://support.voinetworks.net/\nwith the following details\n\nSubject: SMTP restrictions on IP " + str(self.client_address[0]) + "\n" + "-"*60 + "\nTicket Body:\nAddress: " + str(self.client_address[0]) + "\nCustomer Name: \nCustomer Location: \nReverse DNS Needed: yes/no\n\n"
        self.request.send(reply)
        self.request.close()
        logger.info(str(self.client_address[0]) + ' denied')

class SimpleServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    # Ctrl-C will cleanly kill all spawned threads
    daemon_threads = True
    # much faster rebinding
    allow_reuse_address = True

    def __init__(self, server_address, RequestHandlerClass):
        SocketServer.TCPServer.__init__(self, server_address, RequestHandlerClass)

if __name__ == "__main__":
    logger = logging.getLogger('smtpdeny')
    logger.setLevel(logging.INFO)
    hdlr = logging.FileHandler('/var/log/smtpdeny')
    formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)

    server = SimpleServer((HOST, PORT), SingleTCPHandler)
    # terminate with Ctrl-C
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        sys.exit(0)
