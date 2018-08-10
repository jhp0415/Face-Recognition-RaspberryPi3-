#-*- coding:utf-8 -*-
import socket

import tcpip.message
from tcpip.message import Message
from tcpip.message_header import Header       #메시지 헤더. 파일의 길이, 속성 등의 정보
from tcpip.message_body import BodyData       #메시지 몸통. 파일의 본문 내용
from tcpip.message_body import BodyRequest    #전송 요청 메시지
from tcpip.message_body import BodyResponse   #전송 응답 메시지
from tcpip.message_body import BodyResult     #파일 전송 결과 메시지


class MessageUtil:
    @staticmethod
    def send(sock, msg):    # send() 메소드는 msg 매개변수가 담고 있는 모든 바이트를 내보낼 때까지 반복해서 socket.send() 메소드를 호출한다.
        sent = 0
        buffer = msg.GetBytes()
        while sent < msg.GetSize():
            sent += sock.send(buffer)


    @staticmethod
    def receive(sock):
        totalRecv = 0       #
        sizeToRead = 16     # 헤더의 크기(고정, 16 byte)
        hBuffer = bytes()   # 헤더 버퍼

        # 16 byte 크기만큼 버퍼 읽기 ==> 헤더 읽기
        while sizeToRead > 0:   # 첫 반복문에서는 스트림으로부터 메세지 헤더의 경계를 끊어낸다. (헤더 | 바디)
            buffer = sock.recv(sizeToRead)
            if len(buffer) == 0:
                return None

            hBuffer += buffer           # 읽은 데이터
            totalRecv += len(buffer)    # 총 읽은 데이터 길이
            sizeToRead -= len(buffer)

        header = Header(hBuffer)    # 헤더 데이터 파싱하기

        totalRecv = 0
        bBuffer = bytes()   # 바디 버퍼
        sizeToRead = header.BODYLEN     # 바디의 총 길이


        # 바디 읽기
        while sizeToRead > 0:   # 첫 반복문에서 얻은 헤더에서 본문의 길이를 뽑아내어 그 길이만큼 다시 스트림으로부터 본문을 읽는다.
            buffer = sock.recv(sizeToRead)
            if len(buffer) == 0:
                return None

            bBuffer += buffer
            totalRecv += len(buffer)
            sizeToRead -= len(buffer)

        body = None

        if header.MSGTYPE == tcpip.message.REQ_FILE_SEND:
            body = BodyRequest(bBuffer)
        elif header.MSGTYPE == tcpip.message.REP_FILE_SEND:
            body = BodyResponse(bBuffer)
        elif header.MSGTYPE == tcpip.message.FILE_SEND_DATA:
            body = BodyData(bBuffer)
        elif header.MSGTYPE == tcpip.message.FILE_SEND_RES:
            body = BodyResult(bBuffer)
        else:
            raise Exception(
                "Unknown MSGTYPE : {0}".format(header.MSGTYPE))

        # 읽은 데이터 메세지 한 개
        msg = Message()
        msg.Header = header
        msg.Body = body


        return msg


