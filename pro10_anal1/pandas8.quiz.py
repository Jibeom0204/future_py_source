"""df = pd.read_csv('파일명',  header=None,,,)  

  열 구성 정보
    Survived : 0 = 사망, 1 = 생존
    Pclass : 1 = 1등석, 2 = 2등석, 3 = 3등석
    Sex : male = 남성, female = 여성
    Age : 나이
    SibSp : 타이타닉 호에 동승한 자매 / 배우자의 수
    Parch : 타이타닉 호에 동승한 부모 / 자식의 수
    Ticket : 티켓 번호
    Fare : 승객 요금
    Cabin : 방 호수
    Embarked : 탑승지, C = 셰르부르, Q = 퀸즈타운, S = 사우샘프턴

 1) 데이터프레임의 자료로 나이대(소년, 청년, 장년, 노년)에 대한 생존자수를 계산한다.
      cut() 함수 사용
     bins = [1, 20, 35, 60, 150]
      labels = ["소년", "청년", "장년", "노년"]

  2) 성별 및 선실에 대한 자료를 이용해서 생존여부(Survived)에 대한 생존율을 피봇테이블 형태로 작성한다. 
      df.pivot_table()
     index에는 성별(Sex)를 사용하고, column에는 선실(Pclass) 인덱스를 사용한다.
      출력 결과 샘플1 :       
pclass	1	2	3
sex			
female	0.968085	0.921053	0.500000
male	0.368852	0.157407	0.135447
     
   index에는 성별(Sex) 및 나이(Age)를 사용하고, column에는 선실(Pclass) 인덱스를 사용한다.
   출력 결과 샘플2 : 위 결과물에 Age를 추가. 백분율로 표시. 소수 둘째자리까지.    예: 92.86"""

import pandas as pd
import numpy as np

# data 읽기
df=pd.read_csv("titanic_data.csv")
print("상위 3개\n",df.head(3),'\n')
print("컬럼명 확인\n",df.columns,'\n')

#나이대(소년, 청년, 장년, 노년)에 대한 생존자수를 계산
bins=[1,20,35,60,150] # 나이구간 경계값
lables=["소년", "청년", "장년", "노년"] # 구간별 이름

df['나이대']=pd.cut(df['Age'],bins=bins,labels=lables) #cut: 연속형 숫자 데이터를 특정 구간(bin)으로 나누어 범주형(categorical) 데이터로 변환
print("나이구분 상위 3개\n",df.head(3),'\n')

# survived: 생존 1: 사망 0
result=(df.groupby('나이대',observed=True)['Survived'].sum().reset_index()
)
# • observed=True (실제 관측된 값만 집계)
# 	• 데이터프레임에 실제로 최소 1번 이상 등장한 범주만 그룹 결과에 포함
# 실제 존재하는 결과만 나이대에 참여
print("나이대에 대한 생존 인원 수 출력:\n",result,'\n')#
# 나이대에 대한 생존 인원 수 출력
#  나이대
# 소년     70
# 청년    125
# 장년     78
# 노년      5
# Name: Survived, dtype: int64 

# reset.index 사용결과 : 인덱스로 올라간 값을 일반 컬럼으로 내리기
# 나이대에 대한 생존 인원 수 출력:
#    나이대  Survived
# 0  소년        70
# 1  청년       125
# 2  장년        78
# 3  노년         5 

result.columns=['나이대','생존자 수'] # 출력 컬럼명 변경
print("나이대에 대한 생존 인원 수:\n",result)

# 성별 및 선실에 대한 자료를 이용해서 생존 여부에 대한 생존율
pivot1=df.pivot_table(
    values='Survived', # 계산에 사용할 값
    index='Sex', #행 기준(성별)
    columns='Pclass', # 열 기준: 선실 등급
    aggfunc='mean' # Survived 에 대한 평균
)
# pivot: 축 돌려서 출력. 필요한 요소:
# 1. Index (행 축): 테이블의 세로 줄에 배치할 기준 (위 예시에서는 '매장')
# 2. Columns (열 축): 테이블의 가로 줄에 배치할 기준 (위 예시에서는 '상품')
# 3. Values (값): 교차하는 칸에 채워 넣을 숫자 데이터 (위 예시에서는 '매출'
# 중복되는 데이터가 있다면 더할지(sum), 평균을 낼지(mean) 결정하는 집계 함수(Aggregation)

print('\n성별 및 선실 등급별 생존율\n',pivot1,'\n')

# 성별+나이대+선실 등급별 생존율
pivot2=df.pivot_table(
    values='Survived', # 계산에 사용할 값
    index=['Sex','나이대'], #행 기준(성별,나이대)
    columns='Pclass', # 열 기준: 선실 등급
    aggfunc='mean', # Survived 에 대한 평균
    observed=True # 실제 존재하는 범주 출력
)
pivot2=(pivot2*100).round(2) # 생존율을 %로 변환 후 소수둘째자리까지 출력
print('성별+나이대+선실 등급별 생존율\n',pivot2,'\n')
pivot2=(pivot2*100).fillna() # NaN은 0으로 대체
print('성별+나이대+선실 등급별 생존율2\n',pivot2,'\n')# 