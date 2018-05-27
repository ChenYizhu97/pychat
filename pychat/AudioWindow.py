from PyQt5.QtWidgets import QWidget, QGridLayout, QLineEdit, QTextEdit, QPushButton, QApplication, QLabel, QSlider
from PyQt5.QtGui import  QIcon
from PyQt5.QtCore import Qt
import sys


class audioWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setFixedSize(300, 300)
        self.move(300, 300)
        grid = QGridLayout()
        self.setLayout(grid)

        record = QTextEdit("1")
        typein = QLineEdit("2")
        btn_send = QPushButton("send")
        grid.addWidget(record, 0, 0, 4, 4)
        grid.addWidget(typein, 4, 0, 1, 3)
        grid.addWidget(btn_send, 4, 3, 1, 1)
        lab_a = QSlider(Qt.Vertical)
        grid.addWidget(lab_a, 2, 4, 3, 1)

        self.setWindowTitle('Pychat')
        self.setWindowIcon(QIcon('chat.png'))
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    m = audioWindow()
    sys.exit(app.exec_())