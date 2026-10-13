"""
* numpy의 array() 관련 연습문제 *

1) step1 : array 관련 문제
 정규분포를 따르는 난수를 이용하여 5행 4열 구조의 다차원 배열 객체를 생성하고, 각 행 단위로 합계, 최댓값을 구하시오.

< 출력 결과 예시>
1행 합계   : 0.8621332497162859
1행 최댓값 : 0.3422690004932227
2행 합계   : -1.5039264306910727
2행 최댓값 : 0.44626169669315
3행 합계   : 2.2852559938172514
3행 최댓값 : 1.5507574553572447
"""

import numpy as np
np.random.seed(42) # 난수의 42번 인덱스로 고정
data=np.random.randn(5,4) # 정규분포 함수 randn()
print(data,"\n")

i=1
for row in data:
    print('행 합계 : ', np.sum(row)) # row.sum(). 이렇게도 가능
    print('행 최대값 : ', np.max(row))
    i+=1

print()
for a in data.sum(axis=1): # 행합계만 출력
    print(a)
print("=====================================================================")

"""
2) step2 : indexing 관련문제

 문2-1) 6행 6열의 다차원 zero 행렬 객체를 생성한 후 다음과 같이 indexing 하시오.

   조건1> 36개의 셀에 1~36까지 정수 채우기
   조건2> 2번째 행 전체 원소 출력하기 
              출력 결과 : [ 7.   8.   9.  10.  11.  12.]
   조건3> 5번째 열 전체 원소 출력하기
              출력결과 : [ 5. 11. 17. 23. 29. 35.]
   조건4> 15~29 까지 아래 처럼 출력하기
              출력결과 : 
              [[15.  16.  17.]
              [21.  22.  23]
              [27.  28.  29.]]
"""
zarr=np.zeros((6,6)) #zeros((6,6) 6*6의 0 행렬
print(zarr,"\n")
cnt=0
for i in range(6):
    for j in range(6):
        cnt +=1
        zarr[i,j] =cnt

print(zarr,"\n")
print(zarr[1,:],"\n") # zarr[1]과 같다 0,1,2, 순서 중 1, 즉 2번째
print(zarr[:,4],"\n")
print(zarr[2:5,2:5],"\n")
print("=====================================================================")


"""
문2-2) 6행 4열의 다차원 zero 행렬 객체를 생성한 후 아래와 같이 처리하시오.
     조건1> 20~100 사이의 난수 정수를 6개 발생시켜 각 행의 시작열에 난수 정수를 저장하고, 두 번째 열부터는 1씩 증가시켜 원소 저장하기
     조건2> 첫 번째 행에 1000, 마지막 행에 6000으로 요소값 수정하기

<<출력 예시>>
1. zero 다차원 배열 객체
  [[ 0.  0.  0.  0.]
        ...
   [ 0.  0.  0.  0.]]

"""
zarr2=np.zeros((6,4))
print(zarr2,"\n")

ran=np.random.randint(20,100,6) # 17번줄 np.random.seed(42)로 모든 random으로 생기는 것은 고정된다
print(ran,"\n")
ran=list(ran) #[81 81 66 81 70 74]
for row in range(len(zarr2)):
    num=ran.pop(0)
    for cal in range(len(zarr2[0])):
        zarr2[row,cal]=num

print(zarr2,"\n")
zarr2[0][:] =1000
zarr2[-1][:] =6000
print(zarr2,"\n")
print("=====================================================================")

"""
step3 : unifunc 관련문제
  표준정규분포를 따르는 난수를 이용하여 4행 5열 구조의 다차원 배열을 생성한 후
  아래와 같이 넘파이 내장함수(유니버설 함수)를 이용하여 기술통계량을 구하시오.
  배열 요소의 누적합을 출력하시오.

<<출력 예시>>
~ 4행 5열 다차원 배열 ~
[[ 0.56886895  2.27871787 -0.20665035 -1.67593523 -0.54286047]
           ...
 [ 0.05807754  0.63466469 -0.90317403  0.11848534  1.26334224]]
 """
arr3=np.random.randn(4,5)
print("4,5 형태 정규분포 arr3: ",arr3,"\n")
print("기술 통계량 ========")
print("평균: ",np.mean(arr3),"\n") # np.mean(arr3) == arr3.mean(). 동일한 기능 다른 코드
print("합계: ",np.sum(arr3),"\n")
print("표준편차: ",np.std(arr3),"\n")
print("분산: ",np.var(arr3),"\n")
print("최대값: ",np.max(arr3),"\n")
print("최소값: ",np.min(arr3),"\n")

