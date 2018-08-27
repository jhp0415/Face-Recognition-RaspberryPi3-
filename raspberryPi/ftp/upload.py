import requests
import os

try:
    url = "http://ec2-54-180-31-52.ap-northeast-2.compute.amazonaws.com:8080/face/"
    files = {'myfile': open('stream.jpg', 'rb')}
    values = {'name': 'stream.jpg', 'type': 'image', 'size': os.path.getsize('stream.jpg') }
    r = requests.post(url, files=files, data=values)
    print(r.text)

except Exception as e:
    print("error: ", e)