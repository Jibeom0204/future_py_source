# cgi-bin/world.py : 웹용 파이썬
import sys
sys.stdout.reconfigure(encoding='utf-8')  # 한글 깨짐 방지

v1 = "자료1"
v2 = "두번째 자료"

print("Content-Type:text/html; charset=utf-8")
print("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>my</title>
</head>
<body>
    <b>my page</b> 
    <br>
    자료 출력:{0},{1}
    <br/>
    <img src="../images/image.jpeg" />
    <a href="../index.html">메인으로</a>    
</body>
</html>
""".format(v1, v2))

#b 굵게
#br 라인스킵
