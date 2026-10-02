from flask import Flask, render_template,render_template_string
from flask import request,make_response,redirect,url_for,session
"""
파이썬 세션은 웹에서 사용자 정보를 서버에 저장하는 기능을 말함(쿠키틀 통해 세션 운영)
일정시간동안 동일 사용자(브라우저)와 이;ㄹ련의 요청을 하나의 상태로 보고 그 상태를 유지지시키는 기술
쿠키에 비해 상대적으로 안전함
"""
#실습: 사용자가 os를 선택하면 세션에 저장하고 읽기
from datetime import timedelta

app=Flask(__name__);

#Flask는 세션 사용을 위해 secret_key 설정이 필요
app.secret_key="abc123" #위조 방지용 비밀키값
# python -c "import secrets;print(secrets.token_hex(32))"
# 결과: c8897f42ab98f5ef8c559d0c272686a286bf27756b2346e07d5102a1dd915826

app.permanent_session_lifetime=timedelta(seconds=5) # 세션만료시간 5초로 설정 


@app.get("/") # url을 통해 요청이 들어오는것을 확인
def home():
    return render_template("main.html")

@app.route("/setos") # url을 통해 /setos 요청이 들어오는것을 확인
def setos():
    favorite_os=request.args.get("favorite_os") #사용자가 선택한 운영체제 기억.  이 단에서는 아직 넘겨주지 않았음

    if favorite_os:
        session.permanent=True # 세션 만료 시간 설정
        session["f_os"] =favorite_os # "f_os"키로 특정값 세션에 저장
        return redirect(url_for("showos"))
    else:
        return render_template("setos.html")

@app.route("/shows") #클라이언트를 통해 들어온 요청이 redirect(url_for("showos")) 통해 들어오고 def shows():를 실행하며 함수에 묶인 @app이 실행
def showos():
    context={}

    if "f_os" in session:
        context["f_os"] = session["f_os"]
        context["message"] =f"당신이 선택한 운영체제는 '{session['f_os']}'"
    else:
        context["f_os"] = None
        context["message"] = "운영체제 선택하지 않았거나 세션이 만료됨"

    return render_template("showos.html", context=context)


if __name__=='__main__':
    app.run(debug=True,host='0.0.0.0',port=5000);