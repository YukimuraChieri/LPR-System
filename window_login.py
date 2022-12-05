# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'login.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QMessageBox, QLineEdit
import qtawesome
import addsql


class Ui_Login(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(561, 424)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(12)
        Dialog.setFont(font)
        self.flag = False
        self.mainWnd = Dialog
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("./bilibili.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.mainWnd.setWindowIcon(icon)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(0, 0, 561, 161))
        self.label.setText("")
        self.label.setObjectName("label")
        self.Login_in = QtWidgets.QPushButton(Dialog)
        self.Login_in.setGeometry(QtCore.QRect(160, 350, 271, 41))
        self.Login_in.setObjectName("Login_in")
        self.Register = QtWidgets.QPushButton(Dialog)
        self.Register.setGeometry(QtCore.QRect(10, 390, 91, 31))
        self.Register.setObjectName("Register")
        self.user = QtWidgets.QLineEdit(Dialog)
        self.user.setGeometry(QtCore.QRect(160, 186, 271, 41))
        self.user.setObjectName("user")
        self.password = QtWidgets.QLineEdit(Dialog)
        self.password.setGeometry(QtCore.QRect(160, 256, 271, 41))
        self.password.setObjectName("password")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(80, 195, 71, 21))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(100, 265, 61, 21))
        self.label_3.setObjectName("label_3")
        self.radioButton = QtWidgets.QRadioButton(Dialog)
        self.radioButton.setGeometry(QtCore.QRect(160, 310, 115, 19))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.radioButton.setFont(font)
        self.radioButton.setObjectName("radioButton")
        self.radioButton_2 = QtWidgets.QRadioButton(Dialog)
        self.radioButton_2.setGeometry(QtCore.QRect(310, 310, 115, 19))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.radioButton_2.setFont(font)
        self.radioButton_2.setObjectName("radioButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(Dialog)
        self.pushButton_3.setGeometry(QtCore.QRect(480, 10, 31, 31))
        self.pushButton_3.setText("")
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtWidgets.QPushButton(Dialog)
        self.pushButton_4.setGeometry(QtCore.QRect(520, 10, 31, 31))
        self.pushButton_4.setText("")
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_5 = QtWidgets.QPushButton(Dialog)
        self.pushButton_5.setGeometry(QtCore.QRect(440, 10, 31, 31))
        self.pushButton_5.setText("")
        self.pushButton_5.setObjectName("pushButton_5")
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(170, 50, 231, 71))
        font = QtGui.QFont()
        font.setPointSize(28)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        self.label.setScaledContents(True)  # 自适应
        self.label.setPixmap(QPixmap(r"./pic/test_2.png"))
        # 打开gif文件
        # movie = QtGui.QMovie("./pic/timg1.gif")
        # # 设置cacheMode为CacheAll时表示gif无限循环，注意此时loopCount()返回-1
        # movie.setCacheMode(QtGui.QMovie.CacheAll)
        # # 播放速度
        # movie.setSpeed(300)
        # # self.movie_screen是在qt designer里定义的一个QLabel对象的对象名，将gif显示在label上
        # self.label.setMovie(movie)
        # # 开始播放，对应的是movie.start()
        # movie.start()

        # self.retranslateUi(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        Dialog.setWindowFlags(QtCore.Qt.FramelessWindowHint)  # 无边框
        Dialog.setWindowOpacity(0.90)  # 设置窗口透明度
        pe = QtGui.QPalette()
        pe.setColor(QtGui.QPalette.Window, QtCore.Qt.darkCyan)  # 设置背景色
        Dialog.setPalette(pe)
        self.Login_in.setText(_translate("Dialog", "登录"))
        self.Register.setText(_translate("Dialog", "注册账号"))
        self.label_2.setText(_translate("Dialog", "用户名 :"))
        self.label_3.setText(_translate("Dialog", "密码 :"))
        self.radioButton.setText(_translate("Dialog", "自动登录"))
        self.radioButton_2.setText(_translate("Dialog", "记住密码"))
        close_icon = qtawesome.icon('fa5s.times', color='white')
        mini_icon = qtawesome.icon('fa5s.window-minimize', color='white')
        set_icon = qtawesome.icon('fa5s.cog', color='white')
        self.pushButton_4.setIcon(close_icon)  # 设置图标
        self.pushButton_3.setIcon(mini_icon)  # 设置图标
        self.pushButton_5.setIcon(set_icon)  # 设置图标
        self.pushButton_4.clicked.connect(self.mainWnd.close)           # 关闭窗口
        self.pushButton_3.clicked.connect(self.mainWnd.showMinimized)   # 最小化窗口
        self.Login_in.clicked.connect(self.fun)
        self.password.setEchoMode(QLineEdit.Password)   # 设置密码隐藏
        self.Register.clicked.connect(self.Register_fun)
        self.Login_in.setStyleSheet('''
                                    QPushButton{
                                    color:white;
                                    border:2px solid #F3F3F5;
                                    border-radius:8px;
                                    background:Gray;
                                    }
                                    QPushButton:hover{
                                    color:blue;
                                    border:1px solid #F3F3F5;
                                    border-radius:8px;
                                    background:darkGray;
                                    }
                                    ''')
        self.Register.setStyleSheet('''
                                    QPushButton{
                                    color:white;
                                    border:none;
                                    }
                                    QPushButton:hover{
                                    color:blue;
                                    border:none;
                                    }
                                    ''')
        self.pushButton_4.setStyleSheet('''
                                        QPushButton{
                                        color:white;
                                        border:none;
                                        }
                                        QPushButton:hover{
                                        color:blue;
                                        border-radius:8px;
                                        background:darkGray;
                                        }
                                        ''')
        self.pushButton_3.setStyleSheet('''
                                        QPushButton{
                                        color:white;
                                        border:none;
                                        }
                                        QPushButton:hover{
                                        color:blue;
                                        border-radius:8px;
                                        background:darkGray;
                                        }
                                        ''')
        self.pushButton_5.setStyleSheet('''
                                        QPushButton{
                                        color:white;
                                        border:none;
                                        }
                                        QPushButton:hover{
                                        color:blue;
                                        border-radius:8px;
                                        background:darkGray;
                                        }
                                        ''')

    def fun(self):
        user_name = self.user.text()
        user_password = self.password.text()
        print("USER:", user_name)
        print("PASSWORD:", user_password)
        db, cursor = addsql.db_open()
        num = addsql.db_search(cursor, user_name, user_password)
        if num == 1:
            self.flag = True
            self.mainWnd.close()
        elif num == 2:
            self.flag = False
            QMessageBox.information(self.mainWnd,  # 使用infomation信息框
                                    "提示",
                                    "密码错误！")
        elif num == 3:
            self.flag = False
            QMessageBox.information(self.mainWnd,  # 使用infomation信息框
                                    "提示",
                                    "用户名不存在")
        print(self.flag)
        addsql.db_close(db)

    def Register_fun(self):
        user_name = self.user.text()
        user_password = self.password.text()
        if user_name == "":
            QMessageBox.information(self.mainWnd,  # 使用infomation信息框
                                    "提示",
                                    "请输入用户名")
            return
        if user_password == "":
            QMessageBox.information(self.mainWnd,  # 使用infomation信息框
                                    "提示",
                                    "请输入密码")
            return
        print("USER:", user_name)
        print("PASSWORD:", user_password)
        db, cursor = addsql.db_open()
        num = addsql.adduser(user_name, user_password, db, cursor)
        addsql.db_close(db)
        if num != 3:
            QMessageBox.information(self.mainWnd,  # 使用infomation信息框
                                    "提示",
                                    "该用户已注册")
        else:
            QMessageBox.information(self.mainWnd,  # 使用infomation信息框
                                    "提示",
                                    "用户注册成功！")


