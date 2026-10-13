# 배열 연산
# 기본 수학함수는 배열에 요소별로 적용되고,
# +,-,*,/나 또는 add, substract, multyply,divide 함수를 사용
# 벡터화 연산을 하므로 for 문을 사용하지 않고 바로 배열에 대한 연산 가능
import numpy as np
x=np.array([[1,2],[3,4]]) # 기본 자료형인 int로 출력
print("\nx=[[1,2],[3,4]]: \n",x, ' ',x.dtype) 

x=np.array([[1,2],[3,4]],dtype=np.float32) # 정수를 실수처럼 변환시킴
print("\nx=[[1,2],[3,4]],dtype=np.float32 타입 변경:\n",x, ' ',x.dtype)

x=np.array([[1.,2],[3,4]]) # float이 int 보다 상위 타입이기 때문에 하나만 실수로 인식 시켜도 모든 값이 바뀐다
print("\nx=[[1.,2],[3,4]] 하나만 실수로 변경-> 전체 실수로 변경: \n",x, ' ',x.dtype)
print("\n========================\n")

y=np.arange(5,9) #[5,6,7,8] int 64 1차원 배열 생성
print("5~9 1차원 배열 생성: \n",y, ' ',y.dtype)

y=np.arange(5,9).reshape(2,2) #구조 변경. 1차원을 2차원으로 변경
print("\n1차원 배열을 2차원으로 변경: \n",y, ' ',y.dtype)

y=y.astype(np.float32) # type 변경
print("\n타입 변경: \n",y, ' ',y.dtype) # [[5.6.][7.8.]]
print("\n.ndim써서 차원 확인: \n", "x 차원: ",x.ndim ,' ', "y 차원: ",y.ndim) 

print("\n========================\n")
print("더하기:\n",x+y) # 파이썬 연산자 사용
print("np.add더하기\n",np.add(x,y))# 넘파이 함수(유니버셜 함수) -위 보다 연산 속도 빠름

print("\n빼기:\n",x-y) # 파이썬 연산자 사용print("\n")
print("np.subtrac빼기:\n",np.subtract(x,y))

print("\n곱하기\n",x*y) # 파이썬 연산자 사용print("\n")
print("np.multiply곱하기:\n",np.multiply(x,y))

print("\n나누기\n",x/y) # 파이썬 연산자 사용print("\n")
print("np.divide나누기:\n",np.divide(x,y))

print()
print(np.sqrt(x),'',np.exp(x), '', np.log(x),'', np.cos(x))

print("================================================================")

## 내적의 합 구하기
print("\n내적 : dot()_은 모듈의 함수나 배열 객체의 인스턴스 메소드로 내적 연산이 가능")
v=np.array([9,10])
w=np.array([11,12])
# 일반 곱
print("v*w: ", v*w) # 요소별 곱하기_하다마르 식 [9*11] [10*12]

# 백터의 내적(행렬곱)
print("v.dot(w): ",v.dot(w)) # 내적의 결과는 스칼라: 크기만 있고 방향은 없음 # 결과: 219
print("np.dot(v,w): ",np.dot(v,w))
# 결과: 219 = 방법1: (9*11)+(10*12)
# 방법2: a·b=|a||b|*cos
print()

# 배열 계산 함수 (axix를 지정하지 않고 집계함수를 쓰면 전체 배열을 차원을 떨어뜨림)
print(x) #x=np.array([[1.,2],[3,4]]) 2차원
print("평균, 분산:",np.mean(x), ' ', np.var(x),"\n")
print("최대, 최소:",np.max(x), ' ', np.min(x),"\n")
print(np.argmax(x), ' ', np.argmin(x),"\n") #index 반환
print("누적합:",np.cumsum(x),"\n") #누적합: [ 1.  3.  6. 10.] 
print("누적곱:",np.cumprod(x),"\n") #누적곱: [ 1.  2.  6. 24.]  => 1차원으로 표시됨

print()
names1=np.array(['tom','james','tom','oscar'])
names2=np.array(['tom','page','john'])
print("중복제거: ", np.unique(names1),"\n") 
print("중복o 교집합", np.intersect1d(names1,names2),"\n") # 교집합이지만 중복값 x
print("중복o 교집합", np.intersect1d(names1,names2,assume_unique=True),"\n") # 교집합이고 중복값 o
print("합집합", np.union1d(names1,names2),"\n")

print("\n 전치: 2차원 배열에서 행과 열의 위치를 바꿈")
print(x,"\n")
print(x.T,"\n")
print(x.transpose(),"\n")
print(x.transpose(0,1),"\n")

print("\n Broadcasting: 크기가 다른 배열간의 연산. 작은 배열을 여려번 반복해 큰 배열과 연산")
x=np.arange(1,10).reshape(3,3)
y=np.array([1,0,-1])
print("재 선언한 x: ",x,"\n")
print("재 선언한 y: ",y,"\n")
print("x+y: ",x+y,"\n")

# 배열자료 파일로 저장
np.savetxt("numpy2.txt",x) #file i/o
imsi=np.loadtxt("numpy2.txt")
print("txt 배열 출력: ",imsi,"\n")