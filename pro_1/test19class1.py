"""
oop: 객체지향(객체중심)적인 프로그래밍 가능 -> 상속 포함, 다형성등의 기법을 구사 가능
class: 멤버변수(멤버필드), 멤버 메소드로 구성됨
인스턴스에 의해 새로운 이름 공간을 갖는다
def a()로 선언하고
실제 실행은 a() 하는거랑 비슷한가?

"""
import math #모듈
a=2 #전역변수
print('a값: ',a) #실행문

def func(): #함수
    print('ok')

class TestClass:  #클래스의 Header 소문자로 써도 됨->그러나 대문자로 하는게 사회적 합의

    ## 아래로는 클래스의 Body
    aa=1 #멤버변수 #멤버에서만 사용가능?(Y/N) #현재 클래스 내에서 전역변수

    def __init__(self): #특별 메서드 #메소드의 첫 인자(parameter)는 "반드시" "self"
        print("__init__(self):==생성자==객체 생성시 가장 먼저 1회만 호출 - 초기화담당")

    def __del__(self): #특별 메서드
        print("__del__(self)==소멸자==프로그램 종료시 자동 실행 - 마무리 작업")

    def showMessage(self): #일반 메서드
        name1='한국인' #지역변수:showMessage안에서만 유효 -> 다른 곳에서 못씀
        name2="미국인" #지역변수:showMessage안에서만 유효 -> 다른 곳에서 못씀
        print(name1)
        print(name2)
        print(self.aa)
        #메서드는 행위
print()
print(TestClass) #<class '__main__.TestClass'>
print()

print('클래스 멤버 a ==',TestClass.aa) #클래스 멤버 a:1
# TestClass.showMessage #만들때 오류 안남->런타임에러 ##만들 때 에러남=신텍스 에러
# #이렇게 안만든다

print()
test = TestClass() # 생성자 호출 => instance를 하다 => Object(객체)가 만들어진다
# 맨 처음 실행해서 def_-init__을 호출한다
# TestClass() 하면 def __init__(self) 실행됨
# 클래스 생성자를 이용해 객체 생성후 해당 객체의 주소를 객체변수에 치환
# test에 TestClass의 주소를 저장
print('클래스 멤버 a: ',test.aa)
# print(f'test.showMessage()의 결과 출력 == ',test.showMessage())

print()

# Bound Method call - 자동으로 인수로 들어가는 방식
test.showMessage()
#위에서 만들어진 test가 ()안에 자동으로 들어감 -> test가 메소드의 인수로 담겨 호출됨
#로직은 test.showMessage(test) 이런 형식임. 실제로 이러면 안됨 두번 호출해서 오류남

# UnBound Method call - 주소를 다른 곳에 저장해서 직접 저장
TestClass.showMessage(test)
#39줄 주석과 달리 이거는 가능 왜냐? 43번 줄에서 test=TestClass()를 통해 test에 주소가 생겼기 때문  
#그럼에도 이렇게 쓰지는 않음

#함수와 클래스의 차이
#함수는 ()에self가 없음

###############################################
print('================================')
print(type(1)) #실행결과: <class 'int'>
print(type(1.0))#실행결과: <class 'float'>
print(type('ok'))#실행결과: <class 'str'>   
# 여기까지는 이미 원래 존재하던것

print(type(test))
#실행결과: <class '__main__.TestClass'> test타입())이라는 클래스는 사용자가 직접 만들어준 것
#타입이라는 속성과 행위가 같이 있는 것이 클래스
print(id(test)) #실행결과: 2721694584512  # 이 주소는 실행할 때마다 바뀜
print(id(TestClass)) #실행결과: 2721696722496
test2=TestClass() #실행결과: __init__(self):==생성자==객체 생성시 가장 먼저 1회만 호출 - 초기화담당
#test2라는 객체를 한개더 생성. 변수명에 클래스를 담아 호출하면 된다

print(id(test2))#실행결과: 2721694486672 #76번째 줄과는 다른 객체, 주소가 다름
print('================================')
###############################################