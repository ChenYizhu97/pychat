from PyQt5.QtWidgets import QWidget, QGridLayout, QLineEdit, QSpacerItem, QPushButton, QApplication, QLabel
from PyQt5.QtGui import QIcon
import sys
from MainWindow import mainWindow
import gevent


class settingWindow(QWidget):
    def __init__(self, server):
        super().__init__()
        self.initUI()
        self.server = server

    def initUI(self):
        grid = QGridLayout()
        self.setLayout(grid)
        self.setFixedSize(240, 300)
        self.move(300, 300)
        self.setWindowTitle('Pychat')
        self.setWindowIcon(QIcon('chat.png'))

        btn_go = QPushButton('Go')
        lab_ip = QLineEdit('0.0.0.0')
        lab_port = QLineEdit('9000')
        lab1 = QLabel('IP addr:')
        lab2 = QLabel('port:')
        grid.addItem(QSpacerItem(200, 85), 0, 0, 1, 20)
        grid.addWidget(QLabel('Set  your  ip address and  port：'), 1, 1, 1, 18)
        grid.addItem(QSpacerItem(200, 15), 2, 0, 1, 20)
        grid.addWidget(lab1, 3, 1)
        grid.addWidget(lab_ip, 3, 2, 1, 18)
        grid.addItem(QSpacerItem(200, 10), 4, 0, 1, 20)
        grid.addWidget(lab2, 5, 1)
        grid.addWidget(lab_port, 5, 2, 1, 18)
        grid.addItem(QSpacerItem(200, 20), 6, 1, 1, 20)
        grid.addWidget(btn_go, 7, 1, 1, 19)
        grid.addItem(QSpacerItem(200, 10), 8, 0, 1, 20)
        grid.addWidget(QLabel('---------------------------------------------'), 9, 1, 1, 20)
        grid.addWidget(QLabel('Dev by cyz @ XJTU'), 10, 1, 1, 20)

        btn_go.clicked.connect(self.getlocal)

        self.lab_ip = lab_ip
        self.lab_port = lab_port

        self.show()

    def getlocal(self):
        self.server.local_ip = (self.lab_ip.text(), int(self.lab_port.text()))
        self.server.mWindow = mainWindow(self.server)
        self.server.setsocket()
        self.destroy()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    m = settingWindow()
    sys.exit(app.exec_())
