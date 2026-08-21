"""
함수:특정 작업을 수행하는 코드의 집합
모듈: 파이썬 파일 하나에 정의된 함수 클래스 변수 실행문 등을 모아둔 것이다. 관련된 코드들을 하나의 파일로 정리한 것이 모듈
코드를 조직화 하는 수단이며 import를 통해 다른 파일에서 재사용 가능
패키지: 성격이 비슷한 여러 모듈을 디렉토리(폴더)구조로 묶어 관리하는 것
패키지로 선언하려면 __init__.py 형식으로 작성
from my_package import module1 이런 형식으로 사용

모듈: 소스코드의 재사용을 가능하게 하며 소스코드를 하나의 이름 공간으로 구분하고 관리
하나의 파일은 하나의 모듈이 된다
모듈의 멤버로 모듈 함수 클래스 변수 실행문이 있따
표준 모듈(파이썬 제공) 사용자 작성 모듈(내가 작성하는 거), 제 3자 모듈(third party, 전문가가 작성한 유료 모듈)로 구분 할 수 있다
"""


#############################################################################
#####################기본 모듈들 알아보기#####################
# print(print.__module__)
# #builtins  => 내장 모듈
# print('무슨 작업을 하다가 외부 모듈 사용하기')
# #print(sys.path) #이거는 찾을 수 없음 import sys를 해줘야함 모듈의 경로를 볼 수 있는 path는 builtin(내장 함수)가 아니라서 import 해줘야함
# import sys
# print(sys.path) #path는 키워드
# sys.exit() #괄호가 있으니 exit()은 함수

# print('종료')

# ##if 아래로 모듈을 넣을 수 있다
# q='n'
# if q =='y':
#     sys.exit() # 실행중인 프로그램의 종료
# print('종료')

# ##수학관련 모듈 읽기 해보자
# import math
# print(math.pi)
# print(math.sin(math.radians(30))) #사인 30값 출력

# ##달력 출력
# import calendar
# print('2월:',calendar.FEBRUARY)
# print('')
# print(calendar.setfirstweekday(6))
# print(calendar.prmonth(2026,8))
# del calendar # 이려면 이후에 사용 X, 메모리에서 삭제

# #시간 지연
# import time
# print('3초 휴식 중 ..')
# time.sleep(3)
# print('계속')

# ##난수(random) 출력
# import random 
# print('그냥 난수: ',random.random())
# print('int난수 주소: ',random.randint)
# print('int 난수 범위값 ',random.randint(1,100))
# print(random.randrange)
# print('randrange? ',random.randrange(1,100))


# # #import로 모듈을 통으로 가져오면 모듈명.원하는 기능 이렇게 적어야함

# print()
# ### 멤버 골라쓰기
# from random import random 
# #from으로 받아서 사용하고 싶은 것만 import하면 그냥 기능만 적으면 됨
# # 모듈내의 일부 멤버만 로딩
# print(random())

# print()

# from random import randint, randrange, choice # 모듈내의 일부 멤버만 로딩
# print("randrange: ", randrange(1,10))
# print("randint: ", randint(1,10))


# from random import * # 전체 멤버 로딩(비권장) -> 메모리 많이 잡아먹음


#############################################################################
#####################사용자 모듈 만드러 보기#####################