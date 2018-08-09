#-*- coding:utf-8 -*-
from message import ISerializable
import struct

'''
struct 모듈 : 문자의 경우 bytes로 변환가능. 그러나, 숫자의 경우는 bytes(숫자)로 변경 불가능.
struct의 pack, unpack을 사용한다.
'''

    # 메세지 헤더에서 필요한 속성을 얻는다.
class Header(ISerializable):
    def __init__(self, buffer):
        self.struct_fmt = '=3I2BH'      # 헤더형식. 3 unsigned int, 2 byte, 1 unsigned short
        self.struct_len = struct.calcsize(self.struct_fmt)  # 헤더길이

        if buffer != None:
            unpacked = struct.unpack(self.struct_fmt, buffer)   # 데이터 파싱

            self.MSGID = unpacked[0]        # 메세지 구분 ID
            self.MSGTYPE = unpacked[1]      # 메세지 타입, 형식
            self.BODYLEN = unpacked[2]      # 본문(바디)의 길이
            self.FRAGMENTED = unpacked[3]   # 메세지 분할 여부
            self.LASTMSG = unpacked[4]      # 메세지의 끝 여부
            self.SEQ = unpacked[5]          # 순서 번호

    # 헤더 압축(메세지 속성들 모음)
    def GetBytes(self):
        return struct.pack(
            self.struct_fmt,
            *(
                self.MSGID,
                self.MSGTYPE,
                self.BODYLEN,
                self.FRAGMENTED,
                self.LASTMSG,
                self.SEQ
            ))

    # 헤더의 길이
    def GetSize(self):
        return self.struct_len
