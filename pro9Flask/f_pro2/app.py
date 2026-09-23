from flask import Flask, request,make_response
# request: 현재 들어온 HTTP 요청 정보(파라미터, Form, Header, 쿠키..)를 담는 객체
# make_response: 응답(response) 객체를 직접 만들어 반환할 때 사용하는 함수

app =Flask(__name__);

@app.route("/")
def home():
    return "<h2>홈페이지</h2><p>/login으로 이동해보세요</p>"

@app.route("/login", methods=["GET","POST"]) #로그인 정보가 get 방식이든 post 방식이든 다 허용
def login():
    if request.method == "GET": # GET 요청이면 # 클라이언트에서 요청할 때 requset. 서버가 응답하면 respose
        return """
            <h2>로그인 페이지</h2>
            <form action="/login" method="post">
                <input type = "text" name="username" placeholder="사용자 이름 입력">
                <button type="submit">로그인</button>
            </form>
            
            <p>POST 요청 시 username 값을 서버가 받아 처리~</p>
            """
    elif request.method == "POST": # POST 요청이면
        user=request.form.get("username","").strip()
        # GET에서 <form>태그를 달아 전달해 주었기에 form의 정보를.get()하고 그 중 username의 정보를 받는다

        if not user: #user의 값이 없다면
            return "사용자 이름을 입력하시오<br> <a href= '/login'>로그인창으로 돌아가기</a>"

        #정상입력시: 로그인 성공 메세지 출력
        message = f"""
        <h2>로그인 성공!</h2>
        <p>안녕하세요 {user} 회원님. 준비된 서비스 이용하세요</p>
        <a href ='/'>메인으로 이동</a>
        """
        return make_response(message,200) #elif의 return. 전송 메세지, http 상태코드 전달 200을 전달 == 요청성공의 의미

    else:
        return make_response("잘못된 요청",405)

if __name__=='__main__':
    app.run(debug=True,host='0.0.0.0',port=5000);