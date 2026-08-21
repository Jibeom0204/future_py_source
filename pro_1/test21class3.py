"""
메서드
멤버
모듈 
필드
멤버 변수 지역변수 전역변수 ;;

의미 정리
"""

kor = 100 # 모듈의 멤버변수 = 전역변수

# def __init__(self) #- 초기화 작업이 없는 경우 생성자는 생략가능
#    pass
#초기화 작업이 있는경우는 어떤거지?

def abc():
    kor = 0 #abc 함수 내의 지역변수
    print('모듈의 멤버 함수')

class My:
    kor =80 # My클래스 멤버 변수 ('My'라는 type의 객체 공유자원)

    def abc(self):
        print('My 클래스 멤버 메서드 : ')

    def show(self):
        # kor =77 # 메소드 내의 지역 변수
        print(kor) #만약 윗줄의 kor를 주석하면 찾을 수 없어서 모듈의 멤버로 찾으러 감
        # 지역 변수를 찾다가 없으면 모듈 멤버로 간다
        print(self.kor) ##이거는 원래 myObj에서 찾아야 하는데 없음 -> 그럼 원형 가서 찾음
        abc() # 모듈의 멤버인 abc()함수를 호출 #16줄로 감
        self.abc # 클래스의 abc인 23줄로 가서 호출

print()
print('========myObj1========')
myObj1 = My() # 생성자 호출 
myObj1.show() #Bond message call ==> myObj.show() 이렇게 하면 앞에 myObj1이 show()의 ()안에 self로 인식되어 들어가서 호출

print()
print('========myObj2========')
myObj2 = My()
print(myObj2.kor) # .으로 class의 멤버를 호출해서 클래스의 변수 kor에 잡힌 80가져오기? (Y)
# 클래스 안에 있는 함수를 메서드라고 부름 () 있는거 -> 얘는 꼭 self가 필요하다-> 왜? 주소를 가져와야 하니까 ㅇㅇ
myObj2.kor =99 # 새로운 걸로 초기화
print("myObj2.kor를 99로 초기화 하고 새롭게 출력")
print(myObj2.kor)

print()
print('========myObj3========')
myObj3 = My()
print(myObj3.kor)

##################################################
##################################################

