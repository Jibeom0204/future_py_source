# 회귀분석 문제 4) 

# 원격 DB의 jikwon 테이블에서 근무년수에 대한 연봉을 이용하여 회귀분석 모델을 작성하시오.
# Django 또는 Flask로 작성한 웹에서 근무년수를 입력하면 예상 연봉이 나올 수 있도록 프로그래밍 하시오.
# LinearRegression 사용. Ajax 처리!!!      참고: Ajax 처리가 힘들면 그냥 submit()을 해도 됩니다.

from flask import Flask, render_template,render_template_string, request,make_response,redirect,url_for,flash
# pip install pymysql
import pymysql
import os
from flask import get_flashed_messages # 저장해둔 메세지를 꺼내는 함수
# 예: flash("에러~~") -> 메세지를 세션에 잠시 저장 후 get_flashed_messsage만나면 메세지 읽기 가능

app=Flask(__name__);
app.secret_key="abcd1234" # 쿠키 서명용 비밀키

#MariaDB 연결정보
DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "123")
DB_NAME = os.getenv("DB_NAME", "test")

def get_conn():
    return pymysql.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        charset="utf8mb4" ,# 전세계 문자(한글 포함)+이모지까지 처리가능
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=False
    )

@app.route("/")
def home():
    return render_template("index.html");

@app.route("/dbshow", methods=['GET', 'POST'])
def main():
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    import koreanize_matplotlib
    from sklearn.datasets import load_iris
    from sklearn.metrics import mean_squared_error, r2_score
    from sklearn.model_selection import train_test_split
    from sklearn.linear_model import LinearRegression,Ridge,Lasso,ElasticNet
    
    conn=get_conn()
    sql="""select jikwonpay as '연봉', year(now())-year(jikwonibsail) AS '근속년수' from jikwon ;"""
    try:
        
        with conn.cursor() as cur:
            cur.execute(sql)
            rows=cur.fetchall()
        year_pay_df=pd.DataFrame(rows)
        print(year_pay_df)
        



    except Exception as e:
        print('에러')
    finally:
        conn.close()
    
    return render_template("dbshow.html",year_pay_df=year_pay_df)


if __name__=='__main__':
    app.run(debug=True,host='0.0.0.0',port=5000);