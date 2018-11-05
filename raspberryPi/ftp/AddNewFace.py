#-*- coding:utf-8 -*-
# AddNewFace.py

import cv2
import time, os
import ftplib

def get_frame(v):
    # Grab a single frame of video
    ret, frame = v.read()
    return frame

if __name__ == '__main__':
    video = cv2.VideoCapture(0)

    ftp = ftplib.FTP("ec2-54-180-31-52.ap-northeast-2.compute.amazonaws.com")
    ftp.login("root", "root")  # root 계정 로그인하기
    ftp.cwd("/home/ubuntu/knowns")     # 파일 저장할 경로

    while (True):
        frame = get_frame(video)
        time.sleep(0.1)  # 영상에서 프레임에 그린 사각형을 보기위해 sleep 걸기
        cv2.imshow("Frame", frame)  # show the frame
        key = cv2.waitKey(1) & 0xFF

        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            break
        elif key == ord("c"):

            # 이미지 저장
            filename = input("저장할 파일 이름을 입력하세요 : ")
            filepath = "./data"
            file = os.path.join(filepath, filename)  # 경로 + 파일 이름 + 확장자 (리눅스 버전)
            cv2.imwrite(file, frame)  # 이미지 저장
            print("PC에 : %s 파일을 저장했습니다." % (filename))

            # ftp 전송
            myfile = open(os.path.join(filepath, filename), 'rb')  # 파일 경로
            ftp.storbinary("STOR " + filename, myfile)

    video.release()
    myfile.close()
    ftp.close()