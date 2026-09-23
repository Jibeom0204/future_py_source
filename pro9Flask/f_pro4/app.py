from flask import Flask, render_template

app =Flask(__name__);

@app.route("/")
def index():
    return render_template("index.html");

@app.route("/condition")
def condition():
    score =85;
    return render_template("condition.html",score=score);

@app.route("/loop")
def loop():
    users=["김","나","박","이"]
    return render_template("loop.html",users=users);

@app.route("/filter")
def filter():
    message = "hello Flask Jinja2";
    price=12345;
    return render_template("filter.html",m1=message,p1=price);

#jinja2에는 기본적으로 천의 자리 단위 콤마가 없어서 직접 구현하거나 format 사용가능
@app.template_filter('format')
def format_number(value):
    return format(value, ",") # 세자리 마다 , 출력


if __name__=='__main__':
    app.run(debug=True,host='0.0.0.0',port=5000);