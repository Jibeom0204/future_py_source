#############################################################
######## 클로저########
"""
Closure: Scope에 제약을 받지 않는 변수들을 포함하고 있는 코드 블럭이다
내부 함수의 주소를 반환해 함수 밖에서 함수 내의 멤버를 참조하기
뭔 개소리일까? 해보자
"""

## 맛보기
# def f1(a,b):
#     c=a*b
#     return c

# print(f1(2,3)) # f1에 출력하는 함수 없으니 print에 함수 자체를 넣어서 결과값 보이기

# print('\n')

# ## 변형
# def f11(a,b):
#     c=a*b
#     print('c:',c)# print를 추가해보자
#     return c

# print(f11(2,3)) # f1에 출력하는 함수 없으니 print에 함수 자체를 넣어서 결과값 보이기
# print('c:',c) # 오류난다 -> 여기서는 C를 찾을 수 없음 저 C는 f1 공간에 들어가 있는거임 그런데 밖에서 찾으니까 없음



# ## 변형
# def f2(a,b):
#     c=a*b
#     print('c:',c)# print를 추가해보자
#     return c


# kbs =f2(2,3) #함수를 실행해서 2,3,이 a,b에 대응  ## 함수 실행결과를 치환
# print(kbs) #2+3 출력

# kbs=f2  #원래 함수는 f2 (주소를 담고 있음) -> kbs 라는 이름으로 부를게 
# print(kbs) #주소값만 호출 ## 함수 주소를 치환(별명이 하나 생김)

# print(kbs(2,3))
# # c: 6 #kbs =f2(2,3)
# # 6 #print(kbs)

# # <func tion f2 at 0x000001432CA3F7F0> #print(kbs)

# # c: 6 #print(kbs(2,3))
# # 6

# print(id(f2), id(kbs))
# #2432812840944 2432812840944

# mbc=sbs=kbs  #위에서 f2를 kbs라는 이름으로 부르는데 다른 별명도 더 추가함
# del f2 #f2 함수명 삭제 참조 변수 삭제  ##메모리에서 주소를 삭제함
# # aa = f2(2,3)_ #이거는 에러 왜 애러?


# print(kbs(3,4))
# print(sbs(3,4))
# print(mbc(3,4))
 
# print('\n')

print('============클로저를 사용하지 않은 경우============')
def out():
    count =0
    def inn():
        nonlocal count
        count+=1
        return count
    print(inn())

#print(count) #불가함 out()함수 레벨에 있음 nonlocal count-> inner()안에 로컬도 아니고 글로벌도 아님 딱 out 수준

out() #out호출하고 count를 초기화 함  inner를 호출해서 결과를 전달함

print('\n\n')

print('===============클로저를 사용한 경우===============')    
def outer():
    count =0
    def inner():
        nonlocal count
        count+=1
        return count
    return inner #이게 클로저: 내부 함수의 주소를 반환함
var1=outer()
print('var1 주소',var1)
# ===============클로저를 사용한 경우===============
# var1 주소 <function outer.<locals>.inner at 0x000002204E11F950>

print('count : ',var1()) #위에서는 못한 count 호출 가능
print('count : ',var1()) #누적도 가능
print('count : ',var1())
# count :  1
# count :  2
# count :  3
#print(var1.count) #외부에서 직접 접근은 불가. 참조만 가능. #이거 다른 함수에 사용해보자
print(f'var__closure__ 기능, 클로저 내부 확인:',var1.__closure__) #__명령__ : 파이썬 고유명령
#var__closure__ 기능, 클로저 내부 확인: (<cell at 0x000001A99023B3D0: int object at 0x00007FFB1B0DE4B8>,)

# print('\n')

# myvar=var1()
# print(f'myvar 호츌: ',myvar)
# #myvar 호츌:  4

# print('\n')

# var2=outer() #새로운 객체 inner함수 생성
# print(f'inner를 새롭게 호출한 var2: ',var2())
# print(f'inner를 새롭게 호출한 var2: ',var2())
# print(f'inner를 새롭게 호출한 var2: ',var2())
# # inner를 새롭게 호출한 var2:  1
# # inner를 새롭게 호출한 var2:  2
# # inner를 새롭게 호출한 var2:  3  #위에 var1은 원래거 가져와서 4로 누적됨



##############################
# ##다른 실습
# print('수량* 단가*새ㅔ금한 결과 출력')
# def outter2(tax): #tax는 지역변수
#     def inner2(su,dan):
#         amount = su*dan*tax #su,dan은 inner의 지역변수
#         return amount
#     return inner2

# #1분기에는 금액: su*dan에 대한 tax는 0.1 부과
# q1 = outter2(0.1) #q1은 inner2의 주소를 가짐
# result1 = q1(5,50000)
# print('result1: ', result1)
# # print(f'result1: ', result1) #f 붙이고 안붙이고 무슨 차이지??
# result2 = q1(2,10000)
# print('result2: ', result2)
# # 수량* 단가*새ㅔ금한 결과 출력
# # result1:  25000.0
# # result2:  2000.0

