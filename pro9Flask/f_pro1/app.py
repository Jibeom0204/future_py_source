#pip install flask
#pip install waitress
from flask import Flask # 웹서버(WAS, Appilcation 서버)생성에 필요
# 현재 WAS: py 프로그램 코드를 실행해서 요청을 처리하는 서버

# Flask 기본 웹서버는 실무용이 아님, 개발/학습용 => Light weigth Server
# 실무용 서버: gunicorn, waitress, Nginx...
from waitress import serve

app = Flask(__name__); # flask 객체 생성. 현재 모듈의 이름을 생성자에게 전달

@app.route("/") # URL 매핑(라우팅). 클라이언트 요청이 "/"일 때 아래의 함수를 실행
def abc(): # 클라이언트 요청을 처리하는 핸들러 함수
    return "<h2>안녕하세요</h2> ㅎㅇㅎㅇ" # 클라이언트 브라우저에 반환(전송)

@app.route("/about")
def about():
    return "플라스크 실습 중"

@app.route("/user/<name>")#URL에 변수의 값이 담긴 경우
def user(name):
    return f"f로 이름 받기{name}";

if __name__ == '__main__':
    #app.run() #run은 flask가 지원함 # 실습용 기본 서버로 서비스 실행
    # app.run(debug=False,host='0.0.0.0',port=5000); #의 코드의 실제 구조 # False는 어떤경우?
    
    #app.run(debug=Ture,host='0.0.0.0',port=5000); #개발할 때 debug는 True # 개인용, 실습용 방식


    # waitress사용 시
    print("웹 서버 서비스 중...")
    serve(app=app, host='0.0.0.0', port=8000);