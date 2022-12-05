# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tupianxianshi.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QFileDialog
import qtawesome
import cv2


class Ui_Dialog(object):

    images = []

    def setupUi(self, Dialog, pic_data):
        Dialog.setObjectName("Dialog")
        Dialog.setWindowModality(QtCore.Qt.NonModal)
        Dialog.resize(702, 576)
        Dialog.setFixedSize(Dialog.width(), Dialog.height())  # 固定窗口大小
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        Dialog.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("./pic/bilibili.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)
        self.images = pic_data
        self.mainWnd = Dialog
        self.index = 1
        self.img_len = len(pic_data)
        self.centralwidget = QtWidgets.QWidget(Dialog)
        self.centralwidget.setObjectName("centralwidget")
        self.graphicsView = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView.setGeometry(QtCore.QRect(10, 10, 681, 461))
        self.graphicsView.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.graphicsView.setObjectName("graphicsView")
        self.pushButton_back = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_back.setGeometry(QtCore.QRect(442, 510, 111, 41))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        self.pushButton_back.setFont(font)
        self.pushButton_back.setObjectName("pushButton_back")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 10, 681, 461))
        self.label.setText("")
        self.label.setObjectName("label")
        self.pushButton_save = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_save.setGeometry(QtCore.QRect(150, 510, 111, 41))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        self.pushButton_save.setFont(font)
        self.pushButton_save.setObjectName("pushButton_save")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(320, 480, 61, 21))
        self.label_2.setText("")
        self.label_2.setObjectName("label_2")
        self.pushButton_left = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_left.setGeometry(QtCore.QRect(10, 10, 101, 461))
        self.pushButton_left.setText("")
        self.pushButton_left.setObjectName("pushButton_left")
        self.pushButton_right = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_right.setGeometry(QtCore.QRect(592, 10, 101, 461))
        self.pushButton_right.setText("")
        self.pushButton_right.setObjectName("pushButton_right")
        self.statusbar = QtWidgets.QStatusBar(Dialog)
        self.statusbar.setObjectName("statusbar")

        # self.label.setScaledContents(True)  # 自适应
        image = QImage(self.images[0].data, self.images[0].shape[1], self.images[0].shape[0], QImage.Format_RGB888)
        self.label.setPixmap(QPixmap.fromImage(image))
        self.label_2.setText("1/" + str(self.img_len))

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "图片显示"))
        self.pushButton_left.clicked.connect(self.turn_left)
        self.pushButton_right.clicked.connect(self.turn_right)
        self.pushButton_back.setText(_translate("Dialog", "返回"))
        self.pushButton_back.clicked.connect(self.back)
        self.pushButton_save.setText(_translate("Dialog", "保存"))
        self.pushButton_save.clicked.connect(self.save)
        op = QtWidgets.QGraphicsOpacityEffect()
        op_1 = QtWidgets.QGraphicsOpacityEffect()
        # 设置透明度的值
        op.setOpacity(0.6)
        op_1.setOpacity(0.6)
        self.pushButton_left.setGraphicsEffect(op)
        self.pushButton_right.setGraphicsEffect(op_1)
        left_icon = qtawesome.icon('fa5s.chevron-left', color='black')
        right_icon = qtawesome.icon('fa5s.chevron-right', color='black')
        save_icon = qtawesome.icon('fa5s.save', color='white')
        back_icon = qtawesome.icon('fa5s.home', color='white')
        self.pushButton_left.setIcon(left_icon)  # 设置图标
        self.pushButton_right.setIcon(right_icon)  # 设置图标
        self.pushButton_save.setIcon(save_icon)  # 设置图标
        self.pushButton_back.setIcon(back_icon)  # 设置图标
        self.pushButton_left.setIconSize(QtCore.QSize(40, 40))
        self.pushButton_right.setIconSize(QtCore.QSize(40, 40))
        self.pushButton_save.setIconSize(QtCore.QSize(35, 35))
        self.pushButton_back.setIconSize(QtCore.QSize(35, 35))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        Dialog.setWindowOpacity(0.95)  # 设置窗口透明度
        pe = QtGui.QPalette()
        pe.setColor(QtGui.QPalette.Window, QtCore.Qt.darkCyan)  # 设置背景色
        Dialog.setPalette(pe)
        self.pushButton_left.setStyleSheet('''
                                                        QPushButton{
                                                        border:none;
                                                        }
                                                        QPushButton:hover{
                                                        background:lightGray;
                                                        }
                                                        ''')
        self.pushButton_right.setStyleSheet('''
                                                        QPushButton{
                                                        border:none;
                                                        }
                                                        QPushButton:hover{
                                                        background:lightGray;
                                                        }
                                                        ''')
        self.pushButton_save.setStyleSheet('''
                                                    QPushButton{
                                                    color:white;
                                                    border:2px solid #F3F3F5;
                                                    border-radius:8px;
                                                    background:Gray;
                                                    }
                                                    QPushButton:hover{
                                                     color:blue;
                                                    border:2px solid #F3F3F5;
                                                    border-radius:8px;
                                                    background:darkGray;
                                                    }
                                                    ''')
        self.pushButton_back.setStyleSheet('''
                                                    QPushButton{
                                                    color:white;
                                                    border:2px solid #F3F3F5;
                                                    border-radius:8px;
                                                    background:Gray;
                                                    }
                                                    QPushButton:hover{
                                                     color:blue;
                                                    border:2px solid #F3F3F5;
                                                    border-radius:8px;
                                                    background:darkGray;
                                                    }
                                                    ''')

    def turn_left(self):
        if self.index > 1:
            self.index -= 1
        image = self.images[self.index - 1]
        image = QImage(image.data, image.shape[1], image.shape[0], QImage.Format_RGB888)
        self.label.setPixmap(QPixmap.fromImage(image))
        self.label_2.setText(str(self.index)+"/"+str(self.img_len))

    def turn_right(self):
        if self.index < self.img_len:
            self.index += 1
        image = self.images[self.index - 1]
        image = QImage(image.data, image.shape[1], image.shape[0], QImage.Format_RGB888)
        self.label.setPixmap(QPixmap.fromImage(image))
        self.label_2.setText(str(self.index)+"/"+str(self.img_len))

    def back(self):
        self.mainWnd.close()

    def save(self):
        filename = QFileDialog.getSaveFileName(self.mainWnd, '另存为', '', '*.jpg')
        if len(filename[0]) != 0:
            my_pic = self.images[self.index-1]
            my_pic = cv2.cvtColor(my_pic, cv2.COLOR_BGR2RGB)
            cv2.imwrite(filename[0], my_pic)
            print("save ok")
        else:
            print("save error")


