# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Loading(object):
    def setupUi(self, Loading):
        Loading.setObjectName("Loading")
        Loading.resize(400, 160)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(12)
        Loading.setFont(font)
        self.loadWnd = Loading
        self.progressBar = QtWidgets.QProgressBar(Loading)
        self.progressBar.setGeometry(QtCore.QRect(40, 95, 351, 21))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.label = QtWidgets.QLabel(Loading)
        self.label.setGeometry(QtCore.QRect(40, 30, 231, 41))
        self.label.setObjectName("label")

        self.retranslateUi(Loading)
        QtCore.QMetaObject.connectSlotsByName(Loading)

    def retranslateUi(self, Loading):
        _translate = QtCore.QCoreApplication.translate
        Loading.setWindowTitle(_translate("Loading", "Dialog"))
        self.label.setText(_translate("Loading", "图像处理中，请稍等..."))
        Loading.setWindowFlags(QtCore.Qt.FramelessWindowHint)  # 无边框
        Loading.setWindowOpacity(0.9)  # 设置窗口透明度
        pe = QtGui.QPalette()
        pe.setColor(QtGui.QPalette.Window, QtCore.Qt.darkCyan)  # 设置背景色
        Loading.setPalette(pe)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    LoadWindow = QtWidgets.QDialog()  # 创建一个QMainWindow，用来装载你需要的各种组件、控件
    ui = Ui_Loading()    # ui是你创建的ui类的实例化对象

    ui.setupUi(LoadWindow)  # 执行类中的setupUi方法，方法的参数是第二步中创建的QMainWindow
    LoadWindow.show()       # 执行QMainWindow的show()方法，显示这个QMainWindow
    sys.exit(app.exec_())
