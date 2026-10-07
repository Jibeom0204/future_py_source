from flask import Flask, jsonify, render_template,render_template_string, request,make_response,redirect, session,url_for,flash
import pymysql,os;
from db import get_connFunc

app=Flask(__name__);


@app.get("/")
def index():
    return render_template("index.html")


# 전체 직원 조회
@app.get("/acorn/jikwon")
def jikwon_list():
    sql="""
    select jikwonno, jikwonname, busername, jikwonjik, jikwonpay,year(jikwonibsail) as hire
    from jikwon
    inner join buser on jikwon.busernum=buser.buserno
    order by buserno
    """

    with get_connFunc() as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
            rows=cur.fetchall()
    return jsonify({"ok":True,"data":rows})


# 직원 1명 조회
@app.get("/acorn/jikwon/<int:no>")
def jikwon_One(no):
    sql="""
    select jikwonno, jikwonname, busername, jikwonjik, jikwonpay,year(jikwonibsail) as hire
    from jikwon
    inner join buser on jikwon.busernum=buser.buserno
    where jikwonno=%s
    """

    with get_connFunc() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (no,))
            row = cur.fetchone()#no가 %s와 대응됨. #왜 튜플식으로 하는거지? --> 파이썬에서 execute형식으로 sql실행할 때, execute 사용 원칙이 튜플로 사용하는거임
    return jsonify({"ok":True,"data":row})


# 전체 부서 조회
@app.get("/acorn/buser")
def buser_list():
    sql="""
    select * from buser order by buserno
    """

    with get_connFunc() as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
            rows=cur.fetchall()
    return jsonify({"ok":True,"data":rows})

# 특정 부서 직원 조회
@app.get("/acorn/buser/<int:no>")
def buser_One(no):
    sql="""
    select jikwonno 직원번호, jikwonname as 직원명, jikwonjik as 직급, jikwonpay as 연봉, year(jikwonibsail) as 입사년도
    from jikwon
    where busernum=%s 
    """

    with get_connFunc() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (no,))
            rows = cur.fetchall()
    return jsonify({"ok":True,"data":rows})

if __name__=='__main__':
    app.run(debug=True,host='0.0.0.0',port=5000);