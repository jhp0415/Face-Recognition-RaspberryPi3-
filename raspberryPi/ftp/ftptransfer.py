import ftplib

ftp = ftplib.FTP("ec2-54-180-31-52.ap-northeast-2.compute.amazonaws.com")
ftp.login("root", "root")       # root 계정 로그인하기
#ftp.cwd("/home/ubuntu/ftp")     # 파일 저장할 경로
ftp.cwd("/var/www/html/face/uploads")
filename = "stream.jpg"
myfile = open(filename, 'rb')   # 파일 경로
ftp.storbinary("STOR " + filename, myfile)
myfile.close()
ftp.close()

'''
ftp = ftplib.FTP("ec2-54-180-31-52.ap-northeast-2.compute.amazonaws.com")
ftp.login("root", "root")       # root 계정 로그인하기
ftp.cwd("/home/ubuntu/ftp")     # 파일 저장할 경로
filename = "stream.jpg"
#myfile = open(filename, 'rb')   # 파일 경로
ftp.storbinary("STOR " + filename, open(filename, 'rb'))
#.close()
ftp.close()
'''