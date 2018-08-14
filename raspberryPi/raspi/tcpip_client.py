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

class TCPIPClient(Thread, Frame):
    def __init__(self):
        Thread.__init__(self)

        self.serverIp = "ec2-13-124-248-96.ap-northeast-2.compute.amazonaws.com"  # 전송할 서버 IP주소
        self.serverPort = 9000  # AWS TCP Port 주소
        self.filedir = os.path.join(Frame.PATH, Frame.dir_name)  # 전송하고자 할 파일이 있는 디렉토리 경로



        self.CHUNK_SIZE = 4096
        self.connetionFlag = False

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # TCP 소켓을 생성한다.
        print("tcpip_client : 서버:{0}/{1}".format(self.serverIp, self.serverPort))
        self.sock.connect((self.serverIp, self.serverPort))  # 접속 요청을 수락한다.


    def SendFile(self, filepath):
        try:
            print("SendFile : 함수 실행")
            msgId = 0

            reqMsg = Message()
            filesize = os.path.getsize(filepath)
            reqMsg.Body = BodyRequest(None)
            reqMsg.Body.FILESIZE = filesize
            reqMsg.Body.FILENAME = filepath[filepath.rindex('\\') + 1:]

            msgId += 1
            reqMsg.Header = Header(None)
            reqMsg.Header.MSGID = msgId
            reqMsg.Header.MSGTYPE = tcpip.message.REQ_FILE_SEND
            reqMsg.Header.BODYLEN = reqMsg.Body.GetSize()
            reqMsg.Header.FRAGMENTED = tcpip.message.NOT_FRAGMENTED
            reqMsg.Header.LASTMSG = tcpip.message.LASTMSG
            reqMsg.Header.SEQ = 0

            MessageUtil.send(self.sock, reqMsg)  # 클라이언트는 서버와 연결 되자마자 파일 전송 요청 메세지를 보낸다.
            rspMsg = MessageUtil.receive(self.sock)  # 그리고 서버의 응답을 받는다.

            if rspMsg.Header.MSGTYPE != tcpip.message.REP_FILE_SEND:
                print("정상적인 서버 응답이 아닙니다.{0}".
                      format(rspMsg.Header.MSGTYPE))
                exit(0)

            if rspMsg.Body.RESPONSE == tcpip.message.DENIED:
                print("서버에서 파일 전송을 거부했습니다.")
                exit(0)

            ###
            with open(filepath, 'rb') as file:  # 서버에서 전송 요청을 수락했다면, 파일을 열어 서버로 보낼 준비를 한다.
                totalRead = 0
                msgSeq = 0  # ushort
                fragmented = 0  # byte
                if filesize < self.CHUNK_SIZE:
                    fragmented = tcpip.message.NOT_FRAGMENTED
                else:
                    fragmented = tcpip.message.FRAGMENTED

                while totalRead < filesize:
                    rbytes = file.read(self.CHUNK_SIZE)
                    totalRead += len(rbytes)

                    fileMsg = Message()
                    fileMsg.Body = BodyData(rbytes)  # 모든 파일의 내용이 전송될 때까지 파일을 0x03 메세지에 담아 서버로 보낸다.

                    header = Header(None)
                    header.MSGID = msgId
                    header.MSGTYPE = tcpip.message.FILE_SEND_DATA
                    header.BODYLEN = fileMsg.Body.GetSize()
                    header.FRAGMENTED = fragmented
                    if totalRead < filesize:
                        header.LASTMSG = tcpip.message.NOT_LASTMSG
                    else:
                        header.LASTMSG = tcpip.message.LASTMSG

                    header.SEQ = msgSeq
                    msgSeq += 1

                    fileMsg.Header = header
                    print("#", end='')

                    MessageUtil.send(self.sock, fileMsg)

                print()

                rstMsg = MessageUtil.receive(self.sock)  # 서버에서 파일을 제대로 받았는지에 대한 응답을 받는다.

                result = rstMsg.Body
                print("파일 전송 성공 : {0}".
                      format(result.RESULT == tcpip.message.SUCCESS))


        except Exception as err:
            print("sendFile : 예외가 발생했습니다.")
            print(err)


    def DeleteFile(self):
        filelist = [f for f in os.listdir(self.filedir) if f.endswith(".jpg")]
        for f in filelist:
            os.remove(os.path.join(self.filedir, f))
        print("manage_file : %s 내의 모든 파일을 삭제하였습니다." %(self.filedir))


    def run(self):
        try:
            while(True):
                while(Frame.faceFull):
                    lock.acquire()  # 락 설정
                    print("run : 서버 전송 함수 시작")
                    filenames = os.listdir(self.filedir)
                    for filename in filenames:      # 디렉토리 내의 모든 파일 서버에 전송하기
                        fpath = os.path.join(self.filedir, filename)
                        self.SendFile(fpath)  # 파일 1개 전송
                    print("%s 내의 모든 파일을 전송 완료했습니다." % ( Frame.dir_name ))

                    self.DeleteFile()       # 디렉토리 내의 모든 파일 삭제하기
                    print("%s 내의 모든 파일을 삭제 완료했습니다." % ( Frame.dir_name ))
                    print()
                    Frame.sendSuccess = True
                    Frame.faceFull = False
                    lock.release()  # 락 해제

        except Exception as err:
            print("run : 파일을 전송하는 도중 예외가 발생했습니다.")
            print("tcpip run e: ", err)
