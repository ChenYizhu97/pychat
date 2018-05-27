# -*- coding: utf-8 -*-

"""The user interface for our app"""
from gevent import monkey; monkey.patch_all()
import os, sys
import gevent
from gevent import select
from gevent.server import StreamServer
import socket

# Import Qt modules
from PyQt5 import QtCore, QtWidgets

# Import the compiled UI module
from main import chatWindow


# Create a class for our main window
def raw_input():
    """ Non-blocking input from stdin. """

    select.select([sys.stdin], [], [])
    return sys.stdin.readline()


def mainloop(app):
    while True:
        app.processEvents()
        while app.hasPendingEvents():
            app.processEvents()
            gevent.sleep()
        gevent.sleep()  # don't appear to get here but cooperate again


def testprint():
    print('this is running')
    gevent.spawn_later(1, testprint)

def _send(s: socket.socket):
    """ No-blocking sending of msg """
    while True:
        gevent.sleep(1)
        a = raw_input()
        s.send(bytes(a, encoding='utf-8'))


def handle(s: socket.socket, addr):
    print('connect from %s %d' % addr)
    app = QtWidgets.QApplication(sys.argv)
    window = chatWindow()
    s.send(b"hello\n")
    gevent.joinall([
        gevent.spawn(_send, s),
        gevent.spawn(mainloop, app)
    ])


if __name__ == "__main__":
    server = StreamServer(('127.0.0.1', 8888), handle)
    server.serve_forever()