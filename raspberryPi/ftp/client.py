import requests

#http://docs.python-requests.org/en/latest/user/quickstart/#post-a-multipart-encoded-file

url = "http://ec2-54-180-31-52.ap-northeast-2.compute.amazonaws.com:5000/"
fin = open('stream.jpg', 'rb')
files = {'file': fin}

try:
    r = requests.post(url, files=files)
    print (r.text)
finally:
	fin.close()