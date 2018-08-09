#-*- coding:utf-8 -*-

from pi_camera.array import PiRGBArray
from pi_camera import PiCamera

import cv2
from threading import Thread, Lock
import time
import copy

from frame import Frame

lock = Lock()

class VideoCamera(Thread, Frame):
    def __init__(self):
        Thread.__init__(self)

        # Used in Screen resolution and positioning later
        widths = 480
        heights = 320

        # initialize the camera and grab a reference to the raw camera capture
        self.camera = PiCamera()
        self.camera.resolution = (widths, heights)
        self.camera.framerate = 32
        self.camera.hflip = True
        self.rawCapture = PiRGBArray(self.camera, size=(widths, heights))


        # allow the camera to warmup
        time.sleep(0.1)

        #cv2.namedWindow('VideoOutput')
        print("video_camera __init__")


    def run(self):
        # Main Loop
        try:
            while (True):
                # capture frames from the camera
                for image in self.camera.capture_continuous(self.rawCapture, format="bgr", use_video_port=True):
                    #print("run 함수 실행")
                    lock.acquire()  # 락 설정
                    Frame.frame = image.array  # 카메라 촬영한 영상에서 프레임 추출
                    Frame.copy = copy.copy(Frame.frame)
                    lock.release()  # 락 해제

                    time.sleep(0.1)  # 영상에서 프레임에 그린 사각형을 보기위해 sleep 걸기

                    # Output the video, 비디오 출력하기
                    lock.acquire()  # 락 설정
                    cv2.imshow('VideoOutput', Frame.frame)
                    lock.release()  # 락 해제

                    # clear the stream in preparation for the next frame
                    self.rawCapture.truncate(0)

                    # Check for keypresses
                    key = cv2.waitKey(1) & 0xFF

                    if key == ord("q"):
                        print("Q Pressed")
                        break

                cv2.destroyAllWindows()

        except Exception as err:
            print(err)





