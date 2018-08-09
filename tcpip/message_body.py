#-*- coding:utf-8 -*-
from message import ISerializable
import message
import struct


    # 파일 전송 요청 메세지(REQ_FILE_SEND = 0x01)에 사용할 본문 클래스이다.
    # FILESIZE와 FILENAME 데이터 속성을 갖는다.
    # Client가 사용할 예정
class BodyRequest(ISerializable):
    def __init__(self, buffer):
        if buffer != None:      # 바디에 데이터가 있는 경우
            slen = len(buffer)

            # 1 unsigned long long, N character
            self.struct_fmt = str.format('=Q{0}s', slen - 8)        # 바디 형식
            self.struct_len = struct.calcsize(self.struct_fmt)      # 바디 길이
            if slen > 4:    # unsigned long long 의 크기
                slen = slen - 4
            else:
                slen = 0

            unpacked = struct.unpack(self.struct_fmt, buffer)       # buffer 압축해제. 데이터 파싱할 예정

            self.FILESIZE = unpacked[0]
            self.FILENAME = unpacked[1].decode(encoding='utf-8').replace('\x00', '')    # 사용자 언어로 변환 ASCII-->str

        else:       # 바디에 아무런 데이터가 없을 경우
            self.struct_fmt = str.format('Q{0}s', 0)
            self.struct_len = struct.calcsize(self.struct_fmt)
            self.FILESIZE = 0
            self.FILENAME = ''

    # 바디 압축
    def GetBytes(self):
        buffer = self.FILENAME.encode(encoding='utf-8')     # str-->ASCII

        # 1 unsinged long long, N character
        self.struct_fmt = str.format('Q{0}s', len(buffer))

        return struct.pack(
            self.struct_fmt,
            *(
                self.FILESIZE,
                buffer
            ))

    # 바디의 길이
    def GetSize(self):
        buffer = self.FILENAME.encode(encoding='utf-8')

        # 1 unsigned long long, N character
        self.struct_fmt = str.format('=Q{0}s', len(buffer))
        self.struct_len = struct.calcsize(self.struct_fmt)
        return self.struct_len



    ################################################################################################################


    # 파일 전송 요청에 대한 응답 메시지(REP_FILE_SEND = 0x02)에 사용할 본문 클래스이다.
    # 요청 메세지의 MSGID와 수락 여부를 나타내는 RESPONSE 데이터 속성을 갖는다.
    # Server가 사용할 예정

class BodyResponse(ISerializable):
    def __init__(self, buffer):
        # 1 unsinged int, Byte
        self.struct_fmt = '=IB'
        self.struct_len = struct.calcsize(self.struct_fmt)

        if buffer != None:
            unpacked = struct.unpack(self.struct_fmt, buffer)       # buffer 압축 해제

            self.MSGID = unpacked[0]        # 메세지 구분 ID
            self.RESPONSE = unpacked[1]     # 요청 수락
        else:
            self.MSGID = 0
            self.RESPONSE = message.DENIED      # 파일 전송 거절

    def GetBytes(self):
        return struct.pack(
            self.struct_fmt,
            *(
                self.MSGID,
                self.RESPONSE
            ))

    def GetSize(self):
        return self.struct_len



    ###########################################################################################################


    # 실제 파일을 전송하는 메세지(FILE_SEND_DATA = 0x03)에 사용할 본문 클래스이다.
    # 앞서 프로토콜 정의에서 언급되었던 것처럼 DATA 필드만 갖고 있다.
class BodyData(ISerializable):
    def __init__(self, buffer):
        if buffer != None:
            self.DATA = buffer

    def GetBytes(self):
        return self.DATA

    def GetSize(self):
        return len(self.DATA)


    ##############################################################################################################


    # 파일 전송 결과 메세지, 메세지(FILE_SEND_RES = 0x04)에 사용할 본문 클래스이다.
    # 요청 메세지의 MSGID와 성공 여부를 나타내는 RESULT 데이터 속성을 갖는다.
class BodyResult(ISerializable):
    def __init__(self, buffer):
        # 1 unsigned int, Byte
        self.struct_fmt = '=IB'
        self.struct_len = struct.calcsize(self.struct_fmt)

        if buffer != None:      # 파일 전송 성공
            unpacked = struct.unpack(self.struct_fmt, buffer)
            self.MSGID = unpacked[0]
            self.RESULT = unpacked[1]

        else:       # 파일 전송 실패
            self.MSGID = 0
            self.RESULT = message.FAIL


    def GetBytes(self):
        return struct.pack(
            self.struct_fmt,
            *(
                self.MSGID,
                self.RESULT
            ))

    def GetSize(self):
        return self.struct_len







