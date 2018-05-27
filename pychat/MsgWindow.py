from gevent import monkey;monkey.patch_all();
from PyQt5.QtWidgets import QWidget, QGridLayout, QLineEdit, QTextEdit, QPushButton, QApplication
from PyQt5.QtGui import QIcon
import sys
from gevent import socket
import gevent

class msgWindow(QWidget):
    def __init__(self, msgsocket:socket.socket):
        super().__init__()
        self.msgsocket = msgsocket
        self.initUI()

    def initUI(self):
        self.setFixedSize(240, 300)
        self.move(300, 300)
        grid = QGridLayout()
        self.setLayout(grid)

        record = QTextEdit()
        typein = QLineEdit()
        btn_send = QPushButton("send")
        grid.addWidget(record, 0, 0, 4, 4)
        grid.addWidget(typein, 4, 0, 1, 3)
        grid.addWidget(btn_send, 4, 3, 1, 1)
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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    m = msgWindow()
    sys.exit(app.exec_())