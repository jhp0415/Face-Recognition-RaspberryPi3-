#!/usr/bin/python3
# -*- coding:utf-8 -*-

print("Content-Type: text/html")  # 웹서버가 동작할때 꼭 알려줘야되는 정보, Header
print()  # 한줄을 꼭 띄어줘야 한다.

print('''<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>CBNU</title>

  <script>
    var newImage1 = new Image();
    newImage1.src = "image.py?id=1";
    var newImage2 = new Image();
    newImage2.src = "image.py?id=2";
     var newImage3 = new Image();
    newImage3.src = "image.py?id=3";

    function updateImage()
    {
      if(newImage1.complete)
      {
        newImage1.src = "image.py?id=1&" + new Date().getTime(); 
        document.getElementById("img1").src = newImage1.src;
      }
      if(newImage2.complete)
      { 
        newImage2.src = "image.py?id=2&" + new Date().getTime();
        document.getElementById("img2").src = newImage2.src;
      }
      if(newImage3.complete)
      { 
        newImage3.src = "image.py?id=3&" + new Date().getTime();
        document.getElementById("img3").src = newImage2.src;
      }
      var dt = new Date();  
      var elem = document.getElementById("msg");  
      elem.textContent = dt.toTimeString();  

      setTimeout(updateImage, 500);
    }

  </script>

</head>


<body onload = "updateImage()">
    <h1>Face Recognition based Position Detction</h1>
    <h3>Park Jeong-Hyeon, Lee Sang-Min</h3>
    <h3>professor: Kang Hyeon-Su</h3>

  <div id="main">
    <div id="posImg1" style="float:left;width:30%;">
        <p>1</p><br>
        <img id="img1" src="" alt="image1" width="400">
        <p id="text"></p>
        <p>IP : 111111</p><br>
        <p>position: school</p><br>
    </div>

    <div id="posImg2" style="float:left;width:30%;">
        <p>2</p><br>
        <img id="img2" src="" alt="image2" width="400">
        <p>IP : 2222222</p><br>
        <p>position: home</p><br>
    </div>
    
    <div id="posImg3" style="float:left;width:30%;">
        <p>3</p><br>
        <img id="img3" src="" alt="image3" width="400">
        <p>IP : 33333333</p><br>
        <p>position: Lab</p><br>
    </div>

  <textarea id="msg" ></textarea>

  </div>
</body>
</html>
''')
