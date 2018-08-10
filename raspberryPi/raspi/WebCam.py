#-*- coding:utf-8 -*-
# WebCam.py

import cv2
from threading import Thread, Lock
import time
import copy

from raspi.frame import Frame

lock = Lock()

class VideoCamera(Thread, Frame):
    def __init__(self):
        Thread.__init__(self)
        self.video = cv2.VideoCapture(0)


    def __del__(self):
        self.video.release()


    def get_frame(self):
        # Grab a single frame of video
        ret, Frame.frame = self.video.read()
        return Frame.frame

    def run(self):
        try:
            while(True):
                lock.acquire()      # 락 설정
                Frame.frame = self.get_frame()
                Frame.copy = copy.copy(Frame.frame)
                lock.release()      # 락 해제

                time.sleep(0.1)         # 영상에서 프레임에 그린 사각형을 보기위해 sleep 걸기

                lock.acquire()      # 락 설정
                cv2.imshow("Frame", Frame.frame)        # show the frame
                lock.release()      # 락 해제
                
                key = cv2.waitKey(1) & 0xFF

                # if the `q` key was pressed, break from the loop
                if key == ord("q"):
                    break

        except Exception as e:
            print("e: ", e)


