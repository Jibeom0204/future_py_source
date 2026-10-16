# DataFrame의 재구조화
from pandas import Series,DataFrame
import numpy as np
import pandas as pd
pd.set_option('display.max_columns',None) # 싹 다 보여주기
df=pd.read_csv('test.csv')
print("ex1 df\n", df,type(df),"\n")
df=pd.read_csv("https://raw.githubusercontent.com/cwoo0611/pythonforktest/refs/heads/master/testdata_utf8/ex1.csv")
print("ex1 df\n", df,type(df),"\n")

print()
# df=pd.read_table("https://raw.githubusercontent.com/cwoo0611/pythonforktest/refs/heads/master/testdata_utf8/ex1.csv",sep=',')
df=pd.read_table("https://raw.githubusercontent.com/cwoo0611/pythonforktest/refs/heads/master/testdata_utf8/ex1.csv",sep=r',',skip_blank_lines=True)
#,skip_blank_lines=True : 컬럼명이나 데이터 앞에 공백 제거
print('ex1 df\n', df,type(df),'\n')


df=pd.read_csv("https://raw.githubusercontent.com/cwoo0611/pythonforktest/refs/heads/master/testdata_utf8/ex2.csv")
print("ex2 df\n", df,type(df),"\n")

df=pd.read_csv("https://raw.githubusercontent.com/cwoo0611/pythonforktest/refs/heads/master/testdata_utf8/ex2.csv",header=None)
print("ex2 헤더 삭제 df\n", df,type(df),"\n")

df=pd.read_csv("https://raw.githubusercontent.com/cwoo0611/pythonforktest/refs/heads/master/testdata_utf8/ex2.csv",header=None,skiprows=1)
print("ex2 첫번째 데이터 삭제 df\n", df,type(df),"\n")

df=pd.read_csv("https://raw.githubusercontent.com/cwoo0611/pythonforktest/refs/heads/master/testdata_utf8/ex2.csv",header=None,names=['a','b','c','d','e'])
print("ex2 컬럼이름 변경 df\n", df,type(df),"\n")

df=pd.read_csv("https://raw.githubusercontent.com/cwoo0611/pythonforktest/refs/heads/master/testdata_utf8/ex3.txt")
print("txt를 csv로 읽기\n", df,type(df),"\n")
# txt를 csv로 읽기
#                 A         B         C
# 0  aaa -0.264438 -1.026059 -0.619500
# 1  bbb  0.927272  0.302904 -0.032399
df=pd.read_csv("https://raw.githubusercontent.com/cwoo0611/pythonforktest/refs/heads/master/testdata_utf8/ex3.txt",sep=r'\s+',skiprows=[1,3])
# 공백의 공간이 얼마나 되는지 모르면 정규표현식 사용. \s+
print("정규 표현식 사용해서 txt를 csv로 읽기\n", df,type(df),"\n")
# 정규 표현식 사용해서 txt를 csv로 읽기
#              A         B         C
# aaa -0.264438 -1.026059 -0.619500
# bbb  0.927272  0.302904 -0.032399
# ccc -0.264273 -0.386314 -0.217601
# ddd -0.871858 -0.348382  1.100491 
# ★★컬럼의 이름이 없어서 맨 처음의 것이 인덱스로 들어감★★

#skiprows=[1,3] 이거 쓰면 1행 3행 빠짐
#skiprows=range(1,3)
#skiprows=lambda x:x in [1,3] 방법은 여러가지


#read_fwf: 고정된 문자 폭으로 열 구분
df=pd.read_fwf("https://raw.githubusercontent.com/cwoo0611/pythonforktest/refs/heads/master/testdata_utf8/data_fwt.txt",
               header=None,widths=(10,3,5),names=('날짜','상호','가격'),encoding='utf-8') # 윈도우에서 깨지면 cp949,euc-kr 로 읽어도 됨
