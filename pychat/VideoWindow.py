from gevent import monkey; monkey.patch_all()
from PyQt5.QtWidgets import QWidget, QGridLayout, QLineEdit, QTextEdit, QPushButton, QApplication, QLabel, QSlider
from PyQt5.QtGui import QImage, QPixmap, QIcon
from PyQt5.QtCore import Qt
import gevent
from gevent import socket
import sys
import cv2
import pickle,zlib,struct

class videoWindow(QWidget):
    def __init__(self, videosocket:socket.socket = None, msgsocket:socket.socket=None):
        super().__init__()
        self.videosocket = videosocket
        self.msgsocket = msgsocket
        self.initUI()
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 180)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 240)

    def destroy(self, destroyWindow=True, destroySubWindows=True):
        self.cap.release()
        super().destroy()

    def initUI(self):
        self.setFixedSize(540, 300)
        self.move(300, 300)
        grid = QGridLayout()
        self.setLayout(grid)
        record = QTextEdit()
        typein = QLineEdit()
        btn_send = QPushButton("send")
        grid.addWidget(record, 0, 0, 4, 3)
        grid.addWidget(typein, 4, 0, 1, 2)
        grid.addWidget(btn_send, 4, 2, 1, 1)

        lab_v1 = QLabel()
        lab_v1.setFixedSize(240, 180)
        self.v1 = lab_v1
        lab_v2 = QLabel()
        lab_v2.setFixedSize(120, 120)
        self.v2 = lab_v2
        lab_a = QSlider(Qt.Vertical)

        grid.addWidget(lab_v1, 0, 3, 3, 4)
        grid.addWidget(lab_v2, 3, 3, 2, 2)
        grid.addWidget(lab_a, 3, 5, 2, 1)
        self.record = record
        self.typein = typein

        btn_send.clicked.connect(self.sendmsg)
        self.setWindowTitle('Pychat')
        self.setWindowIcon(QIcon('chat.png'))
        self.show()

    def sendmsg(self):
        gevent.sleep(0)
        msg = self.typein.text()
        if msg != '':
            self.msgsocket.sendall(bytes(msg, encoding='utf-8'))
            self.typein.setText('')
            self.record.append('local: ' + msg)
        gevent.sleep(0)

    def reloadv1(self, frame):
        self.v1.setPixmap(QPixmap.fromImage(QImage(frame[:], frame.shape[1], frame.shape[0], frame.shape[1] * 3, QImage.Format_RGB888)))
        gevent.sleep(0)
        print('loadv1==============')

    def reloadv2(self, frame):
        self.v2.setPixmap(QPixmap.fromImage(QImage(frame[:], frame.shape[1], frame.shape[0], frame.shape[1] * 3, QImage.Format_RGB888)))
        print('loadv200000000000000')

    def sendvideo(self):
        while True:
            res, frame = self.cap.read()
            if not res:
                return "Video Capture fail"
            # serialize frame
            frame1 = pickle.dumps(frame)
            frame1 = zlib.compress(frame1, zlib.Z_BEST_COMPRESSION)
            # serialize frame length, and ensure bytes size of frame length is a const ('L' represent 'Long Int').
            size = len(frame1)
            print('s'+str(size))
            size = struct.pack('L', size)
            # sendall data
            print('startsvideosocketsendall')
            print(self.videosocket)
            t = self.videosocket.sendall(size + frame1)
            print(t)
            print('endsvideosocketsendall')
            cv2.resize(frame, (120, 120), interpolation=cv2.INTER_CUBIC)
            self.reloadv2(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB, frame))
            print('endreloadv2')
            gevent.sleep(0)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    m = videoWindow()
    sys.exit(app.exec_())
