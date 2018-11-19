#-*- coding:utf-8 -*-
# face_recog_main.py

from face_recog_threading import FaceRecog

# 메인 동작
if __name__ == '__main__':
    # 객체 생성
    ob_face1 = FaceRecog('1')       # 얼굴을 detection하는 서브 스레드
    ob_face2 = FaceRecog('2')  # 얼굴을 detection하는 서브 스레드
    ob_face3 = FaceRecog('3')  # 얼굴을 detection하는 서브 스레드
    print("객체 생성 완료")

    try:
        print("main : 카메라 동작 및 워크 스레드를 실행합니다.")

        ob_face1.start()
        ob_face2.start()
        ob_face3.start()

        ob_face1.join()       # 스레드가 종료될 때 까지 메인 스레드가 대기하게 한다.
        ob_face2.join()
        ob_face3.join()

    except Exception as err:
        print("main e : ", err)

    print("모든 동작을 종료 합니다.")