class Move(QtWidgets.QDialog):

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.mainWnd.m_flag = True
            self.mainWnd.m_Position = event.globalPos() - self.mainWnd.pos()  # 获取鼠标相对窗口的位置
            event.accept()
            # self.mainWnd.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))  # 更改鼠标图标

    def mouseMoveEvent(self, QMouseEvent):
        if QtCore.Qt.LeftButton and self.m_flag:
            self.mainWnd.move(QMouseEvent.globalPos() - self.m_Position)  # 更改窗口位置
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.mainWnd.m_flag = False
        self.mainWnd.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))

    # def mousePressEvent(self, e):
    #     if e.button() == QtCore.Qt.LeftButton:
    #         self.m_drag = True
    #         self.m_DragPosition = e.globalPos() - self.pos()
    #         e.accept()
    #         self.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))
    #
    # def mouseReleaseEvent(self, e):
    #     if e.button() == QtCore.Qt.LeftButton:
    #         self.m_drag = False
    #         self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
    #
    # def mouseMoveEvent(self, e):
    #     if QtCore.Qt.LeftButton and self.m_drag:
    #         self.move(e.globalPos() - self.m_DragPosition)
    #         e.accept()

    def back(self):
        self.mainWnd.close()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()  # 创建一个QDialog，用来装载你需要的各种组件、控件
    ui = Ui_Login()  # ui是你创建的ui类的实例化对象
    ui.setupUi(Dialog)  # 执行类中的setupUi方法，方法的参数是第二步中创建的QMainWindow
    Dialog.show()  # 执行QDialog的show()方法，显示这个QMainWindow
    sys.exit(app.exec_())