def ui_display(images):
    import sys
    app = QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()  # 创建一个QDialog，用来装载你需要的各种组件、控件
    ui = Ui_Dialog()  # ui是你创建的ui类的实例化对象
    ui.setupUi(Dialog, images)  # 执行类中的setupUi方法，方法的参数是第二步中创建的QDialog
    Dialog.show()  # 执行QDialog的show()方法，显示这个QDialog
    sys.exit(app.exec_())


if __name__ == "__main__":
    import os

    def findAllfile(path, allfile=[]):
        filelist = os.listdir(path)
        for filename in filelist:
            filepath = os.path.join(path, filename)
            if os.path.isdir(filepath):
                # print(filepath)
                findAllfile(filepath, allfile)
            else:
                allfile.append(filepath)
        return allfile
    # 图片路径
    src_path = r"./test-imgs-piliang/"
    file_path = findAllfile(src_path)
    images = []

    for path in file_path:
        print(path)
        img = cv2.imread(path)
        imgH, imgW, imgM = img.shape
        ratio = imgW/imgH
        R = 680/460
        if ratio > R:
            img = cv2.resize(img, (680, int(imgH * 680 / imgW / 20) * 20))
            print(int(imgH * 680 / imgW / 20) * 20)
        else:
            img = cv2.resize(img, (int(imgW * 460 / imgH/20) * 20, 460))
            print(int(imgW * 460 / imgH/10)*10)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        images.append(img)

    ui_display(images)

