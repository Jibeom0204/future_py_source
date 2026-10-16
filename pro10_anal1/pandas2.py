# 재 색인_순서 재배치
from pandas import Series,DataFrame

# Series의 재 색긴
data =Series([1,3,2],index=(1,4,2))
print("원본 data 출력: \n", data,'\n')
data2=data.reindex((1,2,4))  # 내가 작성한 대로 가능 #sort_index()함수는 오름차순, 내림차순만 가능함
print("reindx한 data2 출력:,\n", data2,'\n')

print('\n 재색인 할때 값 채워 넣기')
data3=data2.reindex([0,1,2,3,4,5])
print("reindx한 data3 출력:,\n", data3,'\n')
#  0    NaN
# 1    1.0
# 2    2.0
# 3    NaN
# 4    3.0
# 5    NaN
# dtype: float64 

# 대응값이 없는 인덱스에 특정값으로 채우기
data3=data2.reindex([0,1,2,3,4,5],fill_value=777) # 결측치 있는 값을 fill_value로 777 채움
print("결측치 채운 data3 출력:,\n", data3,'\n')

# NaN 값 앞으로 NaN을 채우기
data3 = data2.reindex([0,1,2,3,4,5],method='ffill')
#method='ffill' 쓰려면 data2가 정렬된 상태여야 함
# data2=data.reindex((2,1,4)) 처럼 되어있으면 에러
# method는 bfill, backfill 등 많다.

print("ffill로 결측치 채운 data3 출력:,\n", data3,'\n')
# reindx한 data3 출력:, //  ffill로 결측치 채운 data3 출력:,
# 0    NaN            //     0    NaN
# 1    1.0             //    1    1.0
# 2    2.0             //    2    2.0
# 3    NaN             //    3    2.0
# 4    3.0             //    4    3.0
# 5    NaN             //    5    3.0
# dtype: float64       //  dtype: float64 

# bool 처리
import numpy as np
print('\n ==============DataFrame: bool 처리==============')
df=DataFrame(np.arange(12).reshape(4,3),index=['1월','2월','3월','4월'],columns=['강남','강북','서초'])
print(df,'\n')

print("df 중 강남만 출력: \n",df['강남'],'\n')
print("df 중 강남에서 3 이상: \n",df['강남']>3,'\n') #강남 안에 있는 값들 중 3 이상인 것을 비교하여 true,false만 출력
print("df 중 강남에서 3 이상: \n",df[df['강남']>3],'\n') # 조건에 맞는 값들을 값으로 출력
# df 중 강남만 출력: 
#  1월    0
# 2월    3
# 3월    6
# 4월    9
# Name: 강남, dtype: int64 

# df 중 강남에서 3 이상: 
#  1월    False
# 2월    False
# 3월     True
# 4월     True
# Name: 강남, dtype: bool 

# df 중 강남에서 3 이상: 
#      강남  강북  서초
# 3월   6   7   8
# 4월   9  10  11 

print(df<3,'\n') #전체 자료 대상으로 bool값 출력
#        강남     강북     서초
# 1월   True   True   True
# 2월  False  False  False
# 3월  False  False  False
# 4월  False  False  False 
df[df<3]=0 # 3 미만 자료는 0으로 대체
print(df,'\n')
#     강남  강북  서초
# 1월   0   0   0
# 2월   3   4   5
# 3월   6   7   8
# 4월   9  10  11 



print("========슬라이싱 관련 메소드========\n")
# df.loc['행 이름']: 해당 행        df.iloc[행(열) 번호]: 위치 기준 행
print("행 이름으로 출력\n",df.loc['3월'],'\n')
print("행 이름으로 출력\n",df.loc['3월', :],'\n')

print("행 이름으로 출력: 2월 이하 행 출력: \n",df.loc[:'2월'],'\n')
print("행 이름으로 출력: 2월 이하 행 중 서초만 출력: \n",df.loc[:'2월',['서초']],'\n')
print("\n=============================================\n")
print(df,'\n')
print("iloc로 행 출력1: \n",df.iloc[2],'\n')
print("iloc로 행 출력2: \n",df.iloc[2,:],'\n') 
print("iloc로 행 출력3: \n",df.iloc[:3],'\n') # 3행 미만 행 모든 열
print("iloc로 행 출력4: \n",df.iloc[:3,2],'\n') # 3행 미만 행 2열
print("iloc로 행 출력5: \n",df.iloc[:3,1:3],'\n') # 3행 미만 행 1,2열
print("iloc로 행 출력6: \n",df.iloc[1:3,1:3],'\n') # 1,2행, 1,2열