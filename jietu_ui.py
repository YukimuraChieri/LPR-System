from PyQt5.QtWidgets import QWidget, QApplication, QDesktopWidget   # , QMessageBox
from PyQt5.QtGui import QBitmap, QPainter, QPen, QBrush
from PyQt5.QtCore import Qt, QPoint, QRect
from PyQt5.QtCore import pyqtSignal

import sys
import cv2


class WScreenShot(QWidget):

    CropSignal = pyqtSignal(list)

    def __init__(self):
        QWidget.__init__(self)
        # 自定义信号
        self.frame = []
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setStyleSheet('''background-color:black; ''')
        self.setWindowOpacity(0.6)
        self.desktopRect = QDesktopWidget().screenGeometry()
        self.setGeometry(self.desktopRect)
        self.setCursor(Qt.CrossCursor)
        self.blackMask = QBitmap(self.desktopRect.size())
        self.blackMask.fill(Qt.black)
        self.mask = self.blackMask.copy()
        self.isDrawing = False
        self.startPoint = QPoint()
        self.endPoint = QPoint()

    def paintEvent(self, event):
        if self.isDrawing:
            self.mask = self.blackMask.copy()
            pp = QPainter(self.mask)
            pen = QPen()
            pen.setStyle(Qt.NoPen)
            pp.setPen(pen)
            brush = QBrush(Qt.white)
            pp.setBrush(brush)
            pp.drawRect(QRect(self.startPoint, self.endPoint))
            self.setMask(QBitmap(self.mask))

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.startPoint = event.pos()
            self.endPoint = self.startPoint
            self.isDrawing = True
            self.update()

    def mouseMoveEvent(self, event):
        if self.isDrawing:
            self.endPoint = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.endPoint = event.pos()
            # 通用
            screenshot = QApplication.primaryScreen().grabWindow(QApplication.desktop().winId())
            rect = QRect(self.startPoint, self.endPoint)
            outputRegion = screenshot.copy(rect)
            outputRegion.save('d:/sho54t.jpg', format='JPG', quality=100)
            self.frame = cv2.imread('d:/sho54t.jpg')
            self.close()

    def closeEvent(self, event):

        self.CropSignal.emit(list(self.frame))  # 发射信号

        print("截取图像信号发送完成！")
        event.accept()


if __name__ == '__main__':

    app = QApplication(sys.argv)
    win = WScreenShot()
    win.show()
    sys.exit(app.exec_())

