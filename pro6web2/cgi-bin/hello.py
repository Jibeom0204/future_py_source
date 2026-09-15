#cgi-bin/hello.py
import sys
sys.stdout.reconfigure(encoding='utf-8') #한글패치

ss = '파이썬 자료 출력' # 파이썬 실행문
# print(ss) 개발자가 자신의 컴 표준 출력장치로 값 출력
ss2=123+200 # 파이썬 실행문

######################################################################
# 사용자가 브라우저에서 <a href="cgi-bin/hello.py"> 링크를 클릭하면
# 웹 서버는 파이썬 인터프리터를 구동하여 hello.py 코드를 실행함

# 파일의 소스 코드가 브라우저로 전송되는 것이 아니라
# hello.py 내부의 print() 함수 등을 통해 생성된 출력물(일반적으로 HTML 구조의 텍스트)이 
# 브라우저로 전송됩니다.
######################################################################


# 클라이언트 브라우저로 파이썬 처리값 출력
print("Content-Type:text/html; charset=utf-8")
print()
print("<html>")
print("<body>")
print("<h2> 파이썬 문서의 자료 출력/h2>")
print(f"파이썬 변수 값1:{ss}<br/>")
print(f"파이썬 변수 값2:{ss2}<br/>")
print("<body>")
print("<html>")