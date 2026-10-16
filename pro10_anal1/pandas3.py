from pandas import Series,DataFrame
import numpy as np

s1=Series([1,2,3],index=['a','b','c'])
s2=Series([4,5,6,7],index=['a','b','c','d'])
print("s1 출력:\n",s1,'\n')
print("s2 출력:\n",s2,'\n')
print("s1+s1: \n",s1+s1,'\n') 
print("s1+s2: \n",s1+s2,'\n')# 같은 인덱스끼리 연산, 불일치 시 NaN

print("s1+s2: \n",s1.add(s2),'\n') # numpy 함수를 사용해서 더하기. add
print("s1+s2: \n",s1.add(s2,fill_value=0),'\n') # 결측치에 옵션을 더할 수 있음. + 보다 add가 유용함

print("s1*s2:\n",s1.mul(s2),'\n') # sub,div도 가능

print('======================\n')
df1=DataFrame(np.arange(9).reshape(3,3),columns=list('kbs'),index=['서울','대전','부산']) # 원래는 'k','b','s' 처럼써야하는데 이렇게도 가능
df2=DataFrame(np.arange(12).reshape(4,3),columns=list('kbs'),index=['서울','대전','부산','광주'])
print("df1 출력:\n",df1,'\n')
print("df2 출력:\n",df2,'\n')
print("df1+df2: \n",df1+df2,'\n')
print("결측치 채워서 df1+df2: \n",df1.add(df2,fill_value=0),'\n') # Nan은 0으로 채운 후. sub,mul,div도 가능 
print("결측치 채워서 df1*df2: \n",df1.mul(df2,fill_value=0),'\n') # 0을 채워서 곱하기 대문에 광주 값이 0 으로 채워짐


print("==============NaN(결측값) 처리==============\n")
print("==============행 관련==============\n")
df=DataFrame([[1.4,np.nan], [7,-4.5], [np.nan, np.nan], [0.5,-1]],columns=['one','two'])
print("\n",df,'\n')
print("NULL 탐지:\n",df.isnull(),'\n') # NULL 값 탐지(결측치 여부 확인)
print("NULL 탐지:\n",df.isna(),'\n') # NULL 값 탐지(결측치 여부 확인). 상동
print("Not NULL 탐지:\n",df.notnull(),'\n')
print("Not NULL 탐지:\n",df.notna(),'\n')

print("NULL 값 삭제: \n",df.dropna(),'\n') # 결측치가 포함된 값 삭제
print("NULL 행 값 삭제: \n",df.dropna(axis=0),'\n') # 행 결측치 삭제를 명시. 상동

print("NaN이 하나라도 있으면 그 행은 삭제\n", df.dropna(how='any'),'\n') # NaN이 하나라도 있으면 그 행은 삭제
print("한 행의 모든 값이 NaN일 때만 해당 행 삭제\n", df.dropna(how='all'),'\n') # 한 행의 모든 값이 NaN일 때만 해당 행 삭제



print("==============열 관련==============\n")
print("NULL 열 값 삭제: \n",df.dropna(axis=1),'\n') # 열 결측치 삭제를 명시 
print("one 열에 NaN 있는 행 삭제\n",df.dropna(subset=['one']),'\n') # subset에 묶인(one) 열에 NaN이 있는 행 삭제
print("two 열에 NaN 있는 행 삭제\n",df.dropna(subset=['two']),'\n')
print("행 기준으로 삭제\n",df.dropna(axis='rows'),'\n') # 행 기준 삭제. axis 0,1 안써도 됨
print("열 기준으로 삭제\n",df.dropna(axis='columns'),'\n') # 열 기준 삭제. 원본 삭제하는거 아님

imsi= df.dropna(axis='rows') # 원본이 아니라 삭제된 복사본이 만들어 짐
print("삭제된 복사본 imsi:\n",imsi,'\n')
print("원본 df: \n",df,'\n') # 원본은 유지
# df.dropna(axis='rows',inplace=True)# inplace로 원본 삭제
# print("원본 삭제 df: \n",df,'\n') # 원본은 유지

print("==============NaN(결측값) 관련 연산==============\n")
print("df 열끼리 합: \n",df.sum(),'\n') # 열끼리 합함. NaN은 연산에서 제외됨
print("df 열끼리 합: \n",df.sum(axis=0, skipna=True),'\n') # skipna: 
print("df 행끼리 합: \n",df.sum(axis=1),'\n') # 행끼리 합. skipna=True가 기본값
# mean(),min(),max(),std(),meadian(),prod()... 경우에도 적용 (기본은 NaN 무시)

print("요약 통계량: \n",df.describe(),'\n')
words=Series(['봄','여름,','가을','겨울'])
print(words.describe())