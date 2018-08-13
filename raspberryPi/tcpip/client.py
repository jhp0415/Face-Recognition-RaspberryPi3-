#-*- coding:utf-8 -*-
import os
import sys
import socket
import struct

import tcpip.message
from tcpip.message import Message

from tcpip.message_header import Header
from tcpip.message_body import BodyData
from tcpip.message_body import BodyRequest
from tcpip.message_body import BodyResponse
from tcpip.message_body import BodyResult

from tcpip.message_util import MessageUtil

CHUNK_SIZE = 4096

if __name__ == '__main__':
    '''
    if len(sys.argv) < 3:
        print("사용법 : {0} <Server IP> <File Path>".
              format(sys.argv[0]))
        sys.exit(0)
    
    serverIp = sys.argv[1]      # 전송할 서버 IP주소
    serverPort = 9000           # AWS TCP Port 주소
    filepath = sys.argv[2]      # 전송하고자 할 파일의 주소
    '''
    serverIp = "127.0.0.1"      # 전송할 서버 IP주소
    serverPort = 9000           # AWS TCP Port 주소
    filedir = "C:\\Users\\jh_p0\\Desktop\\network\\sample"
    filenames = [f for f in os.listdir(filedir) if f.endswith(".jpg")]

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # TCP 소켓을 생성한다.

    try:
        print("서버:{0}/{1}".format(serverIp, serverPort))

        sock.connect((serverIp, serverPort))  # 접속 요청을 수락한다.

        for filename in filenames:
            filepath = os.path.join(filedir, filename)
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

            MessageUtil.send(sock, reqMsg)  # 클라이언트는 서버와 연결 되자마자 파일 전송 요청 메세지를 보낸다.
            rspMsg = MessageUtil.receive(sock)  # 그리고 서버의 응답을 받는다.

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
                if filesize < CHUNK_SIZE:
                    fragmented = tcpip.message.NOT_FRAGMENTED
                else:
                    fragmented = tcpip.message.FRAGMENTED

                while totalRead < filesize:
                    rbytes = file.read(CHUNK_SIZE)
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

                    MessageUtil.send(sock, fileMsg)

                print()

                rstMsg = MessageUtil.receive(sock)  # 서버에서 파일을 제대로 받았는지에 대한 응답을 받는다.

                result = rstMsg.Body
                print("파일 전송 성공 : {0}".
                      format(result.RESULT == tcpip.message.SUCCESS))

    except Exception as err:
        print("예외가 발생했습니다.")
        print(err)

    sock.close()
    print("클라이언트를 종료합니다.")