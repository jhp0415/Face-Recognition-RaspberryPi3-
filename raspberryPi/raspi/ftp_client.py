#-*- coding:utf-8 -*-

import ftplib
import os, sys, time
import socket
from threading import Thread, Lock

from raspi.frame import Frame

lock = Lock()

class FTPClient(Thread, Frame):
    def __init__(self):
        Thread.__init__(self)

        self.ftp = ftplib.FTP("ec2-54-180-31-52.ap-northeast-2.compute.amazonaws.com")
        self.ftp.login("root", "root")  # root 계정 로그인하기
        # ftp.cwd("/home/ubuntu/ftp")     # 파일 저장할 경로
        self.ftp.cwd("/var/www/html/face/uploads")
        self.filename = "stream.jpg"
        self.filedir = os.path.join(Frame.PATH, Frame.dir_name)  # 전송하고자 할 파일이 있는 디렉토리 경로


    def SendFile(self, filepath):
        self.myfile = open(os.path.join(self.filedir, self.filename), 'rb')  # 파일 경로
        self.ftp.storbinary("STOR " + self.filename, self.myfile)


    def run(self):
        try:
            while (True):
                while (Frame.faceFull):
                    lock.acquire()  # 락 설정
                    print("run : 서버 전송 함수 시작")
                    filenames = os.listdir(self.filedir)
                    for filename in filenames:  # 디렉토리 내의 모든 파일 서버에 전송하기
                        fpath = os.path.join(self.filedir, filename)
                        self.SendFile(fpath)  # 파일 1개 전송
                    print("%s 내의 모든 파일을 전송 완료했습니다." % (Frame.dir_name))

                    print()
                    Frame.sendSuccess = True
                    Frame.faceFull = False
                    lock.release()  # 락 해제

        except Exception as err:
            print("run : 파일을 전송하는 도중 예외가 발생했습니다.")
            print("ftp run e: ", err)

        finally:
            self.myfile.close()
            self.ftp.close()