# DataFrame의 재구조화
from pandas import Series,DataFrame
import numpy as np
import pandas as pd

df=pd.DataFrame(1000+np.arange(6).reshape(2,3),index=['대전','서울'],columns=['2023','2024','2025'])
print("df\n",df,'\n')
# df
#      2023  2024  2025
# 대전  1000  1001  1002
# 서울  1003  1004  1005 

# stack, unstack
df_row=df.stack() # 열을 아래로 내려서 행 인덱스 쪽으로 쌓기. 가로로 펼쳐진 열을 세로로 쌓기
print("df_row\n",df_row,'\n')
# df_row
#  대전  2023    1000
#        2024    1001
#        2025    1002
# 서울  2023    1003
#       2024    1004
#       2025    1005
df_col=df_row.unstack() # 행 인덱스를 다시 열쪽으로 펼치기. 세로로 펼쳐진 열을 가로로 펼치기
print("df_col\n",df_col,'\n')

# 범주
print("==========연속형을 범주형으로==========")
price=[10.3,5.5,7.8,3.6]
cut=[3,7,9,11] # 자르는 구간 기준값 부여. (a,b)  => a<x<=b  a초과 b이하
# cut: 구간 기준 값 3개 [(3, 7] < (7, 9] < (9, 11]] ==> 3초과 7이하. 7초과 9이하. 9초과 11 이하.
result_cut=pd.cut(price,cut) # 연속형 -> 범주형
print("연속형 -> 범주형 \n",result_cut,'\n')

result_cut=pd.cut(price,bins=cut,labels=['저가','중가','고가']) # 구분별 기준 라벨 부여
print("라벨 \n",result_cut,'\n')
print(pd.Series(result_cut).value_counts())

print("====================")
datas=pd.Series(np.arange(1,1001))
print("위에서 5개\n",datas[:5],'\n')
print("위에서 2개\n",datas.head(),'\n') # 상동
print("위에서 2개\n",datas.head(2),'\n')
print("아래에서 2개\n",datas[-2:],'\n')
print("아래에서 2개\n",datas.tail(2),'\n') # 상동 

print("\n =================== agg함수 범주의 그룹별 연산 ===================")
datas =pd.DataFrame(
    {
        # '부서':['개발','개발','영업','영업','인사','개발'],
        # '이름':['길동','얌마','호떡','커피','지범','눈물'],
        '연봉':[2000,2999,3000,3999,4000,4999],
        '성과점수':[90,77,55,32,99,42],
    }
)
print("datas\n",datas,'\n')

# print("부서별 연봉 평균(group by)\n",datas.groupby('부서')['연봉'].mean(),'\n')
# print("부서별 인원 수(group by)\n",datas.groupby('부서')['이름'].count(),'\n')
# print("부서별 연봉,성과점수 평균(group by)\n",datas.groupby('부서')[['연봉','성과점수']].mean(),'\n')
# # [['연봉','성과점수']].mean() ==> ['연봉','성과점수'].mean() 이렇게 하면 두개를 동시에 인식 못함

# # 옵션
# pd.set_option('display.max_columns',None)
# print("add(['여러 집계함수'])\n",datas.groupby('부서')['연봉'].agg(['sum','mean','count']),'\n')

# agg대신 상요자 함수를 작성
def summaryFunc(gr):
    return{
        'count':gr.count(),
        'mean':gr.mean(),
        'std':gr.std(),
        'min':gr.min(),
    }
print(datas.apply(summaryFunc)) # apply: 함수 실행용 함수. 숫자만 먹음


print('\n =================merge: DataFrame 객체 병합: 공통 컬럼 기준으로 병합(RDBMS join처럼)=================')
df1=pd.DataFrame({'data1':range(7), 'key':['b','b','a','c','a','a','b']}) 
print("df1\n",df1,'\n')
df2=pd.DataFrame({'key':['a','b','d'],'data2':range(3)})
print("df2\n",df2,'\n')
print('두 데이터 프레임 inner join\n',pd.merge(df1,df2,on='key',how='inner'),'\n') # 교집합 (inner join)
print('두 데이터 프레임 full outer join\n',pd.merge(df1,df2,on='key',how='outer'),'\n') # 교집합 (full outer join)
print('두 데이터 프레임 left join\n',pd.merge(df1,df2,on='key',how='left'),'\n') # 교집합 (left outer join)
print('두 데이터 프레임 right join\n',pd.merge(df1,df2,on='key',how='right'),'\n') # 교집합 (outer outer join)

df3=pd.DataFrame({'key2':['a','b','d'],'data2':range(3)})
print("df3\n",df3,'\n')
# df3
#    key2  data2
# 0    a      0
# 1    b      1
# 2    d      2 
print("df1\n",df1,'\n')
# df1
#     data1 key
# 0      0   b
# 1      1   b
# 2      2   a
print("공통 키가 없는 두 테이블 병합\n", pd.merge(df1,df3,left_on='key',right_on='key2'),'\n')
# 공통 키가 없는 두 테이블 병합
#     data1 key key2  data2
# 0      0   b    b      1
# 1      1   b    b      1
# 2      2   a    a      0

print('==================concat: 상,하 또는 좌,우로 이어 붙이기==================\n')
print("행 기준\n",pd.concat([df1,df3],axis=0),'\n') # 행 단위
# 행 기준
#     data1  key key2  data2
# 0    0.0    b  NaN    NaN
# 1    1.0    b  NaN    NaN
# 2    2.0    a  NaN    NaN
print("열 기준\n",pd.concat([df1,df3],axis=1),'\n') # 열 단위
# 열 기준
#     data1 key key2  data2
# 0      0   b    a    0.0
# 1      1   b    b    1.0
# 2      2   a    d    2.0
# 3      3   c  NaN    NaN


print("\n Pivot 연산: Pivot과 group by 명령의 중간적 성격")
#pivot: 데이터 열중에서 두개의 열을 사용해 데이터의 행열을 재구성
data={ 'city':['강남','강북','강남','강북'],
      'year':[2000,2001,2002,2002],
      'pop':[3.3, 2.5, 3.0, 2.0]
}
df=pd.DataFrame(data)
print('df\n',df,'\n')
print('인구 describe\n',df['pop'].describe(),'\n')
print('도시 평균\n',df.pivot_table(index=['city']),'\n')
print('도시 평균\n',df.pivot_table(index=['city'], aggfunc='mean'),'\n') #상동


print('도시별, 연도별 \n',df.pivot_table(index=['city','year'], aggfunc=[len,'sum']),'\n')

print(' \n',df.pivot_table(index=['city'], values='pop'),'\n')
print(' \n',df.pivot_table(index=['city'], values='pop',aggfunc='mean'),'\n')
print(' \n',df.pivot_table(index=['city'], values='pop',aggfunc='len'),'\n')

# 구조 재구성: year가 행. city가 열
print("year가 행. city가 열\n", df.pivot_table(index=['year'], values='pop',columns=['city']),'\n')
print(df.pivot_table(index=['year'], values='pop', columns=['city'], margins=True))
print(df.pivot_table(index=['year'], values='pop', columns=['city'], margins=True, fill_value=0))
print()


Tlqkf 뭐가 문제지

hap = df.groupby(['city'])
print(hap)
print(hap.sum())
print(df.groupby(['city']).sum())
print(df.groupby(['city']).mean())
