# cgi-bin/my.py : 웹용 파이썬 클라이언트에서 전송한 값 수신
import sys
sys.stdout.reconfigure(encoding='utf-8')  # 한글 깨짐 방지

import os
import urllib.parse

#get/post 요청구분
method = os.environ.get("REQUEST_METHOD", "GET")

if method =="POST": 
    length = int(os.environ.get("CONTENT_LENGTH",0))
    body = sys.stdin.read(length)
else:
    body = os.environ.get("QUERY_STRING","")

params=urllib.parse.parse_qs(body)
irum = params.get("name",[""])[0]
junhwa = params.get("phone",[""])[0]
gen = params.get("gen",[""])[0]
# 여기작성된 코드는 파이썬에서 작성된 부분이라 브라우저에서 인식이 안됨
#그럼 이 파이썬 코드의 의미는 뭐임?
#==================

print("Contet-Type:text/html; charset=utf-8") # 파이썬에서 html 실행가능 한 형식
#get post 방식 둘다
#아래에는 작성된 HTML
print("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>friend</title>
</head>
<body>
    <b>친구정보**<b>
    <br/>
    일반 사용자가 전송한 값: 이름은 {0}, 전화는 {1}, 성별은{2}
    <br/>
    <a href="../index.html">메인으로</a>

</body>
</html>"""
.format(irum,junhwa,gen)) #이름0 전화1 성별2로 받은 값이 format에 저장??