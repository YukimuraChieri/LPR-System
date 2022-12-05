# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'search.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5.QtWidgets import (QTableView,    QHeaderView,    QFormLayout,
                             QVBoxLayout,   QWidget,        QApplication,
                             QHBoxLayout,   QPushButton,    QMainWindow,
                             QGridLayout,   QLabel,         QMessageBox)

from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal
import addsql
import qtawesome
import cv2
import pyttsx3
import copy


class Ui_Search(object):
    images = []

    def setupUi(self, Search):
        Search.setObjectName("Search")
        Search.resize(835, 661)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        Search.setFont(font)
        self.mainWnd = Search
        self.pushButton = QtWidgets.QPushButton(Search)
        self.pushButton.setGeometry(QtCore.QRect(790, 0, 41, 31))
        self.pushButton.setText("")
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(Search)
        self.pushButton_2.setGeometry(QtCore.QRect(750, 0, 41, 31))
        self.pushButton_2.setText("")
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(Search)
        self.pushButton_3.setGeometry(QtCore.QRect(710, 0, 41, 31))
        self.pushButton_3.setText("")
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtWidgets.QPushButton(Search)
        self.pushButton_4.setGeometry(QtCore.QRect(560, 130, 91, 41))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(12)
        self.pushButton_4.setFont(font)
        self.pushButton_4.setObjectName("pushButton_4")
        self.lineEdit_1 = QtWidgets.QLineEdit(Search)
        self.lineEdit_1.setGeometry(QtCore.QRect(160, 130, 41, 41))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.lineEdit_1.setFont(font)
        self.lineEdit_1.setObjectName("lineEdit_1")
        self.label = QtWidgets.QLabel(Search)
        self.label.setGeometry(QtCore.QRect(250, 130, 41, 41))
        self.lineEdit_1.setAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(28)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.radioButton = QtWidgets.QRadioButton(Search)
        self.radioButton.setGeometry(QtCore.QRect(60, 210, 131, 19))
        self.radioButton.setObjectName("radioButton")
        self.radioButton_2 = QtWidgets.QRadioButton(Search)
        self.radioButton_2.setGeometry(QtCore.QRect(230, 210, 115, 19))
        self.radioButton_2.setObjectName("radioButton_2")
        self.radioButton_3 = QtWidgets.QRadioButton(Search)
        self.radioButton_3.setGeometry(QtCore.QRect(410, 210, 115, 19))
        self.radioButton_3.setObjectName("radioButton_3")
        self.label_2 = QtWidgets.QLabel(Search)
        self.label_2.setGeometry(QtCore.QRect(20, 260, 111, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.lineEdit_2 = QtWidgets.QLineEdit(Search)
        self.lineEdit_2.setGeometry(QtCore.QRect(210, 130, 41, 41))
        self.lineEdit_2.setAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.lineEdit_2.setFont(font)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_3 = QtWidgets.QLineEdit(Search)
        self.lineEdit_3.setGeometry(QtCore.QRect(290, 130, 41, 41))
        self.lineEdit_3.setAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.lineEdit_3.setFont(font)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.lineEdit_4 = QtWidgets.QLineEdit(Search)
        self.lineEdit_4.setGeometry(QtCore.QRect(340, 130, 41, 41))
        self.lineEdit_4.setAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.lineEdit_4.setFont(font)
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.lineEdit_5 = QtWidgets.QLineEdit(Search)
        self.lineEdit_5.setGeometry(QtCore.QRect(390, 130, 41, 41))
        self.lineEdit_5.setAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.lineEdit_5.setFont(font)
        self.lineEdit_5.setObjectName("lineEdit_5")
        self.lineEdit_6 = QtWidgets.QLineEdit(Search)
        self.lineEdit_6.setGeometry(QtCore.QRect(440, 130, 41, 41))
        self.lineEdit_6.setAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.lineEdit_6.setFont(font)
        self.lineEdit_6.setObjectName("lineEdit_6")
        self.lineEdit_7 = QtWidgets.QLineEdit(Search)
        self.lineEdit_7.setGeometry(QtCore.QRect(490, 130, 41, 41))
        self.lineEdit_7.setAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.lineEdit_7.setFont(font)
        self.lineEdit_7.setObjectName("lineEdit_7")
        self.layout = QVBoxLayout()
        self.len = 1
        self.model = QStandardItemModel(1, 6)  # 存储任意结构数据
        self.model.setHorizontalHeaderLabels(['获取时间', '车牌', '类型', '置信度', '识别耗时', '来源'])
        self.tableView = QtWidgets.QTableView(Search)
        self.tableView.setModel(self.model)
        self.layout.addWidget(self.tableView)
        # 所有列自动拉伸，充满
        # self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableView.setGeometry(QtCore.QRect(20, 310, 801, 331))
        self.tableView.setObjectName("tableView")
        self.label_3 = QtWidgets.QLabel(Search)
        self.label_3.setGeometry(QtCore.QRect(150, 270, 231, 21))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label_3.setFont(font)
        self.label_3.setText("")
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(Search)
        self.label_4.setGeometry(QtCore.QRect(60, 135, 71, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.comboBox = QtWidgets.QComboBox(Search)
        # 添加条目
        self.comboBox.addItems(["所有类型", "蓝牌", "单层黄牌", "新能源车牌", "白色", "黑色-港澳"])
        self.comboBox.setGeometry(QtCore.QRect(160, 50, 371, 31))
        self.comboBox.setObjectName("comboBox")
        self.label_5 = QtWidgets.QLabel(Search)
        self.label_5.setGeometry(QtCore.QRect(40, 50, 91, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.pushButton_5 = QtWidgets.QPushButton(Search)
        self.pushButton_5.setGeometry(QtCore.QRect(720, 270, 93, 31))
        self.pushButton_5.setObjectName("pushButton_5")

        self.retranslateUi(Search)
        QtCore.QMetaObject.connectSlotsByName(Search)

    def retranslateUi(self, Search):
        _translate = QtCore.QCoreApplication.translate
        Search.setWindowTitle(_translate("Search", "Dialog"))
        self.pushButton_4.setText(_translate("Search", "查找"))
        self.label.setText(_translate("Search", " ·"))
        self.radioButton.setText(_translate("Search", "数据库中查找"))
        self.radioButton_2.setText(_translate("Search", "视频中查找"))
        self.radioButton_3.setText(_translate("Search", "图片中查找"))
        self.label_2.setText(_translate("Search", "查找结果："))
        self.label_4.setText(_translate("Search", "车牌号:"))
        self.label_5.setText(_translate("Search", "车牌类型:"))
        self.pushButton_5.setText(_translate("Search", "自动监控"))
        close_icon = qtawesome.icon('fa5s.times', color='white')
        mini_icon = qtawesome.icon('fa5s.window-minimize', color='white')
        set_icon = qtawesome.icon('fa5s.cog', color='white')
        search_icon = qtawesome.icon('fa5s.search', color='Gray')
        self.pushButton.setIcon(close_icon)     # 设置图标
        self.pushButton_2.setIcon(mini_icon)    # 设置图标
        self.pushButton_3.setIcon(set_icon)     # 设置图标
        self.pushButton_4.setIcon(search_icon)  # 设置图标
        self.pushButton_4.setIconSize(QtCore.QSize(30, 30))
        Search.setWindowFlags(QtCore.Qt.FramelessWindowHint)  # 无边框
        self.pushButton.clicked.connect(self.mainWnd.close)  # 关闭窗口
        self.pushButton_2.clicked.connect(self.mainWnd.showMinimized)  # 最小化窗口
        self.pushButton_4.clicked.connect(self.fun)
        self.pushButton_5.clicked.connect(self.jiankong)
        Search.setWindowOpacity(0.90)  # 设置窗口透明度
        pe = QtGui.QPalette()
        pe.setColor(QtGui.QPalette.Window, QtCore.Qt.darkCyan)  # 设置背景色
        Search.setPalette(pe)
        self.pushButton.setStyleSheet('''
                                                        QPushButton{
                                                        color:white;
                                                        border:none;
                                                        }
                                                        QPushButton:hover{
                                                        background:darkred;
                                                        }
                                                        ''')
        self.pushButton_2.setStyleSheet('''
                                                        QPushButton{
                                                        color:white;
                                                        border:none;
                                                        }
                                                        QPushButton:hover{
                                                        background:Gray;
                                                        }
                                                        ''')
        self.pushButton_3.setStyleSheet('''
                                                        QPushButton{
                                                        color:white;
                                                        border:none;
                                                        }
                                                        QPushButton:hover{
                                                        background:Gray;
                                                        }
                                                        ''')

    def fun(self):

        a = self.lineEdit_1.text()
        b = self.lineEdit_2.text()
        c = self.lineEdit_3.text()
        d = self.lineEdit_4.text()
        e = self.lineEdit_5.text()
        f = self.lineEdit_6.text()
        g = self.lineEdit_7.text()

        size = self.comboBox.currentText()

        print("车牌类型:", size)

        self.model.removeRows(0, self.len)

        if self.radioButton.isChecked():
            print("数据库查询结果：")
            db, cursor = addsql.db_open()

            result = addsql.search_mh(a, b, c, d, e, f, g, cursor)

            addsql.db_close(db)

            row = 0
            for res in result:
                if size != "所有类型":
                    if not res[2] == size:
                        continue
                for col in range(6):
                    i = QStandardItem(res[col])
                    self.model.setItem(row, col, i)
                row += 1
            self.tableView = QTableView()
            self.len = row

            if self.len == 0:
                QMessageBox.information(self.mainWnd,  # 使用infomation信息框
                                        "提示",
                                        "没有搜索到结果")

        elif self.radioButton_2.isChecked():
            print("视频查询结果：")

        elif self.radioButton_3.isChecked():
            import main
            self.images.clear()
            # self.model = QStandardItemModel(0, 6)  # 存储任意结构数据
            imgs = []
            file_new = []
            results_1 = []
            print("图片查询结果：")
            download_path = QtWidgets.QFileDialog.getExistingDirectory()
            print("download_path:", download_path)
            if len(download_path) > 0:
                file_path = main.findAllfile(download_path+'/')
                db, cursor = addsql.db_open()
                # 将数据库中不存在的加到数据库中
                for file in file_path:
                    flag = addsql.db_search_path(cursor, file)
                    if not flag:
                        print(False)
                        # self.FileSignal.emit(file)
                        main.fun_danzhang(file)
                # 查询符合要求的车牌号
                results = addsql.search_mh(a, b, c, d, e, f, g, cursor)
                if len(results) == 0:
                    return
                # 在上一步的结果中筛选出路径符合的结果
                for res in results:
                    if download_path in res[5]:
                        if res[5] not in file_new:
                            file_new.append(res[5])
                print("file_new:", len(file_new))
                for res in file_new:
                    # SQL 查询语句
                    sql = "select * from carinfo where source = " + "'" + res + "'"
                    # 执行SQL语句
                    cursor.execute(sql)
                    # 获取所有记录列表
                    result = cursor.fetchall()
                    for res_1 in result:
                        print("Result:", res_1)
                        results_1.append(res_1)
                file_new.clear()
                row = 0
                for res in results_1:
                    if not res in results:
                        continue
                    if size != "所有类型":
                        if not res[2] == size:
                            continue
                    file_new.append(res[5])
                    for col in range(6):
                        i = QStandardItem(res[col])
                        self.model.setItem(row, col, i)
                    row += 1
                self.len = row
                self.tableView = QTableView()

                if self.len == 0:
                    QMessageBox.information(self.mainWnd,  # 使用infomation信息框
                                            "提示",
                                            "没有搜索到结果")

                for res in file_new:
                    img = main.fun_danzhang(res)
                    if not img is None:
                        imgs.append(img)

                for img in imgs:

                    imgH, imgW, imgM = img.shape
                    ratio = imgW / imgH
                    R = 680 / 460
                    if ratio > R:
                        img = cv2.resize(img, (680, int(imgH * 680 / imgW / 20) * 20))
                    else:
                        img = cv2.resize(img, (int(imgW * 460 / imgH / 20) * 20, 460))
                    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
                    self.images.append(img)

                results_1.clear()
                file_path.clear()
                addsql.db_close(db)

        else:
            QMessageBox.information(self.mainWnd,  # 使用infomation信息框
                                    "提示",
                                    "请选择搜索方式")

    def jiankong(self):
        import pipline
        test = pyttsx3.init()
        cap = cv2.VideoCapture(0)
        timer = 0
        db, cursor = addsql.db_open()
        while True:
            ret, frame = cap.read()
            img, results, confidence, time_set, color = pipline.SimpleRecognizePlate_1(frame)
            cv2.imshow("result", img)

            for i, res in enumerate(results):
                if not addsql.db_search_text(cursor, res):
                    if res != "":
                        if timer > 6:
                            test.setProperty('rate', 150)
                            test.say("警告！检测到不明车辆")
                            test.runAndWait()
                            timer = 0
                        timer += 1
                else:
                    timer = 0

            keyval = cv2.waitKey(2) & 0xFF
            if keyval == ord('s'):
                test.setProperty('rate', 150)
                test.say(results)
                test.runAndWait()
            elif keyval == ord('q'):
                break
        addsql.db_close(db)
        cap.release()
        cv2.destroyAllWindows()


class Move(QtWidgets.QDialog):

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.m_flag = True
            self.m_Position = event.globalPos() - self.pos()  # 获取鼠标相对窗口的位置
            event.accept()
            # self.setCursor(QtGui. QCursor(QtCore.Qt.OpenHandCursor))  # 更改鼠标图标

    def mouseMoveEvent(self, QMouseEvent):
        if QtCore.Qt.LeftButton and self.m_flag:
            self.move(QMouseEvent.globalPos() - self.m_Position)  # 更改窗口位置
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        if QtCore.Qt.LeftButton and self.m_flag:
            self.m_flag = False
            self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Search = QtWidgets.QDialog()  # 创建一个QDialog，用来装载你需要的各种组件、控件
    Search = Move()
    ui = Ui_Search()  # ui是你创建的ui类的实例化对象
    ui.setupUi(Search)  # 执行类中的setupUi方法，方法的参数是第二步中创建的QMainWindow
    Search.show()  # 执行QDialog的show()方法，显示这个QMainWindow
    sys.exit(app.exec_())
