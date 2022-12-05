import pipline
import addsql
import cv2
import os
import math


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


def mkdir(path):
    folder = os.path.exists(path)

    if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(path)  # makedirs 创建文件时如果路径不存在会创建这个路径
        print("---  new folder...  ---")
        print("---  OK  ---")
    else:
        print("---  There is this folder!  ---")


province = {
    "皖": "WAN",     "沪": "HU",     "津": "JINA",   "渝": "YUA",
    "吉": "JIB",     "晋": "JINB",   "蒙": "MENG",   "辽": "LIAO",
    "冀": "JIA",     "黑": "HEI",    "苏": "SU",     "浙": "ZHE",
    "京": "JING",    "闽": "MIN",    "赣": "GANA",   "鲁": "LU",
    "豫": "YUB",     "鄂": "E",      "湘": "XIANG",  "粤": "YUE",
    "贵": "GUIB",    "琼": "QIONG",  "川": "CHUAN",  "桂": "GUIA",
    "云": "YUN",     "藏": "ZANG",   "陕": "SHAN",   "甘": "GANB",
    "青": "QING",    "宁": "NING",   "新": "XIN"
  }


# 图片路径
# src_path = r"D:/CV/pic_data/"
# src_path = r"C:/test-imgs/"
#
# file_path = findAllfile(src_path)


def fun_danzhang(file):
    print(file)
    image = cv2.imread(file)
    if image is None:
        return None
    # 图片缩放，缩小原始数据量，加快处理速度
    imgHight, imgWidth, imgMode = image.shape

    area = imgHight * imgWidth
    print(area)

    # cv2.imshow("step1", image)

    if area > 1000000:       # 518400
        ratio = math.sqrt(area / 1000000)
        H = int(imgHight / ratio)
        W = int(imgWidth / ratio)
    else:
        H = int(imgHight)
        W = int(imgWidth)
    img = cv2.resize(image, (W, H))  # 原图缩放

    cv2.imshow("step2", img)

    img, results, confidence, haoshi, color = pipline.SimpleRecognizePlate(img)

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

    return img


def fun_piliang(download_path):

    src_path = download_path
    file_path = findAllfile(src_path+'/')
    mkdir("C:/test-results/")
    results_file = r"C:/test-results/No16926mresults.txt"

    with open(results_file, 'w') as file_object:
        file_object.write('')

    images = []
    print('file_path:', file_path)

    for n, file in enumerate(file_path):
        print(file)
        image = cv2.imread(file)
        if image is None:
            continue
            # 图片缩放，缩小原始数据量，加快处理速度
        imgHight, imgWidth, imgMode = image.shape

        area = imgHight * imgWidth
        print(area)

        if area > 518400:
            ratio = math.sqrt(area / 518400)
            H = int(imgHight / ratio)
            W = int(imgWidth / ratio)
        else:
            H = int(imgHight)
            W = int(imgWidth)
        img = cv2.resize(image, (W, H))  # 原图

        img, results, confidence, haoshi, color = pipline.SimpleRecognizePlate(img)

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
            if res[0] in province.keys():
                for j, ch in enumerate(province[res[0]]):
                    results[i].insert(j+1, ch)
                del results[i][0]

        with open(results_file, 'a') as file_object:
            file_object.write(file[:].lower()+'\n')
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

    return images


if __name__ == '__main__':

    file_path = "D:/python/python_work/cnsoftbei_1/test-imgs-piliang/005.PNG"
    # download_path = "D:/python/python_work/cnsoftbei_1/test-imgs-piliang"
    fun_danzhang(file_path)
    # fun_piliang(download_path)

    cv2.waitKey(0)

