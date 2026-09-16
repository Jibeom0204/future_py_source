# cgi-bin/.py : 웹용 파이썬 클라이언트에서 전송한 값 수신
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

## ->
#서버(Backend)에서 실행되어 데이터를 처리하기 위한 코드
#CGI(Common Gateway Interface) 규격에 따르면, 브라우저(클라이언트)가
# 파이썬 스크립트(friend.py)를 요청하면 웹 서버가 이 파이썬 파일을 직접 실행함.
#이 파이썬 코드는 frien.html로 생성된 창에서
# 사용자가 보낸 데이터(이름, 전화번호 등)를 읽어들여 연산을 수행한 뒤,
#최종적으로 브라우저가 인식할 수 있는 순수한 HTML 문자열을 생성하여 반환(print)하는 역할

#==================

print("Contet-Type:text/html; charset=utf-8") # 파이썬에서 html 실행가능 한 형식
#get post 방식 둘다 가능한 방식. 어떻게 선택하냐?
# GET 방식을 선택할 때:
# friend.HTML 파일에서 <form action="cgi-bin/my.py" method="get">으로
# 작성하거나 method 속성을 지우면 됩니다.
# 이 경우 파이썬 코드의 else 블록이 실행됩니다.

# POST 방식을 선택할 때:
# HTML에서 <form action="cgi-bin/my.py" method="post">로 수정하여 전송.
# 이 경우 파이썬 코드의 if method == "POST": 블록이 실행됩니다.

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
.format(irum,junhwa,gen))