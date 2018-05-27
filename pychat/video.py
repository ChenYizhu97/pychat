import cv2
from PyQt5.QtWidgets import QWidget, QPushButton, QApplication, QLabel
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage, QPixmap
import sys


class Capture():
    def __init__(self):
        self.capturing = False
        self.c = cv2.VideoCapture(0)

    def startCapture(self):
        print("pressed start")
        self.capturing = True
        cap = self.c
        while self.capturing:
            ret, frame = cap.read()
            cv2.cvtColor(frame, cv2.COLOR_BGR2RGB, frame)
            yield frame
        cv2.destroyAllWindows()
        cap.release()

    def endCapture(self):
        print("pressed End")
        self.capturing = False


class Vwidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(300, 300, 1500, 1500)
        self.sbtn = QPushButton('Start', self)
        self.sbtn.move(0, 0)
        self.ebtn = QPushButton('End', self)
        self.pic = QLabel('pic', self)
        self.pic.setGeometry(100, 100, 500, 500)
        self.pic.show()
        self.ebtn.move(100, 0)
        self.capture = Capture()
        self.frames = self.capture.startCapture()
        frames = self.capture.startCapture()
        frame = next(frames)
        self.sbtn.clicked.connect(self.start)
        self.ebtn.clicked.connect(self.capture.endCapture)
        self.show()

    def start(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.changeImg)
        self.timer.start(20)

    def changeImg(self):
        frame = next(self.frames)
        self.img = QImage(frame[:], frame.shape[1], frame.shape[0], frame.shape[1] * 3, QImage.Format_RGB888)
        self.pic.setPixmap(QPixmap.fromImage(self.img))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    v = Vwidget()
    sys.exit(app.exec_())
