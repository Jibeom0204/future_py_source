###################################################################
####재귀함수####
#재귀 (Recursion) : 문제를 더 작은 문제로 나눔, 각 호출마다 새 함수 스택 생성
"""
재귀함수: 함수가 자기 자신을 호출 - 반복 처리 가능
장단점:
"""

def countDown(n):
    if n==0:
        print('완료')
        return
    else:
        print(n,end = ' ')
        countDown(n-1) # 여기서 자기 함수를 다시 호출하는 거임

countDown(5)
#실행 흐름:  print_num(5)  → print_num(4)   → print_num(3)    → ...    → print_num(0) 종료

print('')

print('========1부터 n까지 정수 합========')
def totF(n): # result 쪽에서 받은 값을 가지고 함수 시작 if 문의 n==0과 비교
    if n==0:
        print('완료')
        return 1
    return n + totF(n-1)
result = totF(100) #이 숫자를 가지고  위로 보냄

print('result 값: ',result)
#함수가 재귀를 했을 때, 즉 5에서 4로, 4에서 3으로, 3에서 2로 진행되는 과정에서는 계산하지 않는다 그저 단계별로 호출하고 최종 단계에서 거슬러 올라가면서 계산한다.
# #############이 개념 AI 돌리면서 좀 더 공부하자!!################
#함수가 시작돌 때 독립적인 공간을 지니기 때문에.
#독립적인 메모리를 차지해서 과하게 사용시 시스템이 멈춘다



########################
## 팩토리얼##
print('팩토리얼 구하기')

def facto(a):
    if a ==1:
        return 1
    print(a)
    return a * facto(a-1)

result2 =facto(5) # 5팩토리얼
print('result2 결과: ', result2)   # 흐름 그림으로 그려보기