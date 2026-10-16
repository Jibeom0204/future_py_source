"""
고수준의 자료구조(Series,DataFrame)와 빠르고 쉬운 데이터 분석용 함수 제공
통합된 시계열 연산, 축약연산, 누락 데이터 처리 SQL, 시각화...등을 제공
데이터 랭글링(Wrangling), 테인터 먼징(Data Munging)을 효율적으로 처리가능


• 데이터 랭글링 (Data Wrangling): '데이터를 다룬다'는 의미로,
원시 데이터를 분석용 구조로 매핑하고 변환하는 포괄적인 과정을 뜻합니다.
(예: 판다스(Pandas)를 이용한 데이터프레임 형태 변환)

• 데이터 먼징 (Data Munging): 랭글링과 동일한 작업을 뜻하지만,
조금 더 비정형적이거나 수작업으로 지저분한 데이터를 주무르고 손보는(munging) 뉘앙스가 강합니다.
"""
import numpy as np
import pandas as pd
from pandas import Series,DataFrame

# Series: 일련의 객체를 담을 수 있는 1차원 배열과 같은 자료구조로 색인(index)을 가짐
obj=pd.Series([3,7,-5,4]) # 리스트(), 튜플[], dict 가능, 셋{}은 불가능
#obj=pd.Series([3,7,-5,4,'일']) # 요소값 모두가  object type
print(obj,type(obj))
print('===============')

obj2=pd.Series([3,7,-5,4], index=['a','b','c','d']) # 기본 index는 0부터 시작하는 정수. 내가 index를 지정할 수 있음
print("obj2: ",obj2,"\n")
print("각 덧셈: ",obj2.sum(),' ',np.sum(obj2),' ',sum(obj2),'\n') #obj2.sum():넘파이 기반이지만 판다스 sum, np.sum(obj2): 넘파이 sum, sum(obj2): 파이썬 sum->느림
print("obj2.std(): ",obj2.std(),'\n')

print(obj2.index) # 색인만 출력
print(obj2.values) # 값만 출력

# 인덱싱/슬라이싱
print("obj2['a']: ",obj2['a'],'\n')  # 'a' 인덱스의 값 '3'이 출력
print("obj2[['a']]: ",obj2[['a']],'\n') # a의 인덱스와 값 같이 출력

print("obj2['a','b']: \n", obj2[['a','b']], "\n")  # 'a' 인덱스의 값 '3'이 출력
print("obj2['a':'c']: \n", obj2['a':'c'], "\n") # a의 인덱스와 값 같이 출력

#print(obj2[2]) #Keyerror: index 순서는 문자열을 사용함
print("obj2.iloc[2]: ",obj2.iloc[2],"\n") # iloc[위치번호]-Series의 2번째 위치에 있는 값  # 2번 인덱스(실질적으로 3번값) 출력
print("obj2.loc['c']:", obj2.loc['c'],'\n') # loc['인덱스 이름']

print("obj2[1:3]: ", obj2[1:3],"\n")
print("obj2.iloc[[2,1]]: ",obj2.iloc[[2,1]],'\n') # 위치 기반 2번, 1번 순서대로 출력
print("obj2.iloc[[1,2]]: ",obj2.iloc[[1,2]],'\n')
print('a' in obj2)
print('k' in obj2)

print('=======================================')
print('\n 파이썬 dict 자료를 Series 객체로 생성')
names ={'mouse':5000,'keyboard':35000,'monitor':55000}
obj3=Series(names)
print("obj3값과 타입: \n",obj3, type(obj3),'\n')
#   [key]        [value]
#  mouse        5000
# keyboard    35000
# monitor     55000
# key값이 index가 된다.

obj3.index=['마우스','키보드','모니터']
print("obj3값과 타입: \n",obj3, type(obj3),'\n')
#  마우스     5000
# 키보드    35000
# 모니터    55000

obj3.name='상품가격'
print(obj3)
# 마우스     5000
# 키보드    35000
# 모니터    55000
# Name: 상품가격, dtype: int64
print('======================\n')
"""
DataFrame : 
    표 모양(2차원형태자료)의 자료구조로 여러 개의 칼럼을 갖는다. (Series가모인형태)
    각 칼럼은 서로 다른 종류의 값을 기억할 수 있다. 
    같은 길이의 리스트에 담긴 dicttype의 데이터를 이용해 DataFrame 객체 생성. 
"""

df=pd.DataFrame(obj3)
print("obj3 값 데이터프레임화 시키고 데이터 프레임의 값과 타입: \n",df,type(df),'\n')
data = {
'irum':['홍길동', '한국인', '신기해', '공기밥', '한가해'],
'juso':('역삼동', '신당동', '역삼동', '역삼동', '신사동'),
'nai':[23, 25, 33, 30, 35],
} # dict 타입의 데이터
frame=pd.DataFrame(data) # dict타입을 DataFrame 형식으로
print("Dataframe으로 변환된 frame\n",frame,'\n')

