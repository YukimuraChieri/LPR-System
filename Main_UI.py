from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QSplashScreen, QWidget
from PyQt5.QtGui import QPixmap, QImage
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal, QUrl
from PyQt5 import QtMultimedia
import numpy as np
import sys

app = QApplication(sys.argv)
splash = QSplashScreen(QPixmap(r".\pic\start_1.png"))
splash.showMessage("程序启动中请稍等...\n", QtCore.Qt.AlignHCenter | QtCore.Qt.AlignBottom, QtCore.Qt.black)
splash.show()  # 显示启动界面

from Window_main import *
from window_tupianxianshi import *
from window_login import *
from jietu_ui import *
from window_search import *
from window_loading import *


class LoginWindow(QDialog):

    # 自定义信号
    mySignal = pyqtSignal(bool)

    def __init__(self):
        QDialog.__init__(self)
        self.login = QDialog()
        self.login = Move()
        self.login_ui = Ui_Login()
        self.login_ui.setupUi(self.login)

    def sendContent(self):
        print("send ok!")
        self.mySignal.emit(self.login_ui.flag)  # 发射信号

    def getSignal(self, connect):

        if connect:
            self.login_ui.mainWnd.close()


class parentWindow(QMainWindow):

    # 自定义信号
    mySignal = pyqtSignal(list)
    log = LoginWindow()

    def __init__(self):
        QMainWindow.__init__(self)
        self.MainWindow = QMainWindow()
        self.MainWindow = Myset()
        self.main_ui = Ui_MainWindow()
        self.main_ui.setupUi(self.MainWindow)

    def sendContent(self):
        print("send ok!")
        print("self.main_ui.images_1::::::::", len(self.main_ui.images_1))
        self.mySignal.emit(self.main_ui.images_1)  # 发射信号
        self.main_ui.images_1.clear()

    def getSignal(self, connect):

        if connect:
            # player.stop()
            self.log.login_ui.mainWnd.close()
            self.MainWindow.show()
        else:
            print("登录失败")

    def getSignal_1(self, connect):
        print("show_1")
        self.main_ui.label_2.setScaledContents(False)  # 自适应
        self.main_ui.label_2.setAlignment(QtCore.Qt.AlignCenter)
        img = np.array(connect)
        img = QImage(img.data, img.shape[1], img.shape[0], QImage.Format_RGB888)
        self.main_ui.label_2.setPixmap(QPixmap.fromImage(img))
        self.main_ui.graphicsView.setStyleSheet("border-image: url(./pic/black.jpg);")

    def getSignal_2(self, connect):
        print("show_2")
        self.main_ui.listModel.setStringList([])
        self.main_ui.listView.setModel(self.main_ui.listModel)
        self.main_ui.layout.addWidget(self.main_ui.listView)
        self.main_ui.listModel.setStringList(connect)
        self.main_ui.listView.setModel(self.main_ui.listModel)
        self.main_ui.layout.addWidget(self.main_ui.listView)

    def getSignal_3(self, connect):
        print("show_3")
        self.main_ui.img_crop = connect


class childWindow(QDialog):

    imgs = []

    def __init__(self):
        QDialog.__init__(self)
        self.display = QDialog()
        self.child = Ui_Dialog()

    def getSignal(self, connect):
        print("picture show_1!!!!!!!")
        if len(connect) != 0:
            self.imgs = connect
            self.child.setupUi(self, self.imgs)
            print("picture show!!!!!!!")
            self.child.mainWnd.show()

    def closeEvent(self, event):
        """
            重写closeEvent方法，实现MainWindow窗体关闭时执行一些代码
            :param event: close()触发的事件
            :return: None
        """
        self.child.label.clear()
        self.child.label_2.clear()
        self.child.images = []
        event.accept()


class childWindow_1(QWidget):

    # 自定义信号
    mySignal = pyqtSignal(list)
    mySignal_1 = pyqtSignal(list)
    mySignal_2 = pyqtSignal(list)

    def __init__(self):
        QWidget.__init__(self)
        self.jt = WScreenShot()


