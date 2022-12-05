import pipline
import cv2
import os
import time
import math

os.system("color 0b")
# 视频文件
# file_path = r"C:\Users\79936\PycharmProjects\cnsoftbei\file_7.mp4"
save_path = r"D:\cnsoftbeiresult\shipin\pic_save"


def mkdir(path):
    folder = os.path.exists(path)

    if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(path)  # makedirs 创建文件时如果路径不存在会创建这个路径
        print("---  new folder...  ---")
        print("---  OK  ---")
    else:
        print("---  There is this folder!  ---")


mkdir(save_path)


def shipin(download_path2):

    file_path = download_path2

    cap = cv2.VideoCapture(file_path)

    ret, frame = cap.read()

    # 图片缩放，缩小原始数据量，加快处理速度
    imgHight, imgWidth, imgMode = frame.shape

    area = imgHight * imgWidth
    print(area)

    if area > 600000:
        ratio = math.sqrt(area / 600000)
        H = int(imgHight / ratio)
        W = int(imgWidth / ratio)
    else:
        H = int(imgHight)
        W = int(imgWidth)

    while True:

        ret, frame = cap.read()
        if frame is None:
            break

        frame = cv2.resize(frame, (W, H))  # 原图
        img, results, confidence, time_set, color = pipline.SimpleRecognizePlate(frame)
        cv2.imshow("result", img)
        keyval = cv2.waitKey(2) & 0xFF
        if keyval == ord(' '):
            listStr = [str(int(time.time())), str(0)]  # 以时间戳和读取的排序作为文件名称
            fileName = ''.join(listStr)
            cv2.imwrite(save_path + os.sep + '%s.jpg' % fileName, img)
            print("Save OK")
        elif keyval == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
