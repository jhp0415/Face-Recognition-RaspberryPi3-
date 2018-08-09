#-*- coding:utf-8 -*-
# face_detection.py

import cv2
from threading import Thread, Lock
import time

from frame import Frame

lock = Lock()       # 공유 변수 제어하기

class FaceDetection(Thread, Frame):
    def __init__(self):
        Thread.__init__(self)

        # Import the face detection haar file, 오픈시비 얼굴인식 사용
        # haarcascade_ㅇㅇㅇ.xml 파일의 경로를 적절히 바꿔줘야 한다.


        # 라즈베리파이에서의 경로
        self.face_cascade = cv2.CascadeClassifier("/home/pi/opencv/opencv-3.4.0/data/haarcascades/haarcascade_frontalface_alt.xml")
        self.eye_cascade = cv2.CascadeClassifier("/home/pi/opencv/opencv-3.4.0/data/haarcascades/haarcascade_eye.xml")

        '''
        # 윈도우에서의 경로
        self.face_cascade = cv2.CascadeClassifier(
            "C:/opencv/build/etc/haarcascades/haarcascade_frontalface_alt.xml")
        self.eye_cascade = cv2.CascadeClassifier("C:/opencv/build/etc/haarcascades/haarcascade_eye.xml")
        '''

        print("face_detection __init__")


    def IsFace(self, buffer):       # 카메라가 촬영한 프레임 속에 얼굴이 있는지 없는지 판단하기
        self.gray = cv2.cvtColor(buffer, cv2.COLOR_BGR2GRAY)
        self.faces = self.face_cascade.detectMultiScale(self.gray, 2, 5)  # 얼굴 찾기
        if (len(self.faces) > 0):
            Frame.faceFound = True  # 얼굴이 있다!
            return Frame.faceFound
        else:
            Frame.faceFound = False
            return Frame.faceFound


    def FindFace(self, buffer):     # 프레임안에 얼굴을 표시하는 사각형 그리기
        if (self.faceFound):  # 프레임안에 얼굴이 존재할 때
            for idx, (x, y, w, h) in enumerate(self.faces):
                cv2.rectangle(buffer, (x, y), (x + w, y + h), (255, 0, 0), 2)  # 얼굴 사각형 그리기
                roi_gray = self.gray[y:y + h, x:x + w]
                roi_color = buffer[y:y + h, x:x + w]
                '''
                eyes = self.eye_cascade.detectMultiScale(roi_gray, 2, 5)
                for eidx, (ex, ey, ew, eh) in enumerate(eyes):      # 눈 그리기
                    cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 0, 255), 2)  # 눈 사각형 그리기
                '''
        # 사각형을 그린 프레임 반환
        return buffer


    def run(self):
        try:
            time.sleep(3)
            while (True):
                lock.acquire()      # 락 설정

                if(self.IsFace(Frame.frame)):
                    print("face_detection : 프레임에 얼굴을 표시합니다.")
                    Frame.frame = self.FindFace(Frame.frame)
                else:       # 얼굴이 없다
                    print("face_detection : There is no Face")

                lock.release()      # 락 해제

        except Exception as e:
            print("face_detection e: ", e)




