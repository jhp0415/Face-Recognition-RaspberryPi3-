# -*- coding:utf-8 -*-
# PiCamera.py

import picamera
import time, os
import ftplib

class VideoCamera():
    RPin = None
    camera = None
    rawCapture = None
    ftp = None
    file = None
    filename = None

    def __init__(self, num):
        self.RPin = num  # 라즈베리파이 번호
        # ftp 설정하기
        self.ftp = ftplib.FTP("ec2-54-180-31-52.ap-northeast-2.compute.amazonaws.com")
        self.ftp.login("root", "root")  # root 계정 로그인하기
        self.ftp.cwd("/home/ubuntu/ftp")  # 파일 저장할 경로
        self.filename = 'stream%s.jpg' % self.RPin
        filepath = "./data"
        self.file = os.path.join(filepath, self.filename)  # 경로 + 파일 이름 + 확장자 (리눅스 버전)


if __name__ == '__main__':

    rpi = VideoCamera(3)

    while (True):
        with picamera.PiCamera() as camera:
            # camera.resolution = (640, 480)
            # camera.start_preview()
            # time.sleep(1)
            camera.resolution = (640, 480)
            camera.capture(rpi.file)  # 이미지 저장

            # camera.stop_preview()

            # 서버에 ftp 전송하기

            myfile = open(rpi.file, 'rb')  # 파일 경로
            rpi.ftp.storbinary("STOR " + rpi.filename, myfile)
            print("서버에 %s 사진을 전송하였습니다." % rpi.filename)

    myfile.close()
    rpi.ftp.close()