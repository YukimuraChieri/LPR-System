
import cv2
import numpy as np


# CascadeClassifier：级联滤波器
watch_cascade = cv2.CascadeClassifier('./model/cascade.xml')


# 判断是否在图像范围内
def computeSafeRegion(shape, bounding_rect):
    top = bounding_rect[1]      # y
    bottom = bounding_rect[1] + bounding_rect[3]    # y+h
    left = bounding_rect[0]     # x
    right = bounding_rect[0] + bounding_rect[2]     # x+w

    min_top = 0
    max_bottom = shape[0]
    min_left = 0
    max_right = shape[1]

    # print("computeSateRegion input shape",shape)
    if top < min_top:
        top = min_top
        # print("tap top 0")
    if left < min_left:
        left = min_left
        # print("tap left 0")

    if bottom > max_bottom:
        bottom = max_bottom
        # print("tap max_bottom max")
    if right > max_right:
        right = max_right
        # print("tap max_right max")

    # print("corr",left,top,right,bottom)
    return [left, top, right-left, bottom-top]


# 从图片中截取指定区域
def cropped_from_image(image, rect):
    x, y, w, h = computeSafeRegion(image.shape,rect)
    return image[y:y+h, x:x+w]


def detectPlateRough(image_gray, resize_h=720, en_scale=1.08, top_bottom_padding_rate=0.05, angle=0):
    # 打印图像形状
    print("image_gray.shape:", image_gray.shape)
    # top_bottom_padding_rate 上下填充率
    if top_bottom_padding_rate > 0.2:     # 如果大于0.2则打印错误警告并退出
        print("error:top_bottom_padding_rate > 0.2:", top_bottom_padding_rate)
        exit(1)

    height = image_gray.shape[0]    # 图像高度
    padding = int(height*top_bottom_padding_rate)   # 填充：高度*上下填充率
    scale = image_gray.shape[1]/float(image_gray.shape[0])  # scale：宽/高

    image = cv2.resize(image_gray, (int(scale*resize_h), resize_h))     # 图像缩放，宽度为scale*resize_h=(width/hight)*resize_h
    image_color_cropped = image[padding:resize_h-padding, 0:image_gray.shape[1]]  # 图像裁剪：去掉上下区域

    image_gray = cv2.cvtColor(image_color_cropped, cv2.COLOR_RGB2GRAY)   # 图像灰度化

    W, H = image_gray.shape
    image_gray_1 = cv2.resize(image_gray, (int(H / 3), int(W / 3)))
    # cv2.imshow("step2_1", image_gray_1)
    # cv2.waitKey(0)

    watches = watch_cascade.detectMultiScale(image_gray, en_scale, 2, minSize=(36, 9), maxSize=(36*40, 9*40))

    cropped_images = []     # 创建一个空列表
    for (x, y, w, h) in watches:
        print(x, y, w, h)
        # cv2.rectangle(image_color_cropped, (x, y), (x + w, y + h), (0, 255, 0), 2)
        # cv2.imshow("img1", image_color_cropped)
        # cv2.waitKey(0)

        # 初始截取区域
        cropped_origin = cropped_from_image(image_color_cropped, (int(x), int(y), int(w), int(h)))

        W, H, M = cropped_origin.shape
        cropped_origin_1 = cv2.resize(cropped_origin, (int(H*2), int(W*2)))
        # cv2.imshow("step2_2", cropped_origin_1)
        # cv2.waitKey(0)

        # 适当扩大检测到的区域
        if angle < 10:
            x -= w * 0.14
            w += w * 0.28
            y -= h * 0.6
            h += h * 1.1
        elif abs(angle) < 20:
            x -= w * 0.14
            w += w * 0.28
            y -= h * 0.7
            h += h * 1.4
        elif abs(angle) < 30:
            x -= w * 0.14
            w += w * 0.28
            y -= h * 0.8
            h += h * 1.6
        else:
            x -= w * 0.15
            w += w * 0.30
            y -= h * 0.9
            h += h * 1.8

        # 截取扩大后的区域
        cropped = cropped_from_image(image_color_cropped, (int(x), int(y), int(w), int(h)))

        W, H, M = cropped.shape
        cropped_1 = cv2.resize(cropped_origin, (int(H * 2), int(W * 2)))
        # cv2.imshow("step2_3", cropped_1)
        # cv2.waitKey(0)
        # 将截取区域信息添加在列表cropped_images中
        cropped_images.append([cropped, [x, y+padding, w, h], cropped_origin])
    return cropped_images
