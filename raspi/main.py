#-*- coding:utf-8 -*-

#from picamera.array import PiRGBArray      # 라즈베리파이 카메라
#from picamera import PiCamera

import os
import cv2                                  # 파이썬 기본 모듈
import time

from frame import Frame                     # 사용자 정의 클래스
#from WebCam import VideoCamera
from video_camera import VideoCamera
from face_detection import FaceDetection
from manage_file import ManageFile

'''
라즈베리파이가 파이카메라를 사용하여 촬영을 시작한다.
촬영 영상에서 사람의 얼굴을 포착하는 경우 해당 프레임을 디렉토리에 저장한다. 
추후 저장된 프레임 영상은 서버로 전송될 예정이다.
'''


    # 메인 동작
if __name__ == '__main__':

    # 객체 생성
    ob_camera = VideoCamera()       # 영상을 촬영하는 메인 스레드
    ob_face = FaceDetection()       # 얼굴을 detection하는 서브 스레드
    ob_file = ManageFile()            # 프레임을 저장하는 서브 스레드

    try:
        print("카메라 동작 및 워크 스레드를 실행합니다.")

        ob_camera.start()      # 쓰레드 실행
        time.sleep(2)
        ob_face.start()
        ob_file.start()

        ob_camera.join()       # 스레드가 종료될 때 까지 메인 스레드가 대기하게 한다.
        ob_face.join()
        ob_file.join()

    except Exception as err:
        print(err)

    print("모든 동작을 종료 합니다.")
