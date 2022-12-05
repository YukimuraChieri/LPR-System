# coding = utf-8
import detect
import copy

# import cropping
import jiaozheng

import finemapping as fm

import segmentation
import cv2

import numpy as np

from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
import json

import sys
import typeDistinguish as td
import imp
import time
import math

imp.reload(sys)
fontC = ImageFont.truetype("./Font/platech.ttf", 28, 0)

import e2e
# 寻找车牌左右边界


def rotate(image, angle, center=None, scale=1.0):  # 1
    (h, w) = image.shape[:2]  # 2
    if center is None:  # 3
        center = (w // 2, h // 2)  # 4

    M = cv2.getRotationMatrix2D(center, angle, scale)  # 5

    rotated = cv2.warpAffine(image, M, (w, h))  # 6
    return rotated  # 7


def rotate_bound(image, angle):
    # grab the dimensions of the image and then determine the
    # center
    (h, w) = image.shape[:2]
    (cX, cY) = (w // 2, h // 2) # grab the rotation matrix (applying the negative of the
    # angle to rotate clockwise), then grab the sine and cosine
    # (i.e., the rotation components of the matrix)
    M = cv2.getRotationMatrix2D((cX, cY), -angle, 1.0)
    cos = np.abs(M[0, 0])
    sin = np.abs(M[0, 1]) # compute the new bounding dimensions of the image
    nW = int((h * sin) + (w * cos))
    nH = int((h * cos) + (w * sin)) # adjust the rotation matrix to take into account translation
    M[0, 2] += (nW / 2) - cX
    M[1, 2] += (nH / 2) - cY # perform the actual rotation and return the image
    return cv2.warpAffine(image, M, (nW, nH))


def find_edge(image):
    sum_i = image.sum(axis=0)
    sum_i = sum_i.astype(np.float)
    sum_i /= image.shape[0]*255
    # print sum_i

    start = 0
    end = image.shape[1]-1

    for i, one in enumerate(sum_i):
        if one > 0.4:
            start = i
            if start-3 < 0:
                start = 0
            else:
                start -= 3

            break
    for i, one in enumerate(sum_i[::-1]):

        if one > 0.4:
            end = end - i
            if end+4 > image.shape[1]-1:
                end = image.shape[1]-1
            else:
                end += 4
            break
    return start, end


# 垂直边缘检测
def verticalEdgeDetection(image):
    image_sobel = cv2.Sobel(image.copy(), cv2.CV_8U, 1, 0)
    # image = auto_canny(image_sobel)

    # img_sobel, CV_8U, 1, 0, 3, 1, 0, BORDER_DEFAULT
    # canny_image = auto_canny(image)
    flag, thres = cv2.threshold(image_sobel, 0, 255, cv2.THRESH_OTSU|cv2.THRESH_BINARY)
    print(flag)
    flag, thres = cv2.threshold(image_sobel, int(flag*0.7), 255, cv2.THRESH_BINARY)
    # thres = simpleThres(image_sobel)
    kernal = np.ones(shape = (3, 15))
    thres = cv2.morphologyEx(thres, cv2.MORPH_CLOSE, kernal)
    return thres


# 确定粗略的左右边界
def horizontalSegmentation(image):

    thres = verticalEdgeDetection(image)
    # thres = thres*image
    head, tail = find_edge(thres)
    # print head, tail
    # cv2.imshow("edge", thres)
    tail = tail+5
    if tail > 135:
        tail = 135
    image = image[0:35, head:tail]
    image = cv2.resize(image, (int(136), int(36)))
    return image


# 打上boundingbox和标签
def drawRectBox(image, rect, addText):
    cv2.rectangle(image, (int(rect[0]), int(rect[1])), (int(rect[0] + rect[2]), int(rect[1] + rect[3])), (0, 0, 255), 3, cv2.LINE_AA)
    cv2.rectangle(image, (int(rect[0]-1), int(rect[1])-40), (int(rect[0] + 240), int(rect[1])), (0, 0, 255), -1, cv2.LINE_AA)

    img = Image.fromarray(image)
    draw = ImageDraw.Draw(img)
    # draw.text((int(rect[0]+1), int(rect[1]-16)), addText.decode("utf-8"), (255, 255, 255), font = fontC)
    draw.text((int(rect[0]+4), int(rect[1]-40)), addText, (255, 255, 255), font=fontC)
    imagex = np.array(img)

    return imagex


import cache
import finemapping_vertical as fv


def RecognizePlateJson(image):
    images = detect.detectPlateRough(image, image.shape[0], top_bottom_padding_rate = 0.1)
    jsons = []
    for j, plate in enumerate(images):
        plate, rect, origin_plate = plate
        res, confidence = e2e.recognizeOne(origin_plate)
        print("res", res)

        # cv2.imwrite(". /"+str(j)+"_rough.jpg", plate)

        # print("车牌类型:", ptype)
        # plate = cv2.cvtColor(plate, cv2.COLOR_RGB2GRAY)
        plate = cv2.resize(plate, (136, int(36*2.5)))

        ptype = td.SimplePredict(plate)
        if ptype > 0 and ptype < 4:
            plate = cv2.bitwise_not(plate)
        # demo = verticalEdgeDetection(plate)

        image_rgb = fm.findContoursAndDrawBoundingBox(plate)
        image_rgb = fv.finemappingVertical(image_rgb)
        cache.verticalMappingToFolder(image_rgb)
        # print time.time() - t1, "校正"
        print("e2e:", e2e.recognizeOne(image_rgb)[0])

        # image_gray = cv2.cvtColor(image_rgb, cv2.COLOR_BGR2GRAY)
        # cv2.imwrite(". /"+str(j)+".jpg", image_gray)
        # image_gray = horizontalSegmentation(image_gray)

        res, confidence = e2e.recognizeOne(image_rgb)
        res_json = {}
        if confidence > 0.6:
            res_json["Name"] = res
            res_json["Type"] = td.plateType[ptype]
            res_json["Confidence"] = confidence
            res_json["x"] = int(rect[0])
            res_json["y"] = int(rect[1])
            res_json["w"] = int(rect[2])
            res_json["h"] = int(rect[3])
            jsons.append(res_json)
    print(json.dumps(jsons, ensure_ascii=False, encoding="gb2312"))

    return json.dumps(jsons, ensure_ascii=False, encoding="gb2312")


def SimpleRecognizePlateByE2E(image):
    # 开始计时
    t0 = time.time()
    # 车牌粗定位
    images = detect.detectPlateRough(image, image.shape[0], top_bottom_padding_rate = 0.1)
    res_set = []
    for j, plate in enumerate(images):
        plate, rect, origin_plate = plate
        # plate = cv2.cvtColor(plate, cv2.COLOR_RGB2GRAY)
        plate = cv2.resize(plate, (136, 36*2))
        res, confidence = e2e.recognizeOne(origin_plate)
        print("res", res)

        t1 = time.time()
        ptype = td.SimplePredict(plate)
        if ptype > 0 and ptype < 5:
            # pass
            plate = cv2.bitwise_not(plate)
        image_rgb = fm.findContoursAndDrawBoundingBox(plate)
        image_rgb = fv.finemappingVertical(image_rgb)
        image_rgb = fv.finemappingVertical(image_rgb)
        cache.verticalMappingToFolder(image_rgb)
        # cv2.imwrite(". /"+str(j)+".jpg", image_rgb)
        res, confidence = e2e.recognizeOne(image_rgb)
        print(res, confidence)
        res_set.append([[], res, confidence])

        if confidence > 0.7:
            image = drawRectBox(image, rect, res+" "+str(round(confidence, 3)))
    return image, res_set


def SimpleRecognizePlate(image):

    # 开始计时
    t = time.time()
    plateType = ["蓝牌", "单层黄牌", "新能源车牌", "白色", "黑色-港澳"]

    W, H, M = image.shape
    # image_1 = cv2.resize(image, (int(H / 3), int(W / 3)))
    # cv2.imshow("step2", image_1)
    # cv2.waitKey(0)

    # 车牌粗定位
    images = detect.detectPlateRough(image, image.shape[0], top_bottom_padding_rate=0.1)

    time_crop = time.time() - t
    if len(images) > 0:
        time_crop /= len(images)

    res_set = []    # 结果列表
    con_set = []    # 置信度列表
    time_set = []   # 耗时列表
    color = []      # 颜色列表
    for j, plate in enumerate(images):

        t0 = time.time()
        plate, rect, origin_plate = plate

        plate = cv2.resize(plate, (136, 36*2))
        t1 = time.time()

        W, H, M = plate.shape
        # plate_1 = cv2.resize(plate, (H * 2, W * 2))
        # cv2.imshow("step3_1", plate_1)
        # cv2.waitKey(0)

        res = td.SimplePredict(plate)

        ptype = res.argmax()

        print(plateType[ptype])

        if ptype > 0 and ptype < 5:
            plate = cv2.bitwise_not(plate)

        image_rgb = fm.findContoursAndDrawBoundingBox(plate)

        W, H, M = image_rgb.shape
        # image_rgb_1 = cv2.resize(image_rgb, (H * 2, W * 2))
        # cv2.imshow("step3_2", image_rgb_1)
        # cv2.waitKey(0)

        image_rgb = fv.finemappingVertical(image_rgb)

        cache.verticalMappingToFolder(image_rgb)
        print("e2e:", e2e.recognizeOne(image_rgb))
        image_gray = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2GRAY)

        W, H = image_gray.shape
        # image_gray_1 = cv2.resize(image_gray, (H*2, W*2))
        # cv2.imshow("step3_3", image_gray_1)
        # cv2.waitKey(0)

        image_gray = horizontalSegmentation(image_gray)

        W, H = image_gray.shape
        # image_gray_1 = cv2.resize(image_gray, (H * 2, W * 2))
        # cv2.imshow("step3_4", image_gray_1)
        # cv2.waitKey(0)

        print("校正", time.time() - t1, "s")

        t2 = time.time()
        if plateType[ptype] == "新能源车牌":
            val = segmentation.slidingWindowsEval_1(image_gray)
        else:
            val = segmentation.slidingWindowsEval(image_gray)

        print("分割和识别", time.time() - t2, "s")
        if len(val) == 3:
            blocks, res, confidence = val
            if plateType[ptype] == "新能源车牌":
                confidence /= 7
            else:
                confidence /= 8
            if confidence > 0.8:
                color_1 = plateType[ptype]
                time_set.append(str(time.time() - t0 + time_crop)+" s")
                image = drawRectBox(image, rect, res+"-"+color_1)
                res_set.append(res)
                con_set.append(confidence)

                print("Res:", res)
                print("Ptype:", ptype)

                color.append(color_1)

                print("color:", color)

            if confidence > 0:
                print("车牌:", res, "置信度:", confidence)

        break

    print(time.time() - t, "s")
    return image, res_set, con_set, time_set, color


def SimpleRecognizePlate_1(image):
    if not image is None:
        image_new = image.copy()
    else:
        return
    # 开始计时
    t = time.time()
    plateType = ["蓝牌", "单层黄牌", "新能源车牌", "白色", "黑色-港澳"]
    # 车牌粗定位
    images = detect.detectPlateRough(image, image.shape[0], top_bottom_padding_rate=0.1)

    for i, img in enumerate(images):
        # cv2.imshow("step3_"+str(i), np.array(img))
        # cv2.waitKey(0)
        x2, y2, w2, h2 = img[1]
        # 绘制一个黑色矩形覆盖找到的车牌区域以免重复
        cv2.rectangle(image, (int(x2), int(y2)), (int(x2 + w2), int(y2 + h2)), (0, 0, 0), -1, 1)

    angles = [-10, 10, -20, 20, -30, 30]

    imageH, imageW, imageM = image.shape
    for ang in angles:
        image_1 = rotate_bound(image, ang)
        images_1 = detect.detectPlateRough(image_1, image_1.shape[0], top_bottom_padding_rate=0.1, angle=ang)
        for img in images_1:
            # img[0] = jiaozheng.correct(img[0])
            # print("ANG:::::::", ang, "\tPoint:", img[1])
            # print("IMAGE SHAPE:", imgW, imgH)
            X, Y, W, H = img[1]
            print("ANGLE=", ang)
            if ang >= 0:
                ang = ang * math.pi / 180
                hc = imageH * math.cos(ang)
                if hc >= Y:
                    x1 = (X - (hc - Y) * math.tan(ang)) * math.cos(ang)
                    y1 = imageH - (X - x1 / math.cos(ang)) / math.sin(ang) - x1 * math.tan(ang)
                    # cv2.circle(image, (int(x1), int(y1)), 20, (0, 0, 255), -1)
                    print("矫正后点的位置:", x1, y1)

                else:
                    yhc = Y - hc
                    alpha = math.atan(yhc / X)
                    beta = ang - alpha
                    L = math.sqrt(yhc ** 2 + X ** 2)
                    x1 = L * math.cos(beta)
                    y1 = imageH - L * math.sin(beta)
                    # cv2.circle(image, (int(x1), int(y1)), 20, (0, 0, 255), -1)
                    print("矫正后点的位置:", x1, y1)

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
                    # cv2.circle(image, (int(x1), int(y1)), 20, (0, 0, 255), -1)
                    print("矫正后点的位置:", x1, y1)

                else:
                    yhc = Y - hc
                    alpha = math.atan(yhc / X)
                    beta = ang - alpha
                    L = math.sqrt(yhc ** 2 + X ** 2)
                    y1 = L * math.cos(beta)
                    x1 = imageW - L * math.sin(beta)
                    x1 = imageW - x1
                    # cv2.circle(image, (int(x1), int(y1)), 20, (0, 0, 255), -1)
                    print("矫正后点的位置:", x1, y1)

                x2 = x1 - H * math.sin(ang)
                y2 = y1
                w2 = H * math.cos(ang) + W * math.sin(ang)
                h2 = H * math.sin(ang) + W * math.cos(ang)

                img[1] = [x2, y2, w2, h2]
            images.append(img)
            # 绘制一个黑色矩形
            cv2.rectangle(image, (int(x2), int(y2)), (int(x2 + w2), int(y2 + h2)), (0, 0, 0), -1, 1)

    print("LEN:", len(images))
    time_crop = time.time() - t
    if len(images) > 0:
        time_crop /= len(images)

    res_set = []    # 结果列表
    con_set = []    # 置信度列表
    time_set = []   # 耗时列表
    color = []      # 颜色列表
    for j, plate in enumerate(images):
        t0 = time.time()
        plate, rect, origin_plate = plate

        plate = cv2.resize(plate, (136, 36 * 2))
        t1 = time.time()

        res = td.SimplePredict(plate)

        ptype = res.argmax()

        print(plateType[ptype])

        if ptype > 0 and ptype < 5:
            plate = cv2.bitwise_not(plate)

        image_rgb = fm.findContoursAndDrawBoundingBox(plate)

        image_rgb = fv.finemappingVertical(image_rgb)

        cache.verticalMappingToFolder(image_rgb)
        print("e2e:", e2e.recognizeOne(image_rgb))
        image_gray = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2GRAY)

        image_gray = horizontalSegmentation(image_gray)

        print("校正", time.time() - t1, "s")

        t2 = time.time()
        if plateType[ptype] == "新能源车牌":
            val = segmentation.slidingWindowsEval_1(image_gray)
        else:
            val = segmentation.slidingWindowsEval(image_gray)
        # print(val)
        print("分割和识别", time.time() - t2, "s")
        if len(val) == 3:
            blocks, res, confidence = val
            if plateType[ptype] == "新能源车牌":
                confidence /= 7
            else:
                confidence /= 8
            if confidence > 0.70:
                color_1 = plateType[ptype]
                time_set.append(str(time.time() - t0 + time_crop) + " s")
                image_new = drawRectBox(image_new, rect, res + "-" + color_1)
                res_set.append(res)
                con_set.append(confidence)

                print("Res:", res)
                print("Ptype:", ptype)

                color.append(color_1)

                print("color:", color)

            if confidence > 0:
                print("车牌:", res, "置信度:", confidence)

    print(time.time() - t, "s")
    return image_new, res_set, con_set, time_set, color