print("이름열: \n",frame['irum'],type(frame['irum']),'\n')
# 이름들 하나하나는 벡터, irum 열은 Series, 전체는 Dataframe
print("frame.irum 식으로도 가능:\n",frame.irum,"\n") #이렇게도 가능

print(DataFrame(data=data,columns=['juso','irum','nai']),'\n') # 열 순서 변경


# NaN(결측치): Not a number: 결측치, 값이 없거나 알 수 없는 Missing Value를 말함
frame2=pd.DataFrame(data,columns=['juso','irum','nai','tel'], index=['a','b','c','d','e'])
print("frame2: \n",frame2, type(frame2),'\n')
#     juso    irum  nai  tel
# a  역삼동  홍길동   23  NaN
# b  신당동  한국인   25  NaN
# c  역삼동  신기해   33  NaN
# d  역삼동  공기밥   30  NaN
# e  신사동  한가해   35  NaN
# 해당 컬럼에 없는 값은 NaN

print('===========================')

frame2['tel'] ='111-1111'
print('번호 부여 후 출력\n',frame2,'\n')
val=pd.Series(['222-2222','333-3333','444-4444'], index=['b','c','e'])
print("1차원 배열 시리즈 val: \n",val,'\n')

print('===========================')
frame2['tel']=val #기존자료 덮어쓰기
print("번호 갱신 후:\n",frame2,'\n')
# 번호 갱신 후:
#    juso irum  nai       tel
# a  역삼동  홍길동   23       NaN
# b  신당동  한국인   25  222-2222
# c  역삼동  신기해   33  333-3333
# d  역삼동  공기밥   30       NaN
# e  신사동  한가해   35  444-4444 

print("전치: \n",frame.T,'\n')
# 전치: 
#          0    1    2    3    4
# irum  홍길동  한국인  신기해  공기밥  한가해
# juso  역삼동  신당동  역삼동  역삼동  신사동
# nai    23   25   33   30   35 

print("frame2의 값만 출력: \n",frame.values,type(frame2.values),'\n')
# frame2의 값만 출력: 
#  [['홍길동' '역삼동' 23]
#  ['한국인' '신당동' 25]
#  ['신기해' '역삼동' 33]
#  ['공기밥' '역삼동' 30]
#  ['한가해' '신사동' 35]] <class 'numpy.ndarray'> 

# frame2: 
#    juso irum  nai  tel
# a  역삼동  홍길동   23  NaN
# b  신당동  한국인   25  NaN
# c  역삼동  신기해   33  NaN
# d  역삼동  공기밥   30  NaN
# e  신사동  한가해   35  NaN <class 'pandas.DataFrame'> 
# 값만 출력하면 class 타입이 바뀐다.
print(frame2.values[0,1],'\n') #홍길동 
print(frame2.values[0:2],'\n')
# [['역삼동' '홍길동' 23 nan]
#  ['신당동' '한국인' 25 '222-2222']] 

# 삭제
frame3=frame2.drop('d') # 행 삭제. 원본 데이터 유지
frame3= frame2.drop('d',axis=0)
print("행 삭제 하고 출력: \n",frame3,'\n')

frame4= frame2.drop('tel',axis=1) # 열 삭제
print("열 삭제 하고 출력: \n",frame4,'\n')

print('===========================\n\n')
print(frame2)
print("행 단위 정렬: \n",frame2.sort_index(axis=0,ascending=False),'\n') # 행 단위 정렬
print("열 단위 정렬: \n",frame2.sort_index(axis=1,ascending=False),'\n') # 열 단위 정렬

print("순위 출력: \n",frame2.rank(axis=0),'\n') # 순위 매김

counts = frame2['juso'].value_counts()
print("counts 출력: \n",counts,'\n')

# 문자열 자르기
data={
    'juso':['서초구 서초2동','강남구 역삼동','강남구 대치동'],
    'inwon': [23,25,15]
}
fr=pd.DataFrame(data)
print("자르기 전 원본 데이터 fr: ;\n",fr,'\n')

result1=Series(x.split()[0] for x in fr.juso)
result2=Series(x.split()[1] for x in fr.juso)
print("공백기준으로 문자열 인덱스 구분됨('구'로구분) result1:\n",result1,'\n')
print("공백기준으로 문자열 인덱스 구분됨('동'으로구분)result2:\n",result2,'\n')
print("result1.value_counts()\n",result1.value_counts(),'\n')