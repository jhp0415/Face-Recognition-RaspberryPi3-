#-*- coding:utf-8 -*-
# face_recog.py

import face_recognition
import cv2
#import camera
import os
import numpy as np

encoding_filename = "face_encoding_file.txt"

class FaceRecog():
    def __init__(self):
        # Using OpenCV to capture from device 0. If you have trouble capturing
        # from a webcam, comment the line below out and use a video file
        # instead.

        #self.camera = camera.VideoCamera()


        self.known_face_encodings = []
        self.known_face_names = []

        # 맨처음 실행할때 파일 생성하기, 이미 파일이 존재하면 실행 안하기
        if os.path.isfile(encoding_filename):
            # 있으면 파일 열어서 읽어오기
            f = open(encoding_filename, "rb")

            while True:
                name = f.readline().decode()
                if not name:
                    print("txt 파일 끝까지 읽기 완료")
                    break
                name = name[len('name:') : -1]
                self.known_face_names.append(name)
                #print(name)

                # 얼굴 인코딩 데이터 읽어오기
                datas = []
                for i in range(0, 128):
                    data = f.readline().decode().split("\n")
                    datas.append(float(data[0]))
                face_encoding = np.array(datas)
                datas.clear()
                self.known_face_encodings.append(face_encoding)
                #print(face_encoding)

        else:
            # 없으면 파일을 만들고, 파일에 인코딩 데이터 저장하기
            f = open(encoding_filename, "wb")

            # Load sample pictures and learn how to recognize it.
            dirname = 'knowns'
            files = os.listdir(dirname)
            for filename in files:
                name, ext = os.path.splitext(filename)
                if ext == '.jpg':
                    self.known_face_names.append(name)
                    pathname = os.path.join(dirname, filename)
                    img = face_recognition.load_image_file(pathname)
                    face_encoding = face_recognition.face_encodings(img)[0]
                    # print(face_encoding)
                    self.known_face_encodings.append(face_encoding)

                    print("%s 저장하기" %name)
                    # 파일에 이름+인코딩 데이터 저장
                    f.write(('name:' + name + "\n").encode())     #이진데이터 변환
                    # 얼굴 인코딩 데이터 저장
                    np.savetxt(f, face_encoding, delimiter=", ")
            print("인코딩 완료")
            f.close()

        # Initialize some variables
        self.face_locations = []
        self.face_encodings = []
        self.face_names = []
        self.process_this_frame = True

    #def __del__(self):
        #del self.camera

    def get_frame(self, frame):
        # Grab a single frame of video
        #frame = self.camera.get_frame()
        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Only process every other frame of video to save time
        if self.process_this_frame:
            # Find all the faces and face encodings in the current frame of video
            self.face_locations = face_recognition.face_locations(rgb_small_frame)
            self.face_encodings = face_recognition.face_encodings(rgb_small_frame, self.face_locations)

            self.face_names = []
            for face_encoding in self.face_encodings:
                # See if the face is a match for the known face(s)
                distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
                min_value = min(distances)

                # tolerance: How much distance between faces to consider it a match. Lower is more strict.
                # 0.6 is typical best performance.
                name = "Unknown"
                if min_value < 0.6:
                    index = np.argmin(distances)
                    name = self.known_face_names[index]

                self.face_names.append(name)

        self.process_this_frame = not self.process_this_frame

        # Display the results
        for (top, right, bottom, left), name in zip(self.face_locations, self.face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        return frame


    def get_jpg_bytes(self):
        frame = self.get_frame()
        # We are using Motion JPEG, but OpenCV defaults to capture raw images,
        # so we must encode it into JPEG in order to correctly display the
        # video stream.
        ret, jpg = cv2.imencode('.jpg', frame)
        return jpg.tobytes()


if __name__ == '__main__':
    face_recog1 = FaceRecog()
    face_recog2 = FaceRecog()
    face_recog3 = FaceRecog()
    frame1 = None
    frame2 = None
    frame3 = None
    while True:
        frame1 = cv2.imread("ftp/stream1.jpg")        # 이미지 읽어오기
        frame2 = cv2.imread("ftp/stream2.jpg")
        frame3 = cv2.imread("ftp/stream3.jpg")
        if (frame1 is None) or (frame2 is None) or (frame3 is None):   # 이미지 읽는 타이밍이 안좋았으면 다시 처음부터
            continue

        frame1 = face_recog1.get_frame(frame1)
        frame2 = face_recog2.get_frame(frame2)
        frame3 = face_recog3.get_frame(frame3)

        # 얼굴인식한 이미지 저장하기
        filename1 = 'stream1.jpg'
        filename2 = "stream2.jpg"
        filename3 = "stream3.jpg"
        filepath = "/var/www/cgi-bin/data/"    # 웹 경로에 저장하기
        file1 = os.path.join(filepath, filename1)  # 경로 + 파일 이름 + 확장자 (리눅스 버전)
        file2 = os.path.join(filepath, filename2)  # 경로 + 파일 이름 + 확장자 (리눅스 버전)
        file3 = os.path.join(filepath, filename3)  # 경로 + 파일 이름 + 확장자 (리눅스 버전)
        cv2.imwrite(file1, frame1)  # 이미지 저장
        cv2.imwrite(file2, frame2)  # 이미지 저장
        cv2.imwrite(file3, frame3)  # 이미지 저장
        print(filepath + "에 파일 저장 완료")

    print('finish')
