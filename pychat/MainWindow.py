from gevent import monkey;monkey.patch_all()
from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QApplication, QSpacerItem, QInputDialog, QLineEdit
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize
from MsgWindow import msgWindow
from clientRecord import clientRecord
from VideoWindow import videoWindow
import gevent
import sys
from gevent import socket

class mainWindow(QWidget):
    def __init__(self,s):
        super().__init__()
        self.initUI()
        self.server = s
    def initUI(self):
        grid = QGridLayout()
        self.setLayout(grid)
        self.setFixedSize(150, 300)
        self.move(300, 300)

        lab_p1 = QPushButton()
        lab_p2 = QPushButton()
        lab_p3 = QPushButton()
        lab_p1.setIcon(QIcon('msg2.png'))
        lab_p1.setIconSize(QSize(64, 64))
        lab_p2.setIcon(QIcon('video1.png'))
        lab_p2.setIconSize(QSize(64, 64))
        lab_p3.setIcon(QIcon('audio2.png'))
        lab_p3.setIconSize(QSize(64, 64))
        grid.addItem(QSpacerItem(150, 10), 0, 0, 1, 15)
        grid.addWidget(lab_p1, 0, 1, 1, 13)
        grid.addWidget(lab_p2, 1, 1, 1, 13)
        grid.addWidget(lab_p3, 2, 1, 1, 13)

        lab_p1.clicked.connect(self.startmsg)
        lab_p2.clicked.connect(self.startvideo)
        lab_p3.clicked.connect(self.startmsg)

        self.setWindowTitle('Pychat')
        self.setWindowIcon(QIcon('chat.png'))
        self.show()

    def startvideo(self):
        value, ok = QInputDialog.getText(self, 'Please input ip and port', '')
        ip, port = value.strip('\n').split(':')
        port = int(port)
        local_ip, port = self.server.local_ip
        msgsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        msgsocket.bind((local_ip, port+10))
        msgsocket.connect((ip, port))
        gevent.sleep(2)
        videosocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        videosocket.bind((local_ip, port+12))
        videosocket.connect((ip, port+2))
        window = videoWindow(msgsocket=msgsocket, videosocket=videosocket)
        client = clientRecord(ip=ip, window=window, msgsocket=msgsocket, svideosocket=videosocket)
        print(client.ip)
        self.server.clients.append(client)
        client.window.record.append('----------')

    def startmsg(self):
        value, ok = QInputDialog.getText(self, 'Please input ip and port', '192.168.12.204:9000')
        ip, port = value.strip('\n').split(':')
        port = int(port)
        local_ip, port = self.server.local_ip
        msgsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        msgsocket.bind((local_ip, port + 10))
        msgsocket.connect((ip, port))
        type = 0
        window = msgWindow(msgsocket=msgsocket)
        client = clientRecord(ip=ip, window_type=type, window=window, msgsocket=msgsocket)
        self.server.clients.append(client)
        print(client.ip)
        client.window.record.append('----------')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    m = mainWindow()
    sys.exit(app.exec_())