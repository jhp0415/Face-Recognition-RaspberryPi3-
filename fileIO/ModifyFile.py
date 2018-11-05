#-*- coding:utf-8 -*-
# ModifyFile.py

import face_recognition
import os
import numpy as np

encoding_filename = "face_encoding_file.txt"

if __name__ == '__main__':
    known_face_encodings = []
    known_face_names = []
    person = []     # 디렉토리에 있는 인물들
    noData = []     # 새로 인코딩 해야할 사람 저장

    # knowns 폴더의 파일들 목록 가져오기
    # .jpg 확장자인 파일들만 따로 추출
    print("AWS knowns 디렉토리 파일 읽어오기")
    filepath = './knowns'
    files = os.listdir(filepath)
    for file in files:
        if file.endswith('.jpg'):
            s = os.path.splitext(file)
            s = os.path.split(s[0])
            person.append(s[1])

    # 인코딩 파일에서 인물 이름 검색하기
    print("인코딩 파일 읽어오기, 이름 검색하기")
    if os.path.isfile(encoding_filename):
        # 있으면 파일 열어서 읽어오기, 존재하는 인물 이름들 추출.
        f = open(encoding_filename, "rb")
        lines = f.readlines()
        for i in range(0, len(lines)):
            line = lines[i].decode()
            if "name:" in line:
                name = line[len("name:"):-1]
                known_face_names.append(name)
                i += 129
                #print("%s 가 인코딩 파일안에 존재합니다." %name)


    # 디렉토리에는 있는데 인코딩 파일에는 저장되지 않는 사람 구하기
    for name in person:
        if name not in known_face_names:
            noData.append(name)
            print("%s이 디렉토리에는 있지만, 인코딩은 되지 않았습니다." %name)


    # 인물 이름과 인코딩 데이터 파일 끝에 추가하기
    # 없으면 그 인물 인코딩
    f = open(encoding_filename, "ab")
    dirname = 'knowns'
    files = os.listdir(dirname)
    for name in noData:
        known_face_names.append(name)
        pathname = os.path.join(dirname, name + '.jpg')
        img = face_recognition.load_image_file(pathname)
        face_encoding = face_recognition.face_encodings(img)[0]
        # print(face_encoding)
        known_face_encodings.append(face_encoding)

        # 파일에 이름+인코딩 데이터 추가
        f.write(('name:' + name + "\n").encode())  # 이진데이터 변환
        # 얼굴 인코딩 데이터 저장
        np.savetxt(f, face_encoding, delimiter=", ")
        print('%s 저장 완료' %name)

    f.close()



