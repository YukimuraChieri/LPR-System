import pipline
import cv2
import os
import time
import pyttsx3
import addsql

os.system("color 0b")

save_path = r"D:\cnsoftbeiresult\shexiangtou\pic_save"


def mkdir(path):
    folder = os.path.exists(path)

    if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(path)  # makedirs 创建文件时如果路径不存在会创建这个路径
        print("---  new folder...  ---")
        print("---  OK  ---")
    else:
        print("---  There is this folder!  ---")


def jiankong():
    mkdir(save_path)
    test = pyttsx3.init()
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        img, results, confidence, time_set, color = pipline.SimpleRecognizePlate(frame)
        cv2.imshow("result", img)

        for i, res in enumerate(results):
            if not addsql.db_search_text(res):
                pass

        if results:
            pass

        keyval = cv2.waitKey(2) & 0xFF
        if keyval == ord(' '):  # 按空格存
            listStr = [str(int(time.time())), str(0)]  # 以时间戳和读取的排序作为文件名称
            fileName = ''.join(listStr)
            cv2.imwrite(save_path + os.sep + '%s.jpg' % fileName, img)
            print("Save OK")
        elif keyval == ord('s'):
            test.setProperty('rate', 150)
            test.say(results)
            test.runAndWait()
        elif keyval == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