print("1사분위 수: ",np.percentile(arr3,25),"\n")
print("2사분위 수: ",np.percentile(arr3,50),"\n")
print("3사분위 수: ",np.percentile(arr3,75),"\n")
print("누적합: \n",np.cumsum(arr3),"\n")
print("=====================================================================")

# numpy 문제 추가 ~~~~~~~~~~~~~~~~~~~~~

# Q1) 브로드캐스팅과 조건 연산 -> numpy에서 브로드 캐스팅 정의 정리
# 다음 두 배열이 있을 때,
a = np.array([[1], [2], [3]])
b = np.array([10, 20, 30])
# 두 배열을 브로드캐스팅하여 곱한 결과를 출력하시오.
# 그 결과에서 값이 30 이상인 요소만 골라 출력하시오.
result=a*b
print('result: \n',result,"\n")
print("곱 결과가 30 이상: ",result[result>=30],"\n") #곱 결과가 30 이상:  [30 40 60 30 60 90] 
print("=====================================================================")

# Q2) 다차원 배열 슬라이싱 및 재배열
#  - 3×4 크기의 배열을 만들고 (reshape 사용),  
#  - 2번째 행 전체 출력
#  - 1번째 열 전체 출력
#  - 배열을 (4, 3) 형태로 reshape
#  - reshape한 배열을 flatten() 함수를 사용하여 1차원 배열로 만들기
arr=np.arange(1,13).reshape(3,4) #1,12를 쓰면 안되는 이유?
print("3*4 arr",arr,"\n")
print("arr[1], 1번 인덱스=2행: ",arr[1],"\n")
print("arr[:,0], 1번째 열 전체: ",arr[:,0],"\n")
resh=arr.reshape(4,3)
print("리쉐입한 결과: \n",resh,"\n")
#flat=resh.flatten() # 차원 한단계 격하 : 4차원 -> 3차원        3차원 -> 2차원      2차원 -> 1차원
flat=resh.ravel() # 기능은 비슷한데 복사본을 만드냐 안만드냐 차이 -> flatten은 무조건 복사본을 만듬. 원본에 영향을 주지 않음
# ravel은 복사본을 만들지 않음, 원본에 영향을 미칠 수 있음. 복사본이 없기에 메모리 관리 관점에서는 효율적
print("격하된 차원 출력: ",flat) #격하된 차원 출력:  [ 1  2  3  4  5  6  7  8  9 10 11 12]
print("=====================================================================")

# Q3) 1부터 100까지의 수로 구성된 배열에서 3의 배수이면서 5의 배수가 아닌 값만 추출하시오.
# 그런 값들을 모두 제곱한 배열을 만들고 출력하시오.
arr=np.arange(1,101) # arrange(시작, 마지막, 증감). 증감 안쓰면 1로 자동지정
imsi = (arr%3==0)&(arr%5!=0)
print("조건 연산자로 연산된 imsi: \n",imsi,"\n")
filtered=arr[imsi]
print("배열값으로 연산된 imsi: \n",filtered,"\n")
squ=filtered*2
print(squ)
print("=====================================================================")

# Q4) 다음과 같은 배열이 있다고 할 때,
# arr = np.array([15, 22, 8, 19, 31, 4])
# 값이 10 이상이면 'High', 그렇지 않으면 'Low'라는 문자열 배열로 변환하시오.
# 값이 20 이상인 요소만 -1로 바꾼 새로운 배열을 만들어 출력하시오. (원본은 유지)
# 힌트: np.where(), np.copy()
labels=np.where(arr>=10,'hihg','low')
print("labels 출력: \n",labels,"\n")
new_arr=np.copy(arr)
new_arr[new_arr>=20]=-1
print("new_arr 출력: \n" ,new_arr,"\n")
print("=====================================================================")

# Q5) 정규분포(평균 50, 표준편차 10)를 따르는 난수 1000개를 만들고, 상위 5% 값만 출력하세요.
# 힌트 :  np.random.normal(), np.percentile()
data=np.random.normal(loc=50,scale=10,size=1000)
# normal 사용법: (loc: float = 0, scale: float = 1, size: None = None) -> float
# loc : float or array_like of floats
# Mean ("centre") of the distribution.
print(data)
print(data.mean(),"\n")#50.528573261725285
threshold=np.percentile(data,95)
top5=data[data>threshold] #top5변수에 threshold 보다 큰 data를 저장
print("상위 5% 출력: \n",top5,"\n")