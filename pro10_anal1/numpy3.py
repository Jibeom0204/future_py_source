"""
배열에 행,열, 추가.."""
import numpy as np

aa=np.eye(3)
print('aa:',aa,"\n")

bb=np.c_[aa, aa[2]] #파이썬에서 언더바는 대게 키워드임. aa 배열. aa[2]와 동일한 열 추가
print('bb: ',bb,"\n")

cc=np.r_[aa,[aa[2]]] # 2행과 동일한 행 추가
print('cc: ',cc,"\n")

print('append,insert,delete 함수 활용')
a=np.array([1,2,3])
print('a: ',a,"\n")
#b=np.append(a,[4,5]) # a에 4와 5를 추가해서 b 변수에 배열로 저장
b=np.append(a,[4,5],axis=0)#axis=0 ==> 행 기준 
print('b: ',b,"\n")
c=np.insert(a,0,[6,7]) # 0번째 위치에 데이터 삽입
print('c: ',c,"\n")
d=np.delete(a,1) # 1번째(인덱스) 자료 삭제.  a를 삭제하는게 아니라 a를 바탕으로 새로운 배열을 만듬
#[1,2,3]중 1번째 인덱스인 2를 삭제
print('d: ',d,"\n")

aa=np.arange(1,10).reshape(3,3)
print('aa: ',aa,"\n")
print(np.insert(aa,1,99),"\n") #1번 인덱스에 90추가.  차원이 축소됨
print(np.insert(aa,1,99,axis=0),"\n")#행 기준. 차원이 유지됨
print(np.insert(aa,1,99,axis=1),"\n")#열 기준. 차원이 유지됨
print("==========")
# 조건 연산(where: 조건, 참, 거짓)
x=np.array([1,2,3])
y=np.array([4,5,6])
conditionData=np.array([True,False,True]) 
result = np.where(conditionData,x,y) #condition이 참이면 x값 거짓이면 y값
print('result: ',result,"\n") # 뭐라노 ㅅㅂ

print("x: ",x,"\n") #
aa=np.where(x>=2)
print('aa: 2보다 큰 x만: ',aa,"\n") #조건을 만족하는 인덱스 위치를 튜플 형태로
print("a[aa]: ",a[aa],"\n") #

print("==========")
kbs=np.concatenate([x,y]) # 배열 결합
print("kbs: ",kbs,"\n") 
mbc,sbs=np.split(kbs,2) #kbs를 2개로 나눔
print("mbc: ",mbc,"\n")
print("sbs: ",sbs,"\n")
print("==========")

a=np.arange(1,17).reshape(4,4)
print("a: \n",a,"\n")
x1,x2=np.hsplit(a,2) # 열방향 분할
print("x1: \n",x1,"\n")
print("x2: \n",x2,"\n")
print(np.vsplit(a,2)) # 행방향 분할
print("==========")
# 표본 추출은 전체 데이터인 모집단에서 일부 데이터를 뽑아 조사,분석하는 것
# - 단순 무작위 추출: 전체에서 랜덤으로 추출
# - 복원 추출: 뽑은 데이터를 다시 넣고 또 뽑은 -중복 허용
# - 비복원 추출: 중복 없음
li =np.array([1,2,3,4,5,6,7])
sample1=np.random.choice(li,size=3,replace=False) # 단순 무작위 추출(비복원)
print("sample1: ",sample1,"\n")
sample2=np.random.choice(li,size=3,replace=True) # 단순 무작위 추출(복원).중복값 허용
print("sample2: ",sample2,"\n")

print()
# 복원 추출
for _ in range(5):
    print("복원 추출: ",li[np.random.randint(0,len(li)-1)],end = " ""\n")

# 비복원 추출
import random
print("비복원 추출: ",random.sample(li.tolist(),5),"\n") # random.sample은 list type을 원함