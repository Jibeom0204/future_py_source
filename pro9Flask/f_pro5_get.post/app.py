from flask import Flask, render_template,request,make_response
#request : template에 있는 html을 반환
#make_response 는?
app =Flask(__name__);

@app.route("/")
def index():
    return render_template("index.html");

@app.route("/get_form")
def get_form():
    return render_template("get_form.html");

@app.route("/get_result")
def get_result():
    name=request.args.get("username") # get 방식으로 requset 사용하는 방법 request.arg.get
    age=request.args.get("age") # '23' 숫자가 아니라 문자 타입으로 받기. 연산할거면 숫자로 바꾸기
    age=age+"살"
    return render_template("get.result.html",name=name,age=age);



if __name__=='__main__':
    app.run(debug=True,host='0.0.0.0',port=5000);