class childWindow_2(QDialog):
    # 自定义信号
    mySignal = pyqtSignal(list)

    def __init__(self):
        QDialog.__init__(self)

        self.mode = QDialog()
        self.mode = Move()
        self.mode_ui = Ui_Search()
        self.mode_ui.setupUi(self.mode)

    def sendContent(self):
        print("send ok!")
        self.mySignal.emit(self.mode_ui.images)  # 发射信号
        self.mode_ui.images.clear()


class childWindow_3(QDialog):
    load_flag = True

    def __init__(self):
        QDialog.__init__(self)
        self.load = QDialog()
        self.load_ui = Ui_Loading()
        self.load_ui.setupUi(self.load)

    def getSignal(self, connect):
        print("Receive Loading Signal:::::::::::::::", connect)
        self.load_ui.progressBar.setValue(connect)
        if self.load_flag:
            print("loading window show")
            self.load_flag = False
            self.load_ui.loadWnd.show()
        if connect >= 100:
            self.load_ui.loadWnd.close()
            self.load_flag = True


class Move(QDialog):

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.m_flag = True
            self.m_Position = event.globalPos() - self.pos()  # 获取鼠标相对窗口的位置
            event.accept()
            self.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))  # 更改鼠标图标

    def mouseMoveEvent(self, QMouseEvent):
        if QtCore.Qt.LeftButton and self.m_flag:
            self.move(QMouseEvent.globalPos() - self.m_Position)  # 更改窗口位置
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        if QtCore.Qt.LeftButton and self.m_flag:
            self.m_flag = False
            self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))


if __name__ == "__main__":

    logwin = LoginWindow()
    window = parentWindow()
    child = childWindow()
    child_1 = childWindow_1()
    child_2 = childWindow_2()
    child_3 = childWindow_3()
    music_path = r".\music\Keil Generic Keygen-EDGE.mp3"
    url = QUrl.fromLocalFile(music_path)
    content = QtMultimedia.QMediaContent(url)
    player = QtMultimedia.QMediaPlayer()
    player.setMedia(content)

    window.main_ui.workThread.load_flag = True
    window.main_ui.workThread.run()

    # 隐藏启动界面
    splash.finish(window.MainWindow)
    # 显示
    logwin.login.show()
    # player.play()

    # 通过Login_in将登录窗体与主窗体关联
    btn_1 = logwin.login_ui.Login_in
    btn_1.clicked.connect(logwin.sendContent)
    logwin.mySignal.connect(window.getSignal)

    # 通过pushButton_piliang将主窗体与子窗体关联
    btn_2 = window.main_ui.pushButton_piliang

    # 在子窗口中连接信号和槽
    window.main_ui.workThread.LoadingSignal.connect(child_3.getSignal)
    window.main_ui.workThread.ImagesSignal.connect(child.getSignal)

    btn_3 = window.main_ui.pushButton_jietu
    btn_3.clicked.connect(window.MainWindow.hide)
    btn_3.clicked.connect(child_1.jt.show)
    child_1.jt.CropSignal.connect(window.MainWindow.show)
    child_1.jt.CropSignal.connect(window.main_ui.getSignal_2)

    btn_4 = window.main_ui.pushButton_switch
    btn_4.clicked.connect(child_2.mode.show)

    # child_2.mode_ui.FileSignal.connect(window.main_ui.getSignal_4)
    btn_5 = child_2.mode_ui.pushButton_4
    btn_5.clicked.connect(child_2.sendContent)

    # 在子窗口中连接信号和槽
    child_2.mySignal.connect(child.getSignal)

    btn6 = window.main_ui.pushButton_exit
    btn6.clicked.connect(window.MainWindow.hide)
    btn6.clicked.connect(logwin.login.show)
    # btn6.clicked.connect(player.play)
    btn7 = window.main_ui.pushButton_close
    sys.exit(app.exec_())