def SimpleRecognizePlate_2(image):
    if not image is None:
        image_new = image.copy()
    else:
        return
    # 开始计时
    t = time.time()
    plateType = ["蓝牌", "单层黄牌", "新能源车牌", "白色", "黑色-港澳"]
    # 车牌粗定位
    images = detect.detectPlateRough(image, image.shape[0], top_bottom_padding_rate=0.1)

    for img in images:
        x2, y2, w2, h2 = img[1]
        # 绘制一个黑色矩形覆盖找到的车牌区域以免重复识别
        cv2.rectangle(image, (int(x2), int(y2)), (int(x2 + w2), int(y2 + h2)), (0, 0, 0), -1, 1)

    angles = [-12, 12, -24, 24, -36, 36, -48, 48, -60, 60]

    imageH, imageW, imageM = image.shape
    for ang in angles:
        image_1 = rotate_bound(image, ang)
        images_1 = detect.detectPlateRough(image_1, image_1.shape[0], top_bottom_padding_rate=0.1, angle=ang)
        for img in images_1:
            # img[0] = jiaozheng.correct(img[0])
            # print("ANG:::::::", ang, "\tPoint:", img[1])
            # print("IMAGE SHAPE:", imgW, imgH)
            X, Y, W, H = img[1]
            print("ANGLE=", ang)
            if ang >= 0:
                ang = ang * math.pi / 180
                hc = imageH * math.cos(ang)
                if hc >= Y:
                    x1 = (X - (hc - Y) * math.tan(ang)) * math.cos(ang)
                    y1 = imageH - (X - x1 / math.cos(ang)) / math.sin(ang) - x1 * math.tan(ang)
                    # cv2.circle(image, (int(x1), int(y1)), 20, (0, 0, 255), -1)
                    print("矫正后点的位置:", x1, y1)

                else:
                    yhc = Y - hc
                    alpha = math.atan(yhc / X)
                    beta = ang - alpha
                    L = math.sqrt(yhc ** 2 + X ** 2)
                    x1 = L * math.cos(beta)
                    y1 = imageH - L * math.sin(beta)
                    # cv2.circle(image, (int(x1), int(y1)), 20, (0, 0, 255), -1)
                    print("矫正后点的位置:", x1, y1)

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
                    # cv2.circle(image, (int(x1), int(y1)), 20, (0, 0, 255), -1)
                    print("矫正后点的位置:", x1, y1)

                else:
                    yhc = Y - hc
                    alpha = math.atan(yhc / X)
                    beta = ang - alpha
                    L = math.sqrt(yhc ** 2 + X ** 2)
                    y1 = L * math.cos(beta)
                    x1 = imageW - L * math.sin(beta)
                    x1 = imageW - x1
                    # cv2.circle(image, (int(x1), int(y1)), 20, (0, 0, 255), -1)
                    print("矫正后点的位置:", x1, y1)

                x2 = x1 - H * math.sin(ang)
                y2 = y1
                w2 = H * math.cos(ang) + W * math.sin(ang)
                h2 = H * math.sin(ang) + W * math.cos(ang)

                img[1] = [x2, y2, w2, h2]
            images.append(img)
            # 绘制一个黑色矩形
            cv2.rectangle(image, (int(x2), int(y2)), (int(x2 + w2), int(y2 + h2)), (0, 0, 0), -1, 1)

    print("LEN:", len(images))
    time_crop = time.time() - t
    if len(images) > 0:
        time_crop /= len(images)

    res_set = []    # 结果列表
    con_set = []    # 置信度列表
    time_set = []   # 耗时列表
    color = []      # 颜色列表
    for j, plate in enumerate(images):
        t0 = time.time()
        plate, rect, origin_plate = plate

        plate = cv2.resize(plate, (136, 36 * 2))
        t1 = time.time()

        res = td.SimplePredict(plate)

        ptype = res.argmax()

        print(plateType[ptype])

        if ptype > 0 and ptype < 5:
            plate = cv2.bitwise_not(plate)

        image_rgb = fm.findContoursAndDrawBoundingBox(plate)

        image_rgb = fv.finemappingVertical(image_rgb)

        cache.verticalMappingToFolder(image_rgb)
        print("e2e:", e2e.recognizeOne(image_rgb))
        image_gray = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2GRAY)

        image_gray = horizontalSegmentation(image_gray)

        print("校正", time.time() - t1, "s")

        t2 = time.time()
        if plateType[ptype] == "新能源车牌":
            val = segmentation.slidingWindowsEval_1(image_gray)
        else:
            val = segmentation.slidingWindowsEval(image_gray)
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
                time_set.append(str(time.time() - t0 + time_crop) + " s")
                image_new = drawRectBox(image_new, rect, res + "-" + color_1)
                res_set.append(res)
                con_set.append(confidence)

                print("Res:", res)
                print("Ptype:", ptype)

                color.append(color_1)

                print("color:", color)

            if confidence > 0:
                print("车牌:", res, "置信度:", confidence)

    print(time.time() - t, "s")
    return image_new, res_set, con_set, time_set, color


if __name__ == '__main__':

    # file_path = r"D:\python\python_work\cnsoftbei_2\pic_test\038.jpg"
    file_path = "D:/python/python_work/cnsoftbei_1/test-imgs-piliang/003.jpg"

    image = cv2.imread(file_path)

    imgHight, imgWidth, imgMode = image.shape
    H = int(imgHight * 0.5)
    W = int(imgWidth * 0.5)

    image = cv2.resize(image, (W, H))

    # cv2.imshow("step1", image)

    # result = SimpleRecognizePlate_1(image)
    result = SimpleRecognizePlate(image)

    # 图片缩放，便于观察处理效果
    imgHight, imgWidth, imgMode = result[0].shape
    H = int(imgHight * 1)
    W = int(imgWidth * 1)

    img = cv2.resize(result[0], (W, H))

    W, H, M = img.shape
    img_1 = cv2.resize(img, (int(H/3), int(W/3)))
    # cv2.imshow("Result", img_1)

    print("****************************************************")
    print("Result:", result[1], result[2], result[4])
    print("****************************************************")
    cv2.waitKey(0)