print("fwf 읽기\n", df,type(df),"\n")
print(df['날짜'].head(2),'\n')
print(df.iloc[:,0].tail(2),'\n')
print("=========================================================")



print('\n\n Chunk: 대량의 데이터를 부분씩(일정크기) 메모리로 읽어 처리하는 단위')
# 대용량 자료 전체 로딩시 메모리 초과 오류 발생 방지 - 멤리 관리
# 스트리밍 방식(일부만 순차 처리)으로 읽기, 분산처리의 효과
# 여러 번 반복해서 읽어야 하므로 속도는 느리다.
import time

n_rows=100000
data={
    'id':range(1,n_rows+1),
    'name': [f'Student_{i}' for i in range(1,n_rows+1)],
    'score1':np.random.randint(50,101, size=n_rows),
    'score2':np.random.randint(50,101, size=n_rows),
}
df=pd.DataFrame(data=data)
print("df\n", df,type(df),"\n")
print("df 위에서 5개\n", df.head(),type(df),"\n")
print("df 아래서 2개\n", df.tail(2),type(df),"\n")

csv_fname='pandas5student.csv' # '저장할 파일의 이름.확장자'
# df.to_clipboard()
df.to_csv(csv_fname,index=False) # Dataframe을 파일로 저장

print('==============================\n')
# csv 파일 읽기: 전체 한번에 읽기
start_all=time.time()
df_all=pd.read_csv(csv_fname)
average_all_1=df_all['score1'].mean()
average_all_2=df_all['score2'].mean()
print(f"전체 처리 score1 평균: {average_all_1:3f}")
print(f"전체 처리 score2 평균: {average_all_2:3f}\n")
time_all=time.time()-start_all

# Chunk로 읽기
chunk_size=1000
total_score1= 0
total_score2= 0
total_count= 0

start_chunk_total= time.time() # 앞의 time은 import로 받아온 모듈. time()은 time 모듈 안에 있는 메서드
for i, chunk in enumerate(pd.read_csv(csv_fname,chunksize=chunk_size)):#1000개로 구분
    start_chunk=time.time()

    #청크 처리중 첫번째 학생 정보 출력
    first_student=chunk.iloc[0]
    print(f"chunk {i+1} 첫번째 학생:ID={first_student['id']}, 이름={first_student['name']}",
          f"score1={first_student['score1']}",f"score2={first_student['score2']}")
    total_score1 += chunk['score1'].sum()
    total_score2 += chunk['score2'].sum()
    total_count += len(chunk)
    end_chunk=time.time()
    elasped=end_chunk-start_chunk
    print(f"====처리 시간: {elasped:7f}") # 청크 단위 처리 시간. 7f 소수자리이하 7자리

time_chunk_total=time.time() -start_chunk_total
average_chunk1 =total_score1/total_count
average_chunk2 =total_score2/total_count

print("\n 처리 결과\n")
print(f"전체 학생 수 : {total_count}\n")
print(f"score1 총합: {total_score1}, 평균{average_chunk1:3f}\n")
print(f"score2 총합: {total_score2}, 평균{average_chunk2:3f}\n")
print(f"전체 한버네 처리 시간: {time_all:7f}초\n")
print(f"chunk로 처리한 총 시간: {time_chunk_total:7f}초\n")

# 청크 처리 시간 시각화

#pip install koreanize-matplotlib
import koreanize_matplotlib
import matplotlib.pyplot as plt

labels = ['전체 한번에 처리','청크로 처리']
times=[time_all,time_chunk_total]
plt.figure(figsize=(6,4))
bars=plt.bar(labels,times,color=['skyblue','red'])

for bar,time_val in zip(bars,times):
    plt.text(bar.get_x()+bar.get_width()/2,\
             bar.get_height(),f'{time_val:3f}초',\
                ha='center',va='bottom',fontsize=10)
    
plt.ylabel('처리시간(초)')
plt.grid(linestyle='--')
plt.tight_layout()
plt.show()