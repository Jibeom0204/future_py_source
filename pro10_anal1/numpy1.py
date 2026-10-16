# numpy의 ndarray는 단순한 배열이라기보다, 
# 벡터/행렬 연산도 가능한 다차원 수치 데이터 구조이다.
# 주요 특징: 
# 동일한 데이터 타입(Homogeneous), 빠른 연산 속도, 메모리 효율성

import numpy as np

# ss =['tom', 'james','oscar',1,True] # List: 여러 타입의 자료로 구현
# print("ss타입")
# print(ss,' ', type(ss),"\n") # <class 'list'>

# ss2=np.array(ss) #list 타입을  array 타입으로 변환
# print("ss2타입")
# print(ss,' ',type(ss2),"\n")

# # ['tom', 'james', 'oscar', 1, True]   <class 'list'>
# # ['tom', 'james', 'oscar', 1, True]   <class 'numpy.ndarray'>

# # 상위 타입순서: int -> float -> complex -> str
# # 메모리 비교
# li =list(range(1,10))
# print("li출력:", li)
# print("id,hex(16진수) 출력")
# print(id(li[0]),id(li[1]),hex(id(li[0])),hex(id(li[1])))
# print()

# print(li*10) # 각 요소를 10을 곱하는게 아니라 10회 반복-> 왜?
# print("--"*10)
# for i in li:
#     print(i*10, end=" ")
# print()

# print()
# num_arr =np.array(li)
# print(num_arr[0], '',num_arr[1], '',id(num_arr[0]), '',id(num_arr[1])) #index로 구분 # id가 뭐지
# #num_arr[0]: 배열 내부의 원소를 읽어서 Numpy Scalar 객체로 꺼냄
# print(num_arr*10)
# #위에거는 10회 반복. 이거는 요소에 곱하기 10
# print("\n\n")


# print("======배열출력======")
# b1=np.array([1,2,3])
# print(b1,b1.shape)
# b2=np.array([[1,2,3],[4,5,6]]) # 파이썬 배열의 중첩리스트를 이차원 배열함
# print(b2,b2.shape) #[[1 2 3]
#                     #[4 5 6]] (2, 3) 2행 3열짜리 배열
# print()
# print("요소 꺼내보기")
# print(b2[0], ' ', b2[[0]], ' ', b2[0,0])
# # #요소 꺼내보기
# # #[1 2 3]   [[1 2 3]]   1
# # b2[0] = 0행 나와라= 1차원 배열만 나타냄
# # b2[[0]] = 2차원 유지 =>  1차원 2차원 배열 나타냄
# # b2[0,0] = 0행의 0렬 나오기

# print()
# print("다른거")
# print(b2,' ', b2.shape, ' ', b2.ndim, ' ', b2.size) #(2,3) 2행 3열짜리 배열. 2 by 3,2*3로 표현
# print("\n\n")


# #배열 선언 후 자동으로 값 채우기
# print("배열 자동 채우기")
# c=np.zeros((2,2)) #zeros: 0으로 채우기 2:2 행렬 만들기
# print("c",c,"\n")
# d=np.ones((2,3)) # ones: 1로 채우기 2:3 행렬 만들기
# print("d",d,"\n")
# e=np.eye(3) # eye: -> 단위 행렬3:3 정방 행렬 만들어주기. 주대각 1
# print("e",e,"\n")

# print()
# print("rand()함수_괄호 안에 숫자는 발생 수 개수: ",np.random.rand(5)) #균등분포(0이상 1미만의 난수 발생)
# print("randn()함수_괄호 안에 숫자는 발생 수 개수: ",np.random.randn(5)) #정규분포(평균 0, 표준편차 1)
# print()

# # np.set_printoptions(threshold=np.inf) #너무 길면 ... +마지막 출력만 하는데 무시하려면 사용하는 함수
# # print("rand()함수_괄호 안에 숫자는 발생 수 개수: ",np.random.rand(5000)) 
# # print("randn()함수_괄호 안에 숫자는 발생 수 개수: ",np.random.randn(5000))

# print("\n난수 발생 후평균 구하기")
# print("np.mean:평균 구하기1: ",np.mean(np.random.rand(5000))) 
# print("np.mean:평균 구하기2: ",np.mean(np.random.randn(5000)))

# print("\n랜덤 다차원 배열")
# np.random.seed(0) #한번 발생한 난수의 값을 고정
# print(np.random.randn(2,3))

print("\n인덱싱과 슬라이싱")
aa=np.array([1,2,3,4,5]) #[]안에 {} ()를 사용할 수 있음 -> 파이썬의 리스트나 튜블이나 셋 자료를 numpy의 nd array 형태로 변환하는거임
print(aa, ' ',aa[1]) #인덱싱.  0부터 시작함. 그래서 2가 출력
print(aa[1:4]) # 1 이상 4 미만 인덱스에 해당하는 값 출력
print(aa[1:])
print(aa[0:5:1]) # 이러면 다나옴 [stat, end, step]=>[0:5:1] 0=시작 5=끝 1=증가값 
print(aa[0:5:2]) 
print(aa[-2:]) # - 붙이면 뒤에서부터 출력
print(aa[-4:-1]) 

print()
bb=aa # 주소 치환
print("aa값: ",aa)
print("bb값: ",bb)
print("aa주소값: ",id(aa),"bb주소값:",id(bb))
#aa주소값:  2710309598384 bb주소값: 2710309598384
# aa와bb의 주소를 치환해서 같은 주소 출력
bb[0]=99
print("aa값: ",aa)
print("bb값: ",bb)

print()
cc=np.copy(aa) # 복사본 별도 생성
print("aa값: ",aa)
print("cc값: ",cc)
cc[0]=77
print("aa값: ",aa)
print("cc값: ",cc)
print("aa주소값: ",id(aa),"cc주소값:",id(cc))
#aa주소값:  2710309598384 cc주소값: 2710350478672
# cc=np.copy(aa) # 복사로 하면 주소가 같지 않음

print("\n\n2차원 배열의 인덱싱과 슬라이싱")
dd=np.array([
    [1,2,3,4], #1행 4열 -> index 기준: 0행 0~3열(세로단위)
    [5,6,7,8], #2행 4열 -> index 기준: 1행 0~3열(세로단위)
    [9,10,11,12]] #3행 4열 -> index 기준: 2행 0~3열(세로단위)
)
print("2차원 배열 dd 출력: \n",dd.shape) #(3, 4) 형태의 배열
print("\n========인덱싱========\n")
print("1. dd[0] : ",dd[0]) #0번째 열 요소값 모두 출력
print("2. dd[0,0] : ",dd[0,0])
print("3. dd[2,3] : ",dd[2,3])
print("\n========슬라이싱========\n")
print("1. dd[0:2]: \n",dd[0:2]) #0행 이상 2행 미만
print("2. dd[1: ]: \n",dd[1:]) #1 행 이상 모든 행
print("3. dd[:,0]: \n",dd[:,0]) # 모든 행 0번째 열
print("4. dd[:,[1]]: \n",dd[:,[1]]) # 모든 행의 1번열을 가져오되 2차원 형태를 유지
print("5.dassdaasddasadsasddasdasadsdasd dd[1:3,1:3]: \n",dd[1:3,1:3]) # 1행 2행의 1열 2열 출력
print("6. dd[::]: \n",dd[::]) # 모든 행 모든 열 출력
print("7. dd[::2,:]: \n",dd[::2,:]) # 0행 2행 의 모든 열. 2는 step
print("8. dd[::,::2]: \n",dd[::,::2])  # 모든 행, 0열,2열 출력
print("9. dd[::2,::2]: \n",dd[::2,::2]) #0행 2행의 0열,2열 출력
print("\n========역순========\n")
print("1. dd[-1:-1]: \n",dd[-1:-1])# 마지막 행, 마지막 열값 1개 출력
print("2. dd[-1]: \n",dd[-1]) #마지막 행
print("3. dd[:,-1]: \n",dd[:,-1]) #모든 행의 마지막 열
print("4. dd[::-1]: \n",dd[::-1]) #행 역순
print("5. dd[:,::-1]: \n",dd[:,::-1])
