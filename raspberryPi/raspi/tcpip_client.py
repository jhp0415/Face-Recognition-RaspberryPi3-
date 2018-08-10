#-*- coding:utf-8 -*-

import os, sys, time
import socket
from threading import Thread, Lock

from raspi.frame import Frame

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import tcpip.message
from tcpip.message import Message
from tcpip.message_header import Header
from tcpip.message_body import BodyData
from tcpip.message_body import BodyRequest
from tcpip.message_body import BodyResponse
from tcpip.message_body import BodyResult
from tcpip.message_util import MessageUtil


lock = Lock()

class TCPIPClient():
    def __init__(self):
        self.serverIp = "ec2-13-124-248-96.ap-northeast-2.compute.amazonaws.com"  # 전송할 서버 IP주소
        self.serverPort = 9000  # AWS TCP Port 주소
        self.filepath = Frame.PATH + "\\" + Frame.dir_name  # 전송하고자 할 파일이 있는 디렉토리 경로
        self.CHUNK_SIZE = 4096
        self.connetionFlag = False

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # TCP 소켓을 생성한다.
        print("tcpip_client : 서버:{0}/{1}".format(self.serverIp, self.serverPort))
        self.sock.connect((self.serverIp, self.serverPort))  # 접속 요청을 수락한다.



    def InitMessage(self, path):

        self.msgId = 0


        print("InitMessage : 서버에 접속을 요청합니다.")
        self.reqMsg = Message()
        self.filesize = os.path.getsize(path)

        self.reqMsg.Body = BodyRequest(None)
        self.reqMsg.Body.FILESIZE = self.filesize
        self.reqMsg.Body.FILENAME = path[path.rindex('\\') + 1:]

        self.msgId += 1
        self.reqMsg.Header = Header(None)
        self.reqMsg.Header.MSGID = self.msgId
        self.reqMsg.Header.MSGTYPE = tcpip.message.REQ_FILE_SEND
        self.reqMsg.Header.BODYLEN = self.reqMsg.Body.GetSize()
        self.reqMsg.Header.FRAGMENTED = tcpip.message.NOT_FRAGMENTED
        self.reqMsg.Header.LASTMSG = tcpip.message.LASTMSG
        self.reqMsg.Header.SEQ = 0


    def RequestConnection(self):
        print("RequestConnection : 서버에 파일 전송을 요청합니다..")
        MessageUtil.send(self.sock, self.reqMsg)  # 클라이언트는 서버와 연결 되자마자 파일 전송 요청 메세지를 보낸다.
        self.rspMsg = MessageUtil.receive(self.sock)  # 그리고 서버의 응답을 받는다.

        if self.rspMsg.Header.MSGTYPE != tcpip.message.REP_FILE_SEND:
            print("정상적인 서버 응답이 아닙니다.{0}".
                  format(self.rspMsg.Header.MSGTYPE))
            exit(0)

        if self.rspMsg.Body.RESPONSE == tcpip.message.DENIED:
            print("서버에서 파일 전송을 거부했습니다.")
            exit(0)

        return True


    def SendFile(self, buffer):
        try:
            print("SendFile : 함수 실행")
            with open(buffer, 'rb') as file:  # 서버에서 전송 요청을 수락했다면, 파일을 열어 서버로 보낼 준비를 한다.
                self.totalRead = 0
                self.msgSeq = 0  # ushort
                self.fragmented = 0  # byte

                if self.filesize < self.CHUNK_SIZE:
                    self.fragmented = tcpip.message.NOT_FRAGMENTED
                else:
                    self.fragmented = tcpip.message.FRAGMENTED

                while self.totalRead < self.filesize:
                    self.rbytes = file.read(self.CHUNK_SIZE)
                    self.totalRead += len(self.rbytes)

                    self.fileMsg = Message()
                    self.fileMsg.Body = BodyData(self.rbytes)  # 모든 파일의 내용이 전송될 때까지 파일을 0x03 메세지에 담아 서버로 보낸다.

                    self.header = Header(None)
                    self.header.MSGID = self.msgId
                    self.header.MSGTYPE = tcpip.message.FILE_SEND_DATA
                    self.header.BODYLEN = self.fileMsg.Body.GetSize()
                    self.header.FRAGMENTED = self.fragmented
                    if self.totalRead < self.filesize:
                        self.header.LASTMSG = tcpip.message.NOT_LASTMSG
                    else:
                        self.header.LASTMSG = tcpip.message.LASTMSG

                    self.header.SEQ = self.msgSeq
                    self.msgSeq += 1

                    self.fileMsg.Header = self.header
                    print("#", end='')

                    MessageUtil.send(self.sock, self.fileMsg)

                print()

                self.rstMsg = MessageUtil.receive(self.sock)  # 서버에서 파일을 제대로 받았는지에 대한 응답을 받는다.

                self.result = self.rstMsg.Body
                print("파일 전송 성공 : {0}".
                      format(self.result.RESULT == tcpip.message.SUCCESS))

        except Exception as err:
            print("sendFile : 예외가 발생했습니다.")
            print(err)



    def run(self):
        try:
            print("run : 서버 전송 함수 시작")
            lock.acquire()  # 락 설정

            paths = os.listdir(self.filepath)
            for path in paths:      # 디렉토리 내의 모든 파일 리스트
                fpath = self.filepath + "\\" + path
                self.InitMessage(fpath)
                self.connetionFlag = self.RequestConnection()
                if (self.connetionFlag):
                    self.SendFile(fpath)  # 파일 1개 전송
                    self.connetionFlag = False

            print("%s 내의 모든 파일을 전송 완료하였습니다." % (self.filepath))
            print()

            lock.release()      # 락 해제
            return True

        except Exception as err:
            print("run : 파일을 전송하는 도중 예외가 발생했습니다.")
            print(err)
