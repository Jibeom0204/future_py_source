"""
Flas app의 Entry Point
라우팅 서버 실행 담당

Jinja2: Flask에서 html을 동적으로 렌더링 할 때 사용하는 템플릿 엔진
웹 서버에서 html문을 완성한 후 클라이언트 전송
html안에 파이썬 변수를 넣고 반복/조건문 등을 사용할 수 있게 해주는 도구

render templete : html 템플릿 파일(Jinja2 템플릿)을 읽어 필요한 값을
채운 후 완성된 html을 응답으로 반환해주는 함수
"""

from flask import Flask, render_template

app =Flask(__name__);
@app.route("/")#methods=["GET","POST"] 명시 안하면 기본이 get 방식
def home():
    return render_template("home.html");

@app.route("/hello")   # 데코레이터: "/hello" 주소로 요청이 오면 아래 함수를 실행하라는 등록표
def hi():
    name = "길동이"      # 그냥 파이썬 지역 변수. 아직 HTML과 아무 관계 없음
    addr ="서초구 서초2동 132";
    return render_template("hello.html",name=name,juso=addr)
#render_temple의 인자 들
#hello.html: templates/ 폴더 기준 상대 경로
#name=name,juso=addr: 왼쪽 = 템플릿 안에서 쓸 이름, 오른쪽 = 파이썬 변수템플릿은 왼쪽 이름만 안다
#hello.html에 name과 juso라는 변수에 값을 넣어 전달.

@app.route("/world")
def world_image():
    return render_template("/my.html")

if __name__=='__main__':
    app.run(debug=True,host='0.0.0.0',port=5000);