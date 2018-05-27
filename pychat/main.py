from gevent import monkey;monkey.patch_all()
from gevent import socket
from SettingWindow import settingWindow
from MsgWindow import msgWindow
from PyQt5.QtWidgets import QApplication
import sys
import gevent
from clientRecord import clientRecord
from VideoWindow import videoWindow
import cv2
import pickle,struct,zlib

def mainloop(app):
    while True:
        app.processEvents()
        while app.hasPendingEvents():
            app.processEvents()
            gevent.sleep(0)
        gevent.sleep(0)

class myServer():
    def __init__(self):
        self.server = False
        # list of object clientRecord
        self.clients = []
        # list of ip: String
        self.remote_ips = []
    def setsocket(self):
        #self.msg_server = StreamServer(self.ip, self.handle_msg)
        #self.msg_server.serve_forever()
        #self.socket.bind()
        print(self.local_ip)
        self.msg_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.msg_server.bind(self.local_ip)
        self.msg_server.listen(5)

        ip, port = self.local_ip

        self.audio_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.audio_server.bind((ip, port + 1))
        self.audio_server.listen(5)

        self.video_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.video_server.bind((ip, port+2))
        self.video_server.listen(5)

        self.server = True
        print('set up succuss -------------')
        #c, addr = self.msg_server.accept()
        gevent.sleep(0)


def serverloop(s: myServer):
    while True:
        if s.server:
            gevent.spawn(msgServerAc, s)
            gevent.spawn(videoServerAc, s)
            break
        gevent.sleep(0)


def msgServerAc(s: myServer):
    while True:
        c, addr = s.msg_server.accept()
        ip, port = addr
        window = msgWindow(c)
        client = clientRecord(ip=ip,msgsocket=c,window=window)
        s.clients.append(client)
        gevent.sleep(0)

def videoServerAc(s: myServer):
    while True:
        rvideosocket, addr = s.video_server.accept()
        ip, port = addr
        for client in s.clients:
            if ip == client.ip:
                break
        client.rvideosocket = rvideosocket
        if client.svideosocket == None:
            svideosocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            local_ip, local_port = s.local_ip
            svideosocket.bind((local_ip, local_port+12))
            svideosocket.connect((ip, port-10))
            client.window.destroy()
            window = videoWindow(videosocket=svideosocket,msgsocket=client.msgsocket)
            client.window = window
            window.sendvideo()
        else:
            print('localsend_________________')
            client.window.sendvideo()
        gevent.sleep(0)


def msghandle(s:myServer):
    while True:
        for client in s.clients:
            a = client.msgsocket.recv(1024)
            client.window.record.append('remote: ' + str(a, encoding='utf-8').strip('\r\n'))
            gevent.sleep(0)
        gevent.sleep(0)

def videohandle(s:myServer):
    while True:
        for client in s.clients:
            print('bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb')
            if client.rvideosocket == None:
                gevent.sleep(0)
                continue
            size = client.rvideosocket.recv(struct.calcsize('L'))
            size, *_ = struct.unpack('L', size)
            print('r'+str(size))
            # recieve frame
            frame = b''
            while len(frame)!= size:
                while len(frame) + 200000   < size:
                    a = client.rvideosocket.recv(200000)
                    frame += a
                frame += client.rvideosocket.recv(size - len(frame))
            print('a'+str(len(frame)))
            # unserialize frame
            frame = zlib.decompress(frame, zlib.MAX_WBITS)
            frame = pickle.loads(frame)
            print('startreloadv1')
            client.window.reloadv1(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB, frame))
            print('endreloadv1')
            print(frame)
            gevent.sleep(0)
        gevent.sleep(0)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    server = myServer()
    s = settingWindow(server)

    gevent.joinall([
        gevent.spawn(videohandle, server),
        gevent.spawn(msghandle, server),
        gevent.spawn(mainloop, app),
        gevent.spawn(serverloop, server)
    ])
