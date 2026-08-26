"""
예외처리: 파일, 네트웤, Db작업, 실행 오류 등의 에러에 대처
try ~except는 프로그램 실행 중 발생할 수 있는 오류(exception)를 처리해서 프로그램이 갑자기 종료되지 않도록 하는 문법

try에는 오류가 발생할 가능서이 있는 코드를 작성하고 excpet에는 해당 오류가 발생했을 때 어떻게 처리할지를 작성한다

try:
    실행할 코드
    ...
except 예외종류:
    오류 처리 코드

finally:
    오류 유무와 상관없이 처리할 구문(반드시 실행할 코드)
"""

def divideFunc(a,b):
    return a/b



try:
    #실행문 처리 블럭(오류 가능 영역)
    #c=divideFunc(5,2)#지금은 정적으로 우리가 입력해 놓지만 실제로는 동적으로 다른 사용자들이 이상한 값을 넣었을 때 처리됨
    # c=divideFunc(5,1)
    # print(c)
    # print('계속')
    aa=[1,2]
    print(aa[0])
    #print(aa[3]) # 인덱스 에러가 발생하지만 예외처리 하지 않으면 인덱스 에러라고 표기되면서 프로그램이 끝남
    #이거에 해당하는 except를 따로 처리해줘야함

    #파일 읽기
    open('c: /work/ok.txt')

###보조기억장치에 저장할 때는 무조건 파일 단위

except ZeroDivisionError:
    #에러 발생 시 처리 영역
    print('두번째 값은 0을주면 안돼요')
except IndexError as err:
    print('참조 범위 오류: ', err)
except Exception as e: #발생한 일반적인 예외를 한버에 받아서 처리할 때 사용
    # 여러 예외를 포괄적으로 처리
    print('에러 : ', e)
finally:
    print('에러 유무에 상관없이 반드시 수행됨')

print('프로그램 종료')

