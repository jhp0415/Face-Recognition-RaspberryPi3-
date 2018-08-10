#-*- coding:utf-8 -*-
import os
import sys
import socket
import socketserver
import struct

import tcpip.message
from tcpip.message import Message      #주고 받는 메시지 (공통)

from tcpip.message_header import Header       #메시지 헤더. 파일의 길이, 속성 등의 정보
from tcpip.message_body import BodyData       #메시지 몸통. 파일의 본문 내용
from tcpip.message_body import BodyRequest    #전송 요청 메시지
from tcpip.message_body import BodyResponse   #전송 응답 메시지
from tcpip.message_body import BodyResult     #파일 전송 결과 메시지

from tcpip.message_util import MessageUtil

CHUNK_SIZE = 4096
upload_dir = ''


    # 소켓 통신으로 파일 전송 받기
class FileReceiveHandler(socketserver.BaseRequestHandler):
    def handle(self):
        print("클라이언트 접속 : {0}".format(self.client_address[0]))

        client = self.request

        reqMsg = MessageUtil.receive(client)    #클라이언트가 보내온 파일 전송 요청 메세지를 수신한다.

        if reqMsg.Header.MSGTYPE != tcpip.message.REQ_FILE_SEND:
            client.close()
            return

        reqBody = BodyRequest(None)


        print("파일 업로드 요청이 왔습니다.")

        # 나는 무조건 수락할 예정
        rspMsg = Message()
        rspMsg.Body = BodyResponse(None)
        rspMsg.Body.MSGID = reqMsg.Header.MSGID
        rspMsg.Body.RESPONSE = tcpip.message.ACCEPTED

        rspMsg.Header = Header(None)

        msgId = 0
        rspMsg.Header.MSGID = msgId
        msgId = msgId + 1
        rspMsg.Header.MSGTYPE = tcpip.message.REP_FILE_SEND
        rspMsg.Header.BODYLEN = rspMsg.Body.GetSize()
        rspMsg.Header.FRAGMENTED = tcpip.message.NOT_FRAGMENTED
        rspMsg.Header.LASTMSG = tcpip.message.LASTMSG
        rspMsg.Header.SEQ = 0

        MessageUtil.send(client, rspMsg)        # 클라이언트에게 '승낙' 응답을 보낸다.

        print("파일 전송을 시작합니다...")

        fileSize = reqMsg.Body.FILESIZE
        fileName = reqMsg.Body.FILENAME
        recvFileSize = 0

        with open(upload_dir + "/" + fileName, 'wb') as file:  # 업로드 받을 파일을 생성한다.
            dataMsgId = -1
            prevSeq = 0

            while True:
                reqMsg = MessageUtil.receive(client)
                if reqMsg == None:
                    break

                print("#", end='')

                if reqMsg.Header.MSGTYPE != tcpip.message.FILE_SEND_DATA:
                    break

                if dataMsgId == -1:
                    dataMsgId = reqMsg.Header.MSGID
                elif dataMsgId != reqMsg.Header.MSGID:
                    break

                if prevSeq != reqMsg.Header.SEQ:  # 메세지 순서가 어긋나면 전송을 중단한다.
                    print("{0}, {1}".format(prevSeq, reqMsg.Header.SEQ))
                    break

                prevSeq += 1

                recvFileSize += reqMsg.Body.GetSize()  # 전송받은 파일의 일부를 담고 있는 bytes 객체를 서버에서 생성한 파일에 기록한다.
                file.write(reqMsg.Body.GetBytes())

                if reqMsg.Header.LASTMSG == tcpip.message.LASTMSG:  # 마지막 메세지만 반복문을 빠져나온다.
                    break

            file.close()


            print()
            print("수신 파일 크기 : {0} bytes".format(recvFileSize))

            rstMsg = Message()
            rstMsg.Body = BodyResult(None)
            rstMsg.Body.MSGID = reqMsg.Header.MSGID
            rstMsg.Body.RESULT = tcpip.message.SUCCESS

            rstMsg.Header = Header(None)
            rstMsg.Header.MSGID = msgId
            msgId += 1
            rstMsg.Header.MSGTYPE = tcpip.message.FILE_SEND_RES
            rstMsg.Header.BODYLEN = rstMsg.Body.GetSize()
            rstMsg.Header.FRAGMENTED = tcpip.message.NOT_FRAGMENTED
            rstMsg.Header.LASTMSG = tcpip.message.LASTMSG
            rstMsg.Header.SEQ = 0

            if fileSize == recvFileSize:  # 파일 전송 요청에 담겨온 파일 크기와 실제로 받은 파일의 크기를 비교하여 같으면 성공 메세지를 보낸다.
                MessageUtil.send(client, rstMsg)
            else:
                rstMsg.Body = BodyResult(None)
                rstMsg.Body.MSGID = reqMsg.Header.MSGID
                rstMsg.Body.RESULT = tcpip.message.FAIL
                MessageUtil.send(client, rstMsg)  # 파일 크기에 이상이 있다면 실패 메세지를 보낸다.

        print("파일 전송을 마쳤습니다.")
        client.close()


    ############################################################################################################

    # server 메인 동작
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("사용법 : {0} <Directory>".format(sys.argv[0]))
        sys.exit(0)

    upload_dir = sys.argv[1]        # 사용자가 데이터를 저장하기 원하는 디렉토리 경로 입력받기
    if os.path.isdir(upload_dir) == False:      # 디렉토리 존재 여부, 없으면?
        os.mkdir(upload_dir)                    # 디렉토리 생성

    bindPort = 9000     # 나의 AWS Custom TCP Port Number
    server = None

    # 서버 스타트
    try:
        # 클라이언트 접속 요청을 처리한다.
        server = socketserver.TCPServer(
            ('', bindPort), FileReceiveHandler)     # 서버 핸들러 실행

        print("파일 업로드 서버 시작...")

        # 클라이언트의 접속 요청을 수신 대기한다.
        # 접속 요청이 있을 경우 수락하고 BaseRequestHandler의 handler() 메소드를 호출한다.
        server.serve_forever()

    except Exception as err:
        print(err)


    print("서버를 종료합니다.")
