#-*- coding:utf-8 -*-

import os

class Frame():
    frame = None                # 영상으로 찍은 프레임. 모든 스레드에서 공유할 공유변수이다.
    copy = None                 # 영상으로 보여줄 원본 카피

    faceMax = 5
    faceFull = False            # 디렉토리 안에 사진이 다 찼는지 flag
    fcount = 0                  # 프레임이 100장 모이면 파일 전송, 그 후 저장된 파일 모두 삭제하기

    faceFound = False           # 프레임에서 얼굴을 찾았는지 못 찾았는지 flag
    sendSuccess = False

    PATH = os.getcwd()          # 현재 작업 디렉토리 경로
    dir_name = "data"               # 사진을 저장할 디렉토리 이름