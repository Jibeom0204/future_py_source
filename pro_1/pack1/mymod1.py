"""
pack1/mymod1.py

여기서는 변수, 함수를 가짐
실행은 안함
"""

tot = 123

def listHap(*ar):
    print(ar)
    if __name__ == '__main__':
        print("나는 메인모듈이다")

def kbsF():#이거로는 실행이 안됨
    print('1박 2일')

def mbcF():#이거로는 실행이 안됨
    print("무한도전")