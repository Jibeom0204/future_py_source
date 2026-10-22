from flask import Flask, render_template, request
import pymysql
import pandas as pd
import numpy as np
from markupsafe import escape
import matplotlib
matplotlib.use('Agg')            # 화면 창 없이 이미지로만 그리는 모드. 반드시 pyplot import보다 먼저 실행
import matplotlib.pyplot as plt  # 그래프 그리는 도구
import io                        # 메모리 안에서 파일처럼 쓰는 버퍼
import base64                    # 이미지를 HTML에 넣을 수 있는 문자열로 변환
plt.rcParams['font.family'] = 'NanumGothic'  # 한글 폰트 (설치 필요, 아래 표 참고)
plt.rcParams['axes.unicode_minus'] = False   # 한글 폰트 사용 시 마이너스 깨짐 방지
#문자열의 HTML 특수문자를 안전하게 바꾸는 함수,  <, > 등을 &lt;, &gt;로 바꿔서 브라우저가 코드를 실행하지 않고 글자로 표시한다

"""
MariaDB에 저장된 jikwon, buser 테이블을 이용하여 아래의 문제에 답하시오
 
   1) 사번, 직원명, 부서명, 직급, 연봉, 근무년수를 DataFrame에 기억 후 출력하시오. (join)
       : 부서번호, 직원명 순으로 오름 차순 정렬 
   2) 부서명, 직급 자료를 이용하여  각각 연봉합, 연봉평균을 구하시오.
   3) 부서명별 연봉합, 평균을 이용하여 세로막대 그래프를 출력하시오.
   4) 성별, 직급별 빈도표를 출력하시오.
   5) 부서별 최고 연봉자 출력 : 부서명별로 가장 연봉이 높은 직원 1명씩 출력 
       출력 항목: 부서명, 직원명, 연봉
   6) 부서별 직원 비율 계산 : 전체 인원 대비 각 부서 인원 비율(%) 
       비율 계산 (%)은 dept_ratio = (dept_count / total * 100).round(2)
      결과를 DataFrame으로 출력
      예: 총 인원: 30명
           영업부 20%
           총무부 30%
           전산부 5%
"""

app = Flask(__name__)
config = {
    'host':'127.0.0.1',
    'user':'root',
    'password':'123',
    'database':'test',
    'port':3306,
    'charset':'utf8mb4'
}  #원래는 env 써야함

def get_connection():
    return pymysql.connect(**config)

## 버튼 누를 때마낟 조회하는 방식으로 만들어보기

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/dbshow",methods=["GET","POST"])
# 1) 사번, 직원명, 부서명, 직급, 연봉, 근무년수를 DataFrame에 기억 후 출력하시오. (join)
#        : 부서번호, 직원명 순으로 오름 차순 정렬 
def db():
    sql1 = """select buserno 부서번호, jikwonno 사번, jikwonname 직원명, busername 부서명, jikwonjik 직급,
    year(NOW())-YEAR(jikwonibsail) as 근속
    from jikwon
    inner join buser on buserno=busernum
    order by busernum, jikwonname desc;"""

    # SQL 실행
    with get_connection() as conn: # DB랑 연결하는 것. 위의 함수를 가져옴.
        with conn.cursor() as cur: # SQL 명령어를 실행하고,결과를 순차적으로 가져오기 위한 메모리 포인터 역할하는 커서 객체를 생성
            cur.execute(sql1) #커서 객체.execute("sql 쿼리"). 위에 sql = .. 작성했으니 그거 가져옴
            data1=cur.fetchall()
            cols = [c[0] for c in cur.description] #description 칼럼등 여러 정보를 반환
    
    df1=pd.DataFrame(data1,columns=cols)
    print(df1.columns)
    # print("SQL 결과 데이터 프레임으로 출력\n",df,type(df))

    if not df1.empty:
        jikwondata=df1[['부서번호','사번','직원명','부서명','직급','근속']].to_html(index=False)
    else:
        jikwondata="정보 조회 불가"

# 2) 부서명, 직급 자료를 이용하여  각각 연봉합, 연봉평균을 구하시오.
    sql2 = """select jikwonjik 직급, sum(jikwonpay) 연봉합, avg(jikwonpay) 연봉평균
                from jikwon
                inner join buser on buserno=busernum
                group by jikwonjik
                ORDER BY jikwonjik DESC;
        """
    # SQL 실행
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql2)
            data2=cur.fetchall()
            cols =[c[0] for c in cur.description]
    
    df2=pd.DataFrame(data2,columns=cols)

    if not df2.empty:
        paydata=df2[['직급', '연봉합', "연봉평균"]].to_html(index=False)
    else :
        paydata="없음"


# 3) 부서명별 연봉합, 평균을 이용하여 세로막대 그래프를 출력하시오.
    sql3 = """select busername 부서명, sum(jikwonpay) 연봉합, avg(jikwonpay) 연봉평균
                from jikwon
                inner join buser on buserno=busernum
                group by busername
                ORDER BY busername DESC;
            """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql3)
            data3=cur.fetchall()
            cols=[c[0] for c in cur.description]

    df3=pd.DataFrame(data3,columns=cols)
    if not df3.empty:
        deptdata = df3.to_html(index=False)   # 표 출력용
            
        sums = df3['연봉합'].astype(float)     # Decimal → float 변환 (그래프 오류 방지)
        means = df3['연봉평균'].astype(float)

        fig, axes = plt.subplots(1, 2, figsize=(10, 4))

        axes[0].bar(df3['부서명'], sums)       # bar(x=가로축 이름, height=막대 높이)
        axes[0].set_title('부서별 연봉 합계')

        axes[1].bar(df3['부서명'], means)
        axes[1].set_title('부서별 연봉 평균')

        fig.tight_layout()                     # 글자 겹침 방지

        buf = io.BytesIO()                     # 메모리 속 빈 파일
        fig.savefig(buf, format='png')         # png로 buf에 저장
        plt.close(fig)                         # 메모리 정리
        chart = base64.b64encode(buf.getvalue()).decode('utf-8')  # 바이트 → 문자열

    else:
        deptdata = "없음"
        chart = ""

    #4) 성별, 직급별 빈도표를 출력하시오.

    #5) 부서별 최고 연봉자 출력 : 부서명별로 가장 연봉이 높은 직원 1명씩 출력 
    #        출력 항목: 부서명, 직원명, 연봉

    sql4="""
    SELECT busername 부서명, jikwonname 직원명, MAX(jikwonpay) 최고연봉
    FROM jikwon
    INNER JOIN buser ON busernum=buserno
    GROUP BY busername;
    """

    # 6) 부서별 직원 비율 계산 : 전체 인원 대비 각 부서 인원 비율(%) 
    return render_template("dbshow.html",
                           jikwondata=jikwondata,
                           paydata=paydata,
                           deptdata=deptdata,
                           chart=chart)



if __name__ == '__main__':
    app.run(debug=True)



