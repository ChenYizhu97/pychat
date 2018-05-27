from gevent import monkey; monkey.patch_all()
import gevent, sys
from gevent import select
import socket
import cv2
import pickle
import zlib
import struct


def _read(s: socket.socket):
    """ Non-blocking output of message from net """

    while True:
        a = s.recv(1024)
        print(str(a, encoding='utf-8').strip('\n'))
        gevent.sleep(1)


def raw_input():
    """ Non-blocking input from stdin. """

    select.select([sys.stdin], [], [])
    return sys.stdin.readline()


def _send(s: socket.socket):
    """ Non-blocking sending of Video frame """

    while True:
        res, frame = cap.read()
        if not res:
            return "Video Capture fail"
        # serialize frame
        frame1 = pickle.dumps(frame)
        frame1 = zlib.compress(frame1, zlib.Z_BEST_COMPRESSION)
        # serialize frame length, and ensure bytes size of frame length is a const ('L' represent 'Long Int').
        size = len(frame1)
        size = struct.pack('L', size)
        # sendall data
        s.sendall(size + frame1)
        gevent.sleep(0)

local_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
local_socket.connect(('127.0.0.1', 8888))
cap = cv2.VideoCapture(0)

gevent.joinall([
    gevent.spawn(_read, local_socket),
    gevent.spawn(_send, local_socket)
])


