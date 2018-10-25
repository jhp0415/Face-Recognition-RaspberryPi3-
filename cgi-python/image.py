#!/usr/bin/python3

# 일단 성공
import sys, time
import os
import cgi
from datetime import datetime

form = cgi.FieldStorage()

if 'id' in form:
   pageId = form["id"].value
   src = './data/stream' + pageId + '.jpg'
else:
    pageId = '1'

#src = './data/stream1.jpg'

while(True):
    sys.stdout.write("Content-Type: image/jpg\n")
    sys.stdout.write("Content-Length: " + str(os.stat(src).st_size) + "\n")
    sys.stdout.write("\n")
    sys.stdout.flush()
    sys.stdout.buffer.write(open(src, "rb").read())
    time.sleep(500)

