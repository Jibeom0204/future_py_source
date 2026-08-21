##############################
# 함수 장식자
# 정의: 새로운 함수 기존 의 함수코드를 수정하지 않고 앞뒤에 새로운 기능을 추가작업을 더해주는 파이썬의 기능
# @장식자 이름 기호를 붙여서 간단하게 사용
"""xmrwld rlsmd cnrk: dnjsfo gkatnfmf qkRnwl dksgrh tlfgod wjsngh fhrm rlfhr tlrkscmrwjd drnsjgks ghkrdlsemf wkrdjq tngod
코드 중복 줄이기: 여러 함수에서 공통으로 쓰는 기능을 하나로 묶어 재사용성을 높임
가독성 향상: @기호를 사용해 코드를 깔끔하고 직관적으로 유지한다
기본 작동원리: 장식자는 함수를 인자로 받아 내부에서 새로운 함수(보통wrapprer)를 감싸서 반환"""


# def make2(fn):
#     return lambda : "안녕" + fn()

# def make1(fn):
#     return lambda : "반가워" + fn()

# def hellofn():
#     return "고길동"

# hi=make2(make1(hellofn)) ##Deco없이 실행 
# #mk2 실행 하면서 내부에 fn()이 작동  그게 mk1  반복해서 hellofn
# print('인삿말', hi)
# print('hi주소:',hi())
# print(f'hi주소:',hi()) #왜 순서가 바뀌지?
# print(hi())

# print('\n공백\n')

# #w장식자 써보자
# @make2
# @make1
# def hellofn2():
#     return "둘리"

# print(hellofn2)
# print(hellofn2())

print('\n\n')
#다른거
def tracefn(func):
    def wrapperFunc(a,b):
        r=func(a,b)
        print(f'gkatnaud:{func.__name__} (a={a}, b={b} -> {r})') # 이 코드 수행하면 a =10 b=20 r =30 을 저장한다
        return r
    #a,b 넣고 호출하면 r이 받음
    return wrapperFunc #함수의 주소를 반환하는 클로저

@tracefn
def addFunc(a,b):
    return a+b

print(addFunc(10,20))



