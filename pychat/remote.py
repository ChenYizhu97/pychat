from gevent import monkey; monkey.patch_all()
import gevent, sys
import socket
from gevent.server import StreamServer
from gevent import select
import cv2
import pickle
import zlib
import struct


def _read(s: socket.socket):
    """ Non-blocking reciving and showing of Video frame """

    while True:
        # unserialize length of frame
        size = s.recv(struct.calcsize('L'))
        size, *_ = struct.unpack('L', size)

        # recieve frame
        frame = b''
        while len(frame) + 16384 < size:
            a = s.recv(16384)
            frame += a
            print(len(frame))
        frame += s.recv(size - len(frame))

        # unserialize frame
        frame = zlib.decompress(frame, zlib.MAX_WBITS)
        frame = pickle.loads(frame)

        # show frame
        cv2.imshow("capture", frame)
        cv2.waitKey(1)
        gevent.sleep(0)


def raw_input():
    """ Non-blocking input from stdin. """

    select.select([sys.stdin], [], [])
    return sys.stdin.readline()


def _send(s: socket.socket):
    """ No-blocking sending of msg """
    while True:
        gevent.sleep(1)
        a = raw_input()
        s.send(bytes(a, encoding='utf-8'))


def handle(s: socket.socket, addr):
    print('connect from %s %d' % addr)
    s.send(b"hello\n")
    gevent.joinall([
        gevent.spawn(_read, s),
        gevent.spawn(_send, s)
    ])


server = StreamServer(('127.0.0.1', 8888), handle)
server.serve_forever()
