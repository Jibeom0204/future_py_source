"""
MariaDB에 저장된 jikwon 테이블을 이용하여 아래의 문제에 답하시오.
     - pivot_table을 사용하여 성별 연봉의 평균을 출력
     - 성별(남, 여) 연봉의 평균으로 시각화 - 세로 막대 그래프

     - 부서명, 성별로 교차 테이블을 작성 (crosstab(부서, 성별))
"""

import pymysql
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import koreanize_matplotlib
from sqlalchemy import create_engine

config = {  # 원래는 .env로 해야하는데 그냥 수기 작성 # 방법1
    'host':'127.0.0.1',
    'user':'root',
    'password':'123',
    'database':'test',
    'port':3306,
    'charset':'utf8'
}

try:
    # # 방법1
    # conn=pymysql.connect(**config) #**는 딕셔너리 언패킹.  config = {  => pymysql.connect( 이렇게 자동 변환시켜줌
    # 사번 직원명 부서명 연봉 성별을 읽어 DataFradme을 작성
    sql="""
    select jikwonno 사번, jikwonname 직원명, busername 부서명, jikwonpay 연봉,jikwongen 성별
    from jikwon inner join buser
    on jikwon.busernum=buser.buserno
    """
    # df=pd.read_sql(sql,conn)


    # # 방법2
    engine=create_engine("mysql+pymysql://root:123@127.0.0.1:3306/test")
    df=pd.read_sql(sql,engine)
    print(df.head(3))


    # pivot_table을 사용하여 성별 연봉의 평균을 출력
    pt=pd.pivot_table(df,index="성별",values='연봉',aggfunc='mean')
    print("성별 연봉의 평균: \n", pt)
    print()


    # 성별 연봉의 평균으로 시각화 - 막대그래프(pandas)
    pt.plot(kind='bar',legend=False,rot=0)
    plt.title("성별 연봉의 평균")
    plt.xlabel=("성별")
    plt.ylabel=("연봉")
    plt.tight_layout() # 자동으로 사이즈 맞추기
    plt.show()

    # 부서명, 성별로 교차 테이블을 작성(crosstab(부서,성별))
    ct=pd.crosstab(df['부서명'],df['성별'])
    print('부서명 성별 교차 테이블:\n',ct)
    
except Exception as e:
    print('처리 오류 :',e)
finally:
    #conn.close()
    engine.dispose()



# 기능	:               df.pivot()	                                   df.pivot_table()
# 주요 목적:	        단순 형태 변환 (구조 재구조화)	                  데이터 요약 및 집계
# 중복 값 처리:        	중복된 인덱스/열이 있으면 에러 발생	               aggfunc를 통해 중복 값 자동 집계
# 집계 함수 (aggfunc): 	사용 불가 ❌	                                   사용 가능 (기본값: mean) ✅
# 결측값(NaN) 처리: 	지원하지 않음	                                 fill_value 옵션으로 대체 가능