# #2분기에는 금액: su*dan에 대한 tax는 0.05 부과
# q2=outter2(0.05)
# result3 = q2(5,50000) #inner 2의 주소를 가지고 있음
# print('result3: ', result3)
# result4 = q2(2,10000)
# print('result4: ', result4)
# # result3:  12500.0
# # result4:  1000.0


##############################
##일급함수

# print('========================일급함수========================')
# 함수를 일반적인 값이나 변수처럼 다루는 것
# 함수를 변수에 넣거나 다른 함수의 재료(인자)로 넘기거나 결과값으로 돌려받을 수 있는 성질
# 함수안에 함수, 인자로 함수 전달, 반환값이 함수임
# 주요특징
# 변수할당: 
# 인자전달:
# 반환값이용:
# 자료구조 저장:

# #반환값이 함수
# def f1(a,b):
#     return a+b
# f2=f1 #함수를 변수나 상수에 저장, 여기서는 f2라는 상수에 저장
# # F2=f1 #이러면 상수에 저장
# print(f1(1,3))
# print(f2(6,2))

# print('\n\n')
# #인자로 함수 전달
# def f3(fu):
#     def f4(): #함수 안에 함수
#         print('f3 안에 있는 내부 함수 "f4"')
#     f4() #내부함수니까 외부에서 참조 없이 호출 할 수 없음. 내부에서 바로 호출
#     return fu #반환값이 함수

# mbc=f3(f1)# 인자로 함수 전달함
# print(mbc(6,7))


# ##############################
# # 축약함수=람다함수
# print('========================축약함수=람다함수========================')
# print('=============함수 정의를 한줄로 줄여서 쓰는 익명 함수=============')
# # #프로그래밍 언어에서 여러줄의 함수 정의를 한줄로 줄여서 쓰는 익명 함수
# # #일회성, 휘발성
# # #형식  lamda 매개변수,..: 표현식 => rturn없이 결과 반환


# # #일반 함수
# # print("일반함수") #프로그램 종료시까지 메모리를 유지
# # def hapf(x,y):
# #     return x+y

# # print("일반 함수",hapf(1,2))

# # #람다로 표현하면
# # print("람다함수")
# # print("람다로 표현하면: ",(lambda x,y:x+y)(1,2)) # 단발성(휘발성) - 실행과 동시에 메모리 사라짐  #다시 부르면 또 실행됨. 실행이 안되지 않음 

# # gg = lambda x,y : x+y # 이 람다식을 gg가 기억함
# # print('gg 함수 1번 출력: ',gg)
# # print('gg 함수 2번 출력: ',gg(1,2))
# # # gg 함수 1번 출력:  <function <lambda> at 0x000001B1F464F950>
# # # gg 함수 2번 출력:  3

# # print('\n\n')

# # print('gg 휘발성?') #다시 부르면 또 실행됨. 실행이 안되지 않음  -> #호출할  때마다 모듈안에서 주소가 바뀐다
# # for i in range(3):
# #     print("gg:",gg)


# # gg2 = lambda x,y : x+y 

# # print('gg주소: ',id(gg), 'gg2 주소: ',id(gg2))
# # # print((lambda x,y : x+y) is lambda x,y : x+y ) #이거 False


# print('\n\n')
# ##############################
# # 다른 람다식

# kbs=lambda a, su=19: a+su
# print(kbs(5))
# print(kbs(5,56))
# # 24
# # 61

# print('\n')
# sbs = lambda a, *tu,**di:print (a,tu,di)
# sbs(1,2,3, var1=4, var2=5)
# # 1 (2, 3) {'var1': 4, 'var2': 5}


# print('임의의 함수에서 람다 사용하기')
# #filter()
# # 반복 가능한 객체(리스트 등)에서 특정 조건에 맞는 요소만 골라낼 수 있음
# # 기본 구조는 filter(함수, 반복 가능한 객체)

# print('5미만 뽑기: ',list(filter(lambda a: a<5,range(10)))) #range() #괄호안에 있는 수만큼 반복 가능하다
# #10까지 반복가능한 수 안에서 5미만인 수를 리스트로 뽑아라
# #[0, 1, 2, 3, 4]
# print('홀수 뽑기: ',list(filter(lambda a: a%2,range(10))))
# #10까지 반복가능한 수 안에서 홀수를 리스트로 뽑아라
# # [1, 3, 5, 7, 9]

# print(bool(0), bool(1)) #이게 print('홀수 뽑기: ',list(filter(lambda a: a%2,range(10)))) 이 코드랑 무슨 상관관계가 있지? 이거 무슨 의미냐

# #filter 사용해 1~100 사이 정수중  5의 배수이거나 7의 배수만 출력
# print('1~100 사이 정수중 5의 배수이거나 7의 배수만: ',list(filter(lambda a: a%5==0 or a%7==0,range(1,101))))
# # 파이썬에서는 && 연산자 없다. 걍 or 쓰면됨 ㅋㅋㅋ 
# #1~100 사이 정수중 5의 배수이거나 7의 배수만:  [5, 7, 10, 14, 15, 20, 21, 25, 28, 30, 35, 40, 42, 45, 49, 50, 55, 56, 60, 63, 65, 70, 75, 77, 80, 84, 85, 90, 91, 95, 98, 100]


