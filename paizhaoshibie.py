from PyQt5.QtGui import QImage
import pipline as pp
import addsql
import cv2
import os
import time
import math
import copy

# import cropping
# import jiaozheng

os.system("color 0b")

save_path = r"D:\cnsoftbeiresult\paizhao\pic_save"


def mkdir(path):
    folder = os.path.exists(path)

    if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(path)  # makedirs 创建文件时如果路径不存在会创建这个路径
        print("---  new folder...  ---")
        print("---  OK  ---")
    else:
        print("---  There is this folder!  ---")


mkdir(save_path)


def paizhao():
    cap = cv2.VideoCapture(0)
    flag = False
    frame_1 = None
    while True:
        ret, frame = cap.read()
        if not frame is None:
            cv2.imshow("capture", frame)
        k = cv2.waitKey(1)
        if k == ord('q'):
            break
        elif k == ord(' '):
            frame_1 = frame
            flag = True
    cap.release()
    cv2.destroyAllWindows()
    return frame_1, flag


def paizhao_s(image, flag=True):

    img_1 = []
    img_crop = []
    res_set = []  # 结果列表
    con_set = []  # 置信度列表
    time_set = []  # 耗时列表
    color = []  # 颜色列表

    image_new = image.copy()
    plateType = ["蓝牌", "单层黄牌", "新能源车牌", "白色", "黑色-港澳"]
    # 车牌粗定位
    images = pp.detect.detectPlateRough(image, image.shape[0], top_bottom_padding_rate=0.1)

    for img in images:
        x2, y2, w2, h2 = img[1]
        img_1.append(img[0])
        # 绘制一个黑色矩形
        cv2.rectangle(image, (int(x2), int(y2)), (int(x2 + w2), int(y2 + h2)), (0, 0, 0), -1, 1)

    angles = [-10, 10, -20, 20, -30, 30]

    imageH, imageW, imageM = image.shape
    i = 0
    for ang in angles:
        image_1 = pp.rotate_bound(image, ang)
        # cv2.imwrite("./test_picture" + str(ang) + ".jpg", image_1)
        images_1 = pp.detect.detectPlateRough(image_1, image_1.shape[0], top_bottom_padding_rate=0.1, angle=ang)
        for img in images_1:

            X, Y, W, H = img[1]
            print("ANGLE=", ang)
            if ang >= 0:
                ang = ang * math.pi / 180
                hc = imageH * math.cos(ang)
                if hc >= Y:
                    x1 = (X - (hc - Y) * math.tan(ang)) * math.cos(ang)
                    y1 = imageH - (X - x1 / math.cos(ang)) / math.sin(ang) - x1 * math.tan(ang)

                else:
                    yhc = Y - hc
                    alpha = math.atan(yhc / X)
                    beta = ang - alpha
                    L = math.sqrt(yhc ** 2 + X ** 2)
                    x1 = L * math.cos(beta)
                    y1 = imageH - L * math.sin(beta)

                x2 = x1
                y2 = y1 - W * math.sin(ang)
                w2 = W * math.cos(ang) + H * math.sin(ang)
                h2 = W * math.sin(ang) + H * math.cos(ang)

                img[1] = [x2, y2, w2, h2]
            else:
                ang = 90 + ang
                ang = ang * math.pi / 180
                hc = imageW * math.cos(ang)
                if hc >= Y:
                    y1 = (X - (hc - Y) * math.tan(ang)) * math.cos(ang)
                    x1 = imageW - (X - y1 / math.cos(ang)) / math.sin(ang) - y1 * math.tan(ang)
                    x1 = imageW - x1

                else:
                    yhc = Y - hc
                    alpha = math.atan(yhc / X)
                    beta = ang - alpha
                    L = math.sqrt(yhc ** 2 + X ** 2)
                    y1 = L * math.cos(beta)
                    x1 = imageW - L * math.sin(beta)
                    x1 = imageW - x1

                x2 = x1 - H * math.sin(ang)
                y2 = y1
                w2 = H * math.cos(ang) + W * math.sin(ang)
                h2 = H * math.sin(ang) + W * math.cos(ang)

                img[1] = [x2, y2, w2, h2]
            i += 1
            images.append(img)
            img_1.append(img[0])
            # 绘制一个黑色矩形
            cv2.rectangle(image, (int(x2), int(y2)), (int(x2 + w2), int(y2 + h2)), (0, 0, 0), -1, 1)

    print("LEN:", len(images))

    for j, plate in enumerate(images):
        t0 = time.time()
        plate, rect, origin_plate = plate

        plate = cv2.resize(plate, (136, 36 * 2))
        t1 = time.time()

        res = pp.td.SimplePredict(plate)

        ptype = res.argmax()

        print(plateType[ptype])

        if ptype > 0 and ptype < 5:
            plate = cv2.bitwise_not(plate)

        image_rgb = pp.fm.findContoursAndDrawBoundingBox(plate)

        image_rgb = pp.fv.finemappingVertical(image_rgb)

        # cv2.imshow('image:::::::::::::', image_rgb)

        pp.cache.verticalMappingToFolder(image_rgb)
        print("e2e:", pp.e2e.recognizeOne(image_rgb))
        image_gray = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2GRAY)

        image_gray = pp.horizontalSegmentation(image_gray)

        print("校正", time.time() - t1, "s")

        t2 = time.time()
        if plateType[ptype] == "新能源车牌":
            val = pp.segmentation.slidingWindowsEval_1(image_gray)
        else:
            val = pp.segmentation.slidingWindowsEval(image_gray)
        # print(val)
        print("分割和识别", time.time() - t2, "s")
        if len(val) == 3:
            blocks, res, confidence = val
            if plateType[ptype] == "新能源车牌":
                confidence /= 7
            else:
                confidence /= 8
            if confidence > 0.65:
                color_1 = plateType[ptype]
                time_set.append(str(time.time() - t0) + " s")
                image_new = pp.drawRectBox(image_new, rect, res + "-" + color_1)
                res_set.append(res)
                con_set.append(confidence)

                print("Res:", res)
                print("Ptype:", ptype)

                color.append(color_1)

                print("color:", color)

            if confidence > 0:
                print("车牌:", res, "置信度:", confidence)

    db, cursor = addsql.db_open()

    text = ""

    if flag:
        source = "camera"
    else:
        source = "screenshot"

    for i, res in enumerate(res_set):
        text = str(res)
        con = con_set[i]
        time1 = time_set[i]
        if text != "":
            addsql.adddata(text, str(con), source, time1, color[i], db, cursor)
    addsql.db_close(db)

    for j, img_2 in enumerate(img_1):
        print(j)
        img_2 = cv2.resize(img_2, (200, 40))
        img_2 = cv2.cvtColor(img_2, cv2.COLOR_RGB2BGR)
        img_2 = QImage(img_2.data, img_2.shape[1], img_2.shape[0], QImage.Format_RGB888)
        img_crop.append(img_2)

    return image_new, res_set, con_set, img_crop, color
