from flask import Flask, render_template,render_template_string
from flask import request,make_response,redirect,url_for
#redirect: 브라우저를 다른 URL로 이동시키는(302) 리다이렉트 응답 생성
#url_for: 라우트 함수 이름으로 URL을 안전하게 생성
#render_template_string: 문자열로 작성한 Jinja 템플릿을 렌더링해 HTML로 반환하는 함수

app=Flask(__name__);

"""
쿠키는 브라우저에 저장되는 작은 키-값 데이터이고 서버가 클라이언트와 연결 상태를 유지하는 것처럼 할 수 있다
서버가 설정 -> 브라우저가 저장-> 다음 요청부터 브라우저가 자동으로 함께 전송
"""
#간단한 HTML: 텍스트로 작성
HOME_HTML = """
<h2>Flask Cookie test</h2>

<form action="/set_cookie" method="post">
    쿠키값: <input type="text" name="name" placeholder="예:hong">
    <button type="submit">쿠키 저장</button>
</form>

<p>
    <a href="/read_cookie">쿠키 읽기</a>
    <a href="/delete_cookie">쿠키삭제</a>
</p>
"""

# @app.route("/") #route는 get과 post를 둘다 받아서 안쪽에서 방식을 명시해줘야함. 애초에 구반할 수 있음
# def home():
#     # render_template_string(문자열): 문자열로 된 템플릿을 HTML로 변환해 반환
#     # 따옴표를 붙이면 문자열 "HOME_HTML" 자체가 되므로, 변수명만 적어야 변수의 내용이 전달됨
#     return render_template_string(HOME_HTML)

@app.get("/")
def home():
    return render_template_string(HOME_HTML)

@app.post("/set_cookie")
def set_cookie():
    # 쿠키저장
    user_send_name = request.form.get("name","anomymous")
    # 클라이언트에 쿠키를 심으려면 응다객체가 필요
    # 먼저 "read_coockie 페이지로 이동하라"는 redicrect 객체를 만들고
    # 그 응답에 따라 쿠키를 추가한 뒤 브라우저에 돌려줌

    # # resp = make_response(redirect("/read_cookie")) #클라이언트 url에서 /readcookie 처럼 쓰는것을 redirect 명령어로 서버단에서 아예 실행하기
    # 그러면 @app.get("/read_cookie") 이쪽으로 넘어가서 실행함.
    # 그런데 /readcookie 부분의 요청이 @app.get("/read_snak") 이런식 변경되면 이 코드를 계속 수정해줘야 하는데 너무 번거로움
    resp=make_response(redirect(url_for("read_cookie"))) # URL_for("함수명")
    # 이렇게 적으면 요청이 바뀌어도 같은 기능을 수행하게 됨

    # 정리
    # resp = make_response(redirect("/read_cookie"))
    # 이 방식으로 하면 @app.get("/read_cookie") 이쪽으로 넘어와서 def read_cookie()를 실행함
    # resp=make_response(redirect(url_for("read_cookie"))) # URL_for("함수명")
    # 이 방식으로 하면 def read_cookie()를 실행하고 결국에는 @app.get("/read_cookie") 이걸 수행하는 것임
    # 이 때 @app.get("/read_cookie")가 @app.get("/ppap")요청으로 클라이언트에서 변경되어도 
    # def read_cookie()을 수행하기에 상관이 없다.

    resp.set_cookie( # 브라우저에 쿠키저장
        key= "cookie_key_name", # 쿠키 이름
        value= user_send_name, # 사용자가 전송한 값을 쿠키에 저장
        max_age=60*5, # 유효시간 - 5분뒤 만료 일반적으로 1년. 파라미터 사용법이 초 단위?
        httponly=True, # JS에서 document.cookie로 접근 불가
        samesite="Lax" #  CSRF 공격(사이트간 요청 위조) 방지용
    )
    return resp
    # 쿠키가 포함된 응답을 브라우저로 반환
    # 브라우저는 쿠키를 저장하고, redirect 요청에 따라 read_cookie로 다시 요청함

@app.get("/read_cookie")
def read_cookie():
    # 브라우저가 요청에 실어보낸 모든 쿠키중에서 내 서버가 만든 쿠키(name)을 꺼냄
    # 만약 없으면 None을 반환(첫 방문/만료/삭제된 경우)

    recieve_name=request.cookies.get("cookie_key_name")

    # 읽은 쿠키 HTML로 출력
    return f"""
    <h3>쿠키 읽기</h3>
    <p>value 쿠키값: {recieve_name}</p>
    """

@app.get("/delete_cookie") #요청명
def delete_cookie(): #요청에 대한 함수의 이름
    # 쿠키 삭제 후 홈(/)으로 이동하기 위해 redirect로 
    resp=make_response(redirect(url_for("home"))) # 원래는 이런 방식 resp = make_response(redirect("/"))
    resp.delete_cookie("recieve_name") # 처리방식의 만들어진 메서드
    return resp

if __name__=='__main__':
    app.run(debug=True,host='0.0.0.0',port=5000);