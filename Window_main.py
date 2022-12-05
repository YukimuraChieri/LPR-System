# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QMessageBox, QVBoxLayout, QListView, QWidget
from PyQt5.QtCore import QStringListModel, QAbstractListModel, QModelIndex, QSize
import qtawesome
import addsql
import math
import numpy as np

from PyQt5.QtCore import pyqtSignal, QThread


# 增加了一个继承自QThread类的类，重新写了它的run()函数
# run()函数即是新线程需要执行的：执行一个操作；发送计算完成的信号。


class WorkThread(QThread):

    # 定义信号
    LoadingSignal = pyqtSignal(int)
    ImagesSignal = pyqtSignal(list)
    PhotographSignal = pyqtSignal(list, list, list)
    Screenshot = pyqtSignal(list, list, list)
    images_1 = []
    load_flag = False
    folder_flag = False
    camera_flag = False
    video_flag = False
    photograph_flag = False
    crop_flag = False
    search_flag = False

    def __int__(self, src_path, file_path, frame):
        super().__init__()
        self.src_path = src_path
        self.file_path = file_path
        self.frame = frame

    def run(self):
        import paizhaoshibie
        import shexiangtoushibie
        import shipinshibie
        import pipline
        import main
        import cv2
        if self.load_flag:
            self.load_flag = False
            img_load = cv2.imread(r".\test-imgs-piliang\013.JPG")
            # 图片缩放，缩小原始数据量，加快处理速度
            imgHight, imgWidth, imgMode = img_load.shape

            area = imgHight * imgWidth
            print(area)

            if area > 800000:
                ratio = math.sqrt(area / 800000)
                H = int(imgHight / ratio)
                W = int(imgWidth / ratio)
            else:
                H = int(imgHight)
                W = int(imgWidth)
            img_load = cv2.resize(img_load, (W, H))  # 原图
            pipline.SimpleRecognizePlate(img_load)
            print("初始化线程结束")

        elif self.folder_flag:
            self.folder_flag = False
            print("路径批量识别")
            self.images_1.clear()
            print("src_path:", self.src_path)
            if len(self.src_path) > 0:

                file_path = main.findAllfile(self.src_path + '/')
                main.mkdir("C:/test-results/")
                results_file = r"C:/test-results/No16926mresults.txt"

                with open(results_file, 'w') as file_object:
                    file_object.write('')

                images = []
                print('file_path:', file_path)
                file_len = len(file_path)
                for n, file in enumerate(file_path):
                    print(file)
                    step = int((n + 1) / file_len * 100)
                    print("loading send:", step)
                    self.LoadingSignal.emit(step)  # 发射信号
                    image = cv2.imread(file)
                    if image is None:
                        continue
                    # 图片缩放，缩小原始数据量，加快处理速度
                    imgHight, imgWidth, imgMode = image.shape

                    area = imgHight * imgWidth

                    # print("SHAPE:", image.shape)

                    if area > 1000000:
                        ratio = math.sqrt(area / 1000000)
                        H = int(imgHight / ratio)
                        W = int(imgWidth / ratio)
                    img = cv2.resize(image, (W, H))  # 原图

                    img, results, confidence, haoshi, color = pipline.SimpleRecognizePlate_1(img)

                    images.append(img)

                    db, cursor = addsql.db_open()

                    text = ""

                    source = file
                    if not addsql.db_search_path(cursor, file):
                        for i, res in enumerate(results):
                            text = str(res)
                            con = confidence[i]
                            time = haoshi[i]
                            if text != "":
                                addsql.adddata(text, str(con), source, time, color[i], db, cursor)

                    addsql.db_close(db)

                    for i, res in enumerate(results):
                        results[i] = list(results[i])
                        if res[0] in main.province.keys():
                            for j, ch in enumerate(main.province[res[0]]):
                                results[i].insert(j + 1, ch)
                            del results[i][0]

                    with open(results_file, 'a') as file_object:
                        file_object.write(file[:].lower() + '\n')
                        for res in results:
                            for ch in res:
                                file_object.write(ch)
                            file_object.write('\n')
                        file_object.write('\n')

                    print("***********************")
                    for res in results:
                        for ch in res:
                            print(ch, end='')
                        print('\n', end='')
                    print("***********************\n")
                file_path.clear()

                for img in images:

                    imgH, imgW, imgM = img.shape
                    ratio = imgW / imgH
                    R = 680 / 460
                    if ratio > R:
                        img = cv2.resize(img, (680, int(imgH * 680 / imgW / 20) * 20))
                    else:
                        img = cv2.resize(img, (int(imgW * 460 / imgH / 20) * 20, 460))
                    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
                    self.images_1.append(img)
            self.ImagesSignal.emit(self.images_1)
            print("线程结束")

        elif self.camera_flag:
            self.camera_flag = False
            print("摄像头实时识别")
            shexiangtoushibie.shexiangtou()

        elif self.photograph_flag:
            print("拍摄照片识别")
            self.photograph_flag = False
            img_0, flag = paizhaoshibie.paizhao()
            img_crop = []
            items = []
            print(flag)
            if flag:
                print(img_0.shape)
                img, res, con, img_crop, color = paizhaoshibie.paizhao_s(img_0)
                # RGB转BGR
                img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
                print("img_crop:", len(img_crop))
                print("L_res:", len(res))
                print("RES:", res)
                for i, item in enumerate(res):
                    item = item + "\t  置信度:" + str(con[i])[0:6]
                    items.append(item)
                print("Items:", items)
                self.PhotographSignal.emit(list(img), img_crop, items)
            else:
                self.PhotographSignal.emit(list(img_0), img_crop, items)
            print("线程结束")

        elif self.video_flag:
            print("视频实时识别")
            self.video_flag = False
            shipinshibie.shipin(self.file_path)

        elif self.search_flag:
            self.search_flag = False
            main.fun_danzhang(self.file_path)

        elif self.crop_flag:
            self.crop_flag = False

            items = []
            self.frame = np.array(self.frame)
            img, res, con, img_1, color = paizhaoshibie.paizhao_s(self.frame, flag=False)
            imgH, imgW, imgM = img.shape
            ratio = imgW / imgH
            R = 640 / 500
            if ratio > R:
                img = cv2.resize(img, (640, int(imgH * 640 / imgW / 20) * 20))
                print(int(imgH * 680 / imgW / 20) * 20)
            else:
                img = cv2.resize(img, (int(imgW * 500 / imgH / 20) * 20, 500))
                print(int(imgH * 680 / imgW / 20) * 20)
            # RGB转BGR
            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
            img = list(img)
            for i, item in enumerate(res):
                item = item + "\t  置信度:" + str(con[i])[0:6]
                items.append(item)
            print("Items:", items)

            self.Screenshot.emit(img, img_1, items)  # 发射信号
            items.clear()


class Ui_MainWindow(QWidget):

    workThread = WorkThread()
    images_1 = []
    image = []
    items = []
    img_crop = []

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(928, 643)
        MainWindow.setFixedSize(MainWindow.width(), MainWindow.height())  # 固定窗口大小
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        MainWindow.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("bilibili.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.img_crop = []
        self.step = 0
        self.mainWnd = MainWindow
        self.layout = QVBoxLayout()
        self.listModel = QStringListModel()
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.graphicsView = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView.setGeometry(QtCore.QRect(20, 80, 640, 501))
        self.graphicsView.setStyleSheet("border-image: url(./pic/2.png);")
        self.graphicsView.setObjectName("graphicsView")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(680, 50, 141, 20))
        self.label.setObjectName("label")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(680, 150, 91, 20))
        self.label_3.setObjectName("label_3")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(20, 80, 640, 501))
        self.label_2.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.label_2.setText("")
        self.label_2.setObjectName("label_2")
        self.pushButton_left = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_left.setGeometry(QtCore.QRect(20, 80, 81, 501))
        self.pushButton_left.setText("")
        self.pushButton_left.setObjectName("pushButton_left")
        self.pushButton_right = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_right.setGeometry(QtCore.QRect(580, 80, 81, 501))
        self.pushButton_right.setText("")
        self.pushButton_right.setObjectName("pushButton_right")
        self.pushButton_user = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_user.setGeometry(QtCore.QRect(720, -1, 81, 31))
        self.pushButton_user.setObjectName("pushButton_user")
        self.pushButton_exit = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_exit.setGeometry(QtCore.QRect(640, -1, 81, 31))
        self.pushButton_exit.setObjectName("pushButton_exit")
        self.pushButton_set = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_set.setGeometry(QtCore.QRect(805, -1, 41, 31))
        self.pushButton_set.setText("")
        self.pushButton_set.setObjectName("pushButton_set")
        self.pushButton_mini = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_mini.setGeometry(QtCore.QRect(845, -1, 41, 31))
        self.pushButton_mini.setText("")
        self.pushButton_mini.setObjectName("pushButton_mini")
        self.pushButton_close = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_close.setGeometry(QtCore.QRect(885, -1, 41, 31))
        self.pushButton_close.setText("")
        self.pushButton_close.setObjectName("pushButton_close")
        self.label_12 = QtWidgets.QLabel(self.centralwidget)
        self.label_12.setGeometry(QtCore.QRect(310, 590, 72, 21))
        self.label_12.setText("")
        self.label_12.setObjectName("label_12")
        self.pushButton_switch = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_switch.setGeometry(QtCore.QRect(680, 540, 231, 61))
        self.pushButton_switch.setObjectName("pushButton_switch")
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(680, 230, 231, 291))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.pushButton_piliang = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.pushButton_piliang.setObjectName("pushButton_piliang")
        self.verticalLayout_2.addWidget(self.pushButton_piliang)
        self.pushButton_shipin = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.pushButton_shipin.setObjectName("pushButton_shipin")
        self.verticalLayout_2.addWidget(self.pushButton_shipin)
        self.pushButton_paizhao = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.pushButton_paizhao.setObjectName("pushButton_paizhao")
        self.verticalLayout_2.addWidget(self.pushButton_paizhao)
        self.pushButton_shexiangtou = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.pushButton_shexiangtou.setObjectName("pushButton_shexiangtou")
        self.verticalLayout_2.addWidget(self.pushButton_shexiangtou)
        self.pushButton_clear = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.pushButton_clear.setObjectName("pushButton_clear")
        self.verticalLayout_2.addWidget(self.pushButton_clear)
        self.pushButton_jietu = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.pushButton_jietu.setObjectName("pushButton_jietu")
        self.verticalLayout_2.addWidget(self.pushButton_jietu)
        self.listView = QtWidgets.QListView(self.centralwidget)
        self.listView.setGeometry(QtCore.QRect(680, 180, 231, 41))
        self.listView.setObjectName("listView")
        self.graphicsView_2 = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView_2.setGeometry(QtCore.QRect(680, 80, 231, 61))
        self.graphicsView_2.setObjectName("graphicsView_2")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(680, 80, 231, 61))
        self.label_4.setText("")
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(0, 60, 680, 540))
        self.label_5.setText("")
        self.label_5.setObjectName("label_5")
        self.graphicsView.raise_()
        self.label_2.raise_()
        self.label_5.raise_()
        self.label.raise_()
        self.label_3.raise_()
        self.pushButton_left.raise_()
        self.pushButton_right.raise_()
        self.pushButton_user.raise_()
        self.pushButton_exit.raise_()
        self.pushButton_set.raise_()
        self.pushButton_mini.raise_()
        self.pushButton_close.raise_()
        self.label_12.raise_()
        self.pushButton_switch.raise_()
        self.verticalLayoutWidget_2.raise_()
        self.listView.raise_()
        self.graphicsView_2.raise_()
        self.label_4.raise_()
        MainWindow.setCentralWidget(self.centralwidget)

        def click1():
            self.images_1.clear()
            download_path = QtWidgets.QFileDialog.getExistingDirectory()

            self.workThread.src_path = download_path
            self.workThread.folder_flag = True

            # self.workThread.exit()
            self.workThread.start()

            self.workThread.LoadingSignal.connect(self.fun_load)
            self.workThread.ImagesSignal.connect(self.getSignal)

        def click2():
            # self.workThread.exit()
            self.workThread.camera_flag = True
            self.workThread.start()

        def click3():
            download_path1 = QtWidgets.QFileDialog.getOpenFileName(MainWindow, '请选择视频文件', '', '*.mp4')
            download_path2 = download_path1[0]
            print(download_path2)
            if len(download_path2) == 0:
                print("您还没选视频哟")
                QMessageBox.information(MainWindow,  # 使用infomation信息框
                                        "提示",
                                        "您还没选择视频")
            elif download_path2[-3:] != "mp4":
                print("请选择MP4类型的视频文件")
                QMessageBox.information(MainWindow,  # 使用infomation信息框
                                        "提示",
                                        "请选择MP4类型的视频文件")
            else:
                # self.workThread.exit()
                self.workThread.video_flag = True
                self.workThread.file_path = download_path2
                self.workThread.start()

        def click4():
            self.label_2.clear()
            self.label_4.clear()
            self.label_12.clear()
            self.listModel.setStringList([])
            self.listView.setModel(self.listModel)
            self.layout.addWidget(self.listView)
            self.graphicsView.setStyleSheet("border-image: url(./pic/2.png);")
            print("clear")

        def click5():
            _translate = QtCore.QCoreApplication.translate
            # self.workThread.exit()
            self.workThread.photograph_flag = True
            self.workThread.start()

            self.label_4.clear()
            self.label_2.clear()

            self.img_crop.clear()
            self.listModel.setStringList(self.items)
            self.listView.setModel(self.listModel)
            self.layout.addWidget(self.listView)

            self.workThread.PhotographSignal.connect(self.getSignal_1)

        def click6():
            self.label_2.clear()
            self.label_4.clear()
            self.label_12.clear()
            self.listModel.setStringList([])
            self.listView.setModel(self.listModel)
            self.layout.addWidget(self.listView)
            print("截图")
        self.retranslateUi(MainWindow)
        self.pushButton_piliang.clicked.connect(click1)
        self.pushButton_shexiangtou.clicked.connect(click2)
        self.pushButton_shipin.clicked.connect(click3)
        self.pushButton_clear.clicked.connect(click4)
        self.pushButton_paizhao.clicked.connect(click5)
        self.pushButton_jietu.clicked.connect(click6)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "车牌识别"))
        self.label.setText(_translate("MainWindow", "定位车牌位置："))
        self.label_3.setText(_translate("MainWindow", "识别结果："))
        self.pushButton_user.setText(_translate("MainWindow", "账户设置"))
        self.pushButton_exit.setText(_translate("MainWindow", "退出登录"))
        self.pushButton_switch.setText(_translate("MainWindow", "“天眼”模式"))
        self.pushButton_piliang.setText(_translate("MainWindow", "路径批量识别"))
        self.pushButton_shipin.setText(_translate("MainWindow", "实时视频识别"))
        self.pushButton_paizhao.setText(_translate("MainWindow", "拍摄照片识别"))
        self.pushButton_shexiangtou.setText(_translate("MainWindow", "摄像实时识别"))
        self.pushButton_clear.setText(_translate("MainWindow", "清除识别数据"))
        self.pushButton_jietu.setText(_translate("MainWindow", "屏幕截图识别"))
        self.label_5.setScaledContents(True)  # 自适应
        self.label_5.setPixmap(QPixmap(r"./pic/edge_1.png"))
        self.listView.clicked.connect(self.checkItem)
        self.pushButton_close.clicked.connect(self.mainWnd.close)  # 关闭窗口
        self.pushButton_mini.clicked.connect(self.mainWnd.showMinimized)  # 最小化窗口
        MainWindow.setWindowFlags(QtCore.Qt.FramelessWindowHint)  # 无边框
        MainWindow.setWindowOpacity(0.95)  # 设置窗口透明度
        pe = QtGui.QPalette()
        pe.setColor(QtGui.QPalette.Window, QtCore.Qt.darkCyan)  # 设置背景色
        MainWindow.setPalette(pe)
        paizhao_icon = qtawesome.icon('fa5s.camera', color='white')
        shipin_icon = qtawesome.icon('fa5s.film', color='white')
        piliang_icon = qtawesome.icon('fa5s.folder', color='white')
        shexiangtou_icon = qtawesome.icon('fa5s.video', color='white')
        clear_icon = qtawesome.icon('fa5s.broom', color='white')
        jietu_icon = qtawesome.icon('fa5s.image', color='white')
        close_icon = qtawesome.icon('fa5s.times', color='white')
        mini_icon = qtawesome.icon('fa5s.window-minimize', color='white')
        set_icon = qtawesome.icon('fa5s.cog', color='white')
        switch_icon = qtawesome.icon('fa5s.eye', color='white')
        self.pushButton_paizhao.setIcon(paizhao_icon)   # 设置图标
        self.pushButton_shipin.setIcon(shipin_icon)     # 设置图标
        self.pushButton_piliang.setIcon(piliang_icon)   # 设置图标
        self.pushButton_shexiangtou.setIcon(shexiangtou_icon)   # 设置图标
        self.pushButton_clear.setIcon(clear_icon)       # 设置图标
        self.pushButton_jietu.setIcon(jietu_icon)       # 设置图标
        self.pushButton_close.setIcon(close_icon)       # 设置图标
        self.pushButton_mini.setIcon(mini_icon)         # 设置图标
        self.pushButton_set.setIcon(set_icon)           # 设置图标
        self.pushButton_switch.setIcon(switch_icon)     # 设置图标
        self.pushButton_paizhao.setIconSize(QtCore.QSize(35, 35))
        self.pushButton_shipin.setIconSize(QtCore.QSize(35, 35))
        self.pushButton_piliang.setIconSize(QtCore.QSize(35, 35))
        self.pushButton_shexiangtou.setIconSize(QtCore.QSize(35, 35))
        self.pushButton_clear.setIconSize(QtCore.QSize(35, 35))
        self.pushButton_jietu.setIconSize(QtCore.QSize(35, 35))
        self.pushButton_switch.setIconSize(QtCore.QSize(40, 40))
        op = QtWidgets.QGraphicsOpacityEffect()
        op_1 = QtWidgets.QGraphicsOpacityEffect()
        # 设置透明度的值
        op.setOpacity(0.4)
        op_1.setOpacity(0.4)
        self.pushButton_left.setGraphicsEffect(op)
        self.pushButton_right.setGraphicsEffect(op_1)
        left_icon = qtawesome.icon('fa5s.chevron-left', color='black')
        right_icon = qtawesome.icon('fa5s.chevron-right', color='black')
        self.pushButton_left.setIcon(left_icon)  # 设置图标
        self.pushButton_right.setIcon(right_icon)  # 设置图标
        self.pushButton_left.setIconSize(QtCore.QSize(40, 40))
        self.pushButton_right.setIconSize(QtCore.QSize(40, 40))
        self.pushButton_piliang.setStyleSheet('''
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
        self.pushButton_shipin.setStyleSheet('''
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
        self.pushButton_shexiangtou.setStyleSheet('''
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
        self.pushButton_paizhao.setStyleSheet('''
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
        self.pushButton_clear.setStyleSheet('''
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
        self.pushButton_jietu.setStyleSheet('''
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
        self.pushButton_left.setStyleSheet('''
                                            QPushButton{
                                            border:none;
                                            }
                                            QPushButton:hover{
                                            background:Gray;
                                            }
                                            ''')
        self.pushButton_right.setStyleSheet('''
                                            QPushButton{
                                            border:none;
                                            }
                                            QPushButton:hover{
                                            background:Gray;
                                            }
                                            ''')
        self.pushButton_set.setStyleSheet('''
                                            QPushButton{
                                            color:white;
                                            border:none;
                                            }
                                            QPushButton:hover{
                                            background:Gray;
                                            }
                                            ''')
        self.pushButton_mini.setStyleSheet('''
                                            QPushButton{
                                            color:white;
                                            border:none;
                                            }
                                            QPushButton:hover{
                                            background:Gray;
                                            }
                                            ''')
        self.pushButton_close.setStyleSheet('''
                                            QPushButton{
                                            color:white;
                                            border:none;
                                            }
                                            QPushButton:hover{
                                            background:darkred;
                                            }
                                            ''')
        self.pushButton_exit.setStyleSheet('''
                                            QPushButton{
                                            color:white;
                                            border:none;
                                            }
                                            QPushButton:hover{
                                            color:blue;
                                            background:Gray;
                                            }
                                            ''')
        self.pushButton_user.setStyleSheet('''
                                            QPushButton{
                                            color:white;
                                            border:none;
                                            }
                                            QPushButton:hover{
                                            color:blue;
                                            background:Gray;
                                            }
                                            ''')
        self.pushButton_switch.setStyleSheet('''
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

    def checkItem(self, index):
        self.label_4.setScaledContents(True)  # 自适应
        self.label_4.setPixmap(QPixmap.fromImage(self.img_crop[index.row()]))

    def load_data(self, sp):
        sp.showMessage("程序启动中请稍等...\n", QtCore.Qt.AlignHCenter | QtCore.Qt.AlignBottom,
                       QtCore.Qt.black)
        QtWidgets.qApp.processEvents()  # 允许主进程处理事件

    def getSignal(self, connect):
        print("Receive Images Signal:::::::::::::::", len(connect))
        self.images_1 = connect

    def fun_load(self, connect):
        print(connect, "%")

    def getSignal_1(self, image, img_crop, items):
        print("Receive PhotographSignal:::::::::::::::")
        self.image = np.array(image)
        self.img_crop = img_crop
        self.items = items

        self.label_2.setScaledContents(True)  # 自适应
        self.image = QImage(self.image.data, self.image.shape[1], self.image.shape[0], QImage.Format_RGB888)
        self.label_2.setPixmap(QPixmap.fromImage(self.image))

        if len(img_crop) > 0:

            self.listModel.setStringList(self.items)
            self.listView.setModel(self.listModel)
            self.layout.addWidget(self.listView)

            self.label_4.setScaledContents(True)  # 自适应
            if len(self.img_crop) > 0:
                self.label_4.setPixmap(QPixmap.fromImage(self.img_crop[0]))

    def getSignal_2(self, image):

        # self.workThread.exit()
        self.workThread.crop_flag = True
        self.workThread.frame = image
        self.workThread.start()
        self.workThread.Screenshot.connect(self.getSignal_3)

    def getSignal_3(self, image, img_crop, items):
        print("Receive Screenshot Signal:::::::::::::::")
        self.image = np.array(image)
        self.img_crop = img_crop
        self.items = items

        self.label_2.setScaledContents(False)  # 取消自适应
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)    # 图像居中
        self.graphicsView.setStyleSheet("border-image: url(./pic/black.jpg);")
        self.image = QImage(self.image.data, self.image.shape[1], self.image.shape[0], QImage.Format_RGB888)
        self.label_2.setPixmap(QPixmap.fromImage(self.image))
        print("len(img_crop):", len(img_crop))
        if len(img_crop) > 0:

            self.listModel.setStringList(items)
            self.listView.setModel(self.listModel)
            self.layout.addWidget(self.listView)

            self.label_4.setScaledContents(True)  # 自适应
            if len(self.img_crop) > 0:
                self.label_4.setPixmap(QPixmap.fromImage(self.img_crop[0]))

    def getSignal_4(self, file_path):

        self.workThread.search_flag = True
        self.workThread.file_path = file_path
        self.workThread.run()


class Myset(QtWidgets.QMainWindow):
    """对QMainWindow类重写，实现一些功能"""

    def closeEvent(self, event):
        """
            重写closeEvent方法，实现MainWindow窗体关闭时执行一些代码
            :param event: close()触发的事件
            :return: None
        """
        reply = QMessageBox.question(self, '确认退出', "是否要退出？",
                                               QMessageBox.Yes | QMessageBox.No,
                                               QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.m_flag = True
            self.m_Position = event.globalPos() - self.pos()  # 获取鼠标相对窗口的位置
            event.accept()
            # self.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))  # 更改鼠标图标

    def mouseMoveEvent(self, QMouseEvent):
        if QtCore.Qt.LeftButton and self.m_flag:
            self.move(QMouseEvent.globalPos() - self.m_Position)  # 更改窗口位置
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.m_flag = False
        self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()  # 创建一个QMainWindow，用来装载你需要的各种组件、控件
    MainWindow = Myset()     # 注意修改为了自己重写的Myset类
    ui = Ui_MainWindow()    # ui是你创建的ui类的实例化对象
    splash = QtWidgets.QSplashScreen(QtGui.QPixmap(r".\pic\start_1.png"))
    splash.show()           # 显示启动界面
    ui.load_data(splash)    # 加载数据
    QtWidgets.qApp.processEvents()  # 处理主进程事件

    splash.finish(MainWindow)  # 隐藏启动界面
    ui.setupUi(MainWindow)  # 执行类中的setupUi方法，方法的参数是第二步中创建的QMainWindow
    MainWindow.show()       # 执行QMainWindow的show()方法，显示这个QMainWindow
    sys.exit(app.exec_())
