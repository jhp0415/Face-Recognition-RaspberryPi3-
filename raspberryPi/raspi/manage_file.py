#-*- coding:utf-8 -*-
# manage_file.py

import os
import sys
import cv2
from threading import Thread, Lock
import time
from datetime import datetime

from raspi.frame import Frame
from raspi.tcpip_client import TCPIPClient


lock = Lock()

class ManageFile(Thread, Frame):
    def __init__(self, buffer):
        Thread.__init__(self)
        self.client = buffer
        # 디렉토리 형성하기
        self.dir_name = Frame.dir_name
        self.upload_dir = Frame.PATH + "/" + self.dir_name      # 리눅스 용
        #self.upload_dir = Frame.PATH + "\\" + self.dir_name    # 사용자가 데이터를 저장하기 원하는 디렉토리 경로 입력받기(윈도우는 \\, 리눅스는 /)
        if os.path.isdir(self.upload_dir) == False:       # 디렉토리 존재 여부, 없으면?
            os.mkdir(self.upload_dir)  # 디렉토리 생성


    def GetDatatime(self):
        now = datetime.now()
        # 년-월-일_시-분-초
        self.data = "{0}-{1}-{2}_{3}-{4}-{5}".format(now.year, now.month, now.day, now.hour, now.minute, now.second)
        print(self.data)
        return self.data


    def SavaFile(self):
        filename = self.GetDatatime() + ".jpg"  # 저장할 파일 이름 정하기. 현재 시간 + count index
        #file = self.upload_dir + "\\" + filename  # 경로 + 파일 이름 + 확장자 (윈도우 버전)
        file = self.upload_dir + "/" + filename  # 경로 + 파일 이름 + 확장자 (리눅스 버전)

        cv2.imwrite(file, Frame.copy)  # 이미지 저장

        print("manage_file : %s 파일을 저장했습니다." %(filename))
        return True



    def DeleteFile(self):
        filelist = [f for f in os.listdir(self.upload_dir) if f.endswith(".jpg")]
        for f in filelist:
            os.remove(os.path.join(self.upload_dir, f))
        print("manage_file : %s 내의 모든 파일을 삭제하였습니다." %(self.upload_dir))


    def run(self):
        try:
            time.sleep(3)
            while(True):
                lock.acquire()  # 락 설정
                if(Frame.faceFound):        # 3초 간격으로 프레임을 디렉토리에 저장한다. (적절한 시간은 3초)
                    self.SavaFile()
                    Frame.fcount += 1
                    if (Frame.fcount == Frame.faceMax):
                        Frame.faceFull = True
                        #lock.release()  # 락 잠시 해제
                        while Frame.sendSuccess is not True:        # True가 될때까지 무한루프
                            #print("manage_file 대기 중...")
                            pass

                        Frame.sendSuccess = False       # 초기화
                        Frame.fcount = 0
                lock.release()  # 락 해제
                time.sleep(2)

        except Exception as e:
            print("manage_file e : ", e)

