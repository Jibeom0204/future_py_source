from flask import Flask, jsonify, render_template,render_template_string, request,make_response,redirect, session,url_for,flash
import pymysql,os;

app=Flask(__name__);


@app.get("/")
def index():
    return render_template("main.html")

@app.get("/legacy")
def iegacy_f():
    pass#지금은 생략

@app.get("/async")
def async_f():
    pass#지금은 생략

@app.get("/fetch")
def fetch_f():
    return render_template("show3.html")

@app.get("/axios")
def axios_f():
    return render_template("show3.html")
 
@app.get("/api/sangdata")
def sangdata():
    conn=pymysql.connect(
        host="localhost",
        user="root",
        password="123",
        database="test",
        charset="utf8mb4" ,# 전세계 문자(한글 포함)+이모지까지 처리가능
    )
    cur=conn.cursor()
    cur.execute("select code,sang,su,dan from sangdata")
    columns=[col[0] for col in cur.description]
    rows=cur.fetchall()
    result=[dict(zip(columns,row)) for row in rows]
    print(result)
    cur.close()
    conn.close()
    return jsonify(result)

if __name__=='__main__':
    app.run(debug=True,host='0.0.0.0',port=5000);