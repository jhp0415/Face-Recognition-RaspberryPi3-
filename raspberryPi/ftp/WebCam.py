#-*- coding:utf-8 -*-
# WebCam.py

import cv2
from threading import Thread, Lock
import time, os
import ftplib


lock = Lock()

def get_frame(v):
    # Grab a single frame of video
    ret, frame = v.read()
    return frame

if __name__ == '__main__':
    video = cv2.VideoCapture(0)
    video2 = cv2.VideoCapture(1)

    ftp = ftplib.FTP("ec2-54-180-31-52.ap-northeast-2.compute.amazonaws.com")
    ftp.login("root", "root")  # root 계정 로그인하기
    ftp.cwd("/home/ubuntu/ftp")     # 파일 저장할 경로
    #ftp.cwd("/var/www/html/face/uploads")

    while (True):
        frame = get_frame(video)
        frame2 = get_frame(video2)

        # 이미지 저장
        filename = 'stream.jpg'
        filename2 = "stream2.jpg"
        filepath = "./data"
        file = os.path.join(filepath, filename)  # 경로 + 파일 이름 + 확장자 (리눅스 버전)
        file2 = os.path.join(filepath, filename2)  # 경로 + 파일 이름 + 확장자 (리눅스 버전)
        cv2.imwrite(file, frame)  # 이미지 저장
        cv2.imwrite(file2, frame2)  # 이미지 저장
        print("manage_file : %s 파일을 저장했습니다." % (filename))

        # ftp 전송
        myfile = open(os.path.join(filepath, filename), 'rb')  # 파일 경로
        ftp.storbinary("STOR " + filename, myfile)
        myfile = open(os.path.join(filepath, filename2), 'rb')  # 파일 경로
        ftp.storbinary("STOR " + filename2, myfile)


        time.sleep(0.1)  # 영상에서 프레임에 그린 사각형을 보기위해 sleep 걸기
        cv2.imshow("Frame", frame)  # show the frame
        cv2.imshow("Frame2", frame2)  # show the frame
        key = cv2.waitKey(1) & 0xFF


        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            break

    video.release()
    video2.release()
    myfile.close()
    ftp.close()