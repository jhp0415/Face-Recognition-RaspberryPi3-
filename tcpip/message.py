#-*- coding:utf-8 -*-
'''
헤더와 바디의 두 부분으로 나누니다. 바디에는 실제로 저달하고자 하는 데이터를 담고,
헤더에는 본문 길이를 비롯해 메세지의 속성 몇 가지를 담는다.
바디의 길이는 담는 데이터에 따라 달라지지만, 헤더의 길이는 16바이트로 항상 일정하다.

수신한 패킷을 분석할 때는 가장 먼저 16바이트를 먼저 확인해서 (바디의 전체 길이 포함하여) 메세지의 속성을 확인하고,
그 다음에 바디의 길이 만큼을 또 읽어 하나의 메세지 끝을 끊어내야 한다.
'''

# 메세지 타입 상수 정의
REQ_FILE_SEND = 0x01    # 요청 메세지 타입
REP_FILE_SEND = 0x02    # 응답 메세지 타입
FILE_SEND_DATA = 0x03   # 전송 파일
FILE_SEND_RES = 0x04    # 전송 완료 메세지


NOT_FRAGMENTED = 0x00   # 파일의 분할 여부를 상수로 정의
FRAGMENTED = 0x01

NOT_LASTMSG = 0x00      # 분할된 메세지의 마지막 여부 상수 정의
LASTMSG = 0x01

ACCEPTED = 0x00         # 파일의 전송 수락 여부를 상수로 정의
DENIED = 0x01

FAIL = 0x00             # 파일 전송의 성공 여부를 상수 정의
SUCCESS = 0x01


    # 메세지, 헤더, 바디는 모두 이 클래스를 상속한다.
    # 즉, 이들은 자신의 데이터를 바이트 배열로 변환하고, 그 바이트 배열의 크기를 반환해야 한다.
class ISerializable:
    def GetBytes(self):
        pass

    def GetSize(self):
        pass


''''''

    # 기본 메세지 형식
class Message(ISerializable):
    def __init__(self):
        self.Header = ISerializable()
        self.Body = ISerializable()

    # ISerializable 클래스로 부터 상속받은 메서드, overriding
    def GetBytes(self):
        buffer = bytes(self.GetSize())      # 네트워크 데이터 전송은 bytes 형태로.

        header = self.Header.GetBytes()
        body = self.Body.GetBytes()

        return header + body

    # 메세지의 헤더길이 + 바디길이 = 메세지의 전체 길이
    def GetSize(self):
        return self.Header.GetSize() + self.Body.GetSize()
