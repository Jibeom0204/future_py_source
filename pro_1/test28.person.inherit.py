"""
사람 클래스 추상 상속
"""

class Person:
    say = '난 사람이다' #접근 권한 = public
    age = '20'
    __msg = 'good: #private 멤버 --현재 클래스에서만 유효  => 다른 클래스에서는 호출할 수 없음'
    ##__변수이름  => private 선언의 규칙

    def __init__(self,age):
        print("person 생성자")
        self.age = age 
        #7줄 age = 클래스 내에서 쓸 수 있는 전역 변수 =  프로토 타입
        # =  Person()클래스를 바탕으로 생성된 Person 타입으로 생성된 객체 age가 없으면 참조하는 전역변수
        # = 20으로 고정 다른거는 변동될 수 있음
        #11줄 self.age = Person()클래스를 바탕으로 생성된 Person 타입으로 생성된 객체 주소 내에 존재하는 
        #11줄 age = 메서드 안에서만 쓸 수 있는 지역변수

    def printInfo(self):
        print(f'나이: {self.age}, 이야기: {self.say}')
        #19번줄에서 print한 self.age는 맨 처음 11번으로 생성된 self.age를 참고하고 없으면 전역변수인 Class 변수인 7번줄 age가져옴
    
    def helloMethod(self):
        print('안녕')
        print('Hello: ', self.say, self.age, self.__msg)
        

################################################################
print(Person.say, Person.age) #원형 클래스의 이름으로 멤버 호출 -> 가능하긴 한데 비권장 방법
# 설계도로 상품을 만들고 그 상품의 특성을 불러오는게 맞다
# ==> 객체를 생성하고 객체 변수의 이름으로 멤버를 가져오는게 맞다.
# 객체 변수(인스턴스 변수): 생성된 개별 객체마다 따로따로 보관하는 고유 데이터 (self.name, self.age)
#Person.printInfro() # 이건 불가능한 방법 #self를 받지 못해서 에러남
per = Person('25')
print()
print('==per.printInfo()확인==')
per.printInfo()

print()
print('==per.helloMethod()확인==')
per.helloMethod()

print()
print('===========================')
print()

#################################################################
class Employee(Person):
    subject = '근로자'
    say = "일하는 동물" #hiding(shadowing)
    # 부모 클래스, 자식 클래스에 같은 이름의 변수로 선언된 멤버가 있으면 자식 클래스, 지역 변수가 우선된다
    # 40줄에 say가 선언이 안되면 Person()클래스의 전역변수인 6번줄 say가 출력이 된다
    # 40줄에 say가 선언되면 부모 클래스의 것을 무시하고 자식 클래스, 지역 것을 먼저 가져옴 = Shadowing

    def __init__(self):
        print('Employee 생성자')

    def printInfo(self):  #메소드 오버라이딩 -> 부모 클래스와 자식 클래스에 동일한 이름의 메서드가 있을 때
        #내용이 다르면 자식 클래스의 메서드가 먼저 호출됨 -> 이걸 활용하여 다형성을 구현할 수 있음
        print('Employee 클래스의 printInfo() 호출됨')

    def ePrintInfo(self):
        print(self.subject, self.say, self.age)
       # print(self.__msg) #부모 클래스에서 선언된 private 형의 멤버를 호출 -> 문법 에러는 아니지만 실행에서 에러
        print('===self.helloMethod()===')
        self.helloMethod() # 멤버만 호출 했을 때는 불가능 => 메서드 자체를 불러왔을 때는 가능

        print()
        print('===self.printInfo()확인===')
        self.printInfo() #현재 클래스에서 먼저 호출함 55줄을 먼저 호출하는데 없으면 부모클래스의 것, 즉 20번줄 불러옴

        print()
        print('===부모 클래스의 printInfo 호출 super.printInfo()===')
        super().printInfo()# 현재 클래서 건너 뛰고 바로 부모 클래스 메서드 호출

        print()
        print('===자식클래스 say |||super().로 호출한 부모클래스 say)===')
        print(self.say, super().say)
 #################################################################       

emp =Employee() # init()에 생성자가 받을 인자를 요구하지 않음으로 Employee() 괄호에 뭐 넣을 필요없음
print("emp.subject, emp.age, emp.say",emp.subject, emp.age, emp.say)
print('================================')
print('==emp.printInfro()==')
emp.printInfo()
emp.ePrintInfo()
########################################
print('-----'*5) # - 25개 출력
class Worker(Person):
    def __init__(self, age):
        print('Worker 생성자')
        super().__init__(age) # Worker()클래스 내에서 나이를 받을 self.age = age가 없어 부모 클래스 꺼 호출함

    def wPrintInfo(self):
        print('Worker -wPrintInfo=()처리')

        print()
        print("===self.printInfo()확인===")
        self.printInfo()

        print()
        print("===super().printInfo()확인===")
        super().printInfo()

wor =Worker('30')
print()
print('===wor.say,wor.age===')
print(wor.say,wor.age)
# Worker에 30을 줬는데 20이 찍힘
# ===wor.say,wor.age===
# 난 사람이다 20
# (myproject) PS C:\wor
# 13줄의 self.age = age의 역할을 해줄 멤버가 Worker 내에 없음 어떻게 해결하냐?
# super().__init__(age) -> 부모 클래스에서 age 30을 받아줄 생성자를 호출하면 됨
#######################################################
# def __init__(self, age):
#         print('Worker 생성자')
# 이거를 pass 처리하면 30이 출력이됨

# 자식의 생성자가 있으면 자식의 생성자를 호출
# 자식의 생성자가 없으면 부모의 생성자를 호출
# Worker()의 생성자가 없으니 Person()으로 직행
wor.wPrintInfo()

############################
print("=====Worker의 자식 만들기=====")
class Programmer(Worker): #Programmer의 부모는 Worker, Worker의 부모는 Person 
    #Programmer는 super로 Worker에만 접근 가능
    #super.super 이딴거 없다
    def __init__(self, age):
        print('=====Programmer 생성자=====')
       # super().__init__(age) #Bound method call
        Worker.__init__(self,age) #Unbound method call #둘다 같은기능
        #Worker()에서 93번줄에서 super로 호출한 거를 Programmer()가 다시 호출

    def pPrintInfo(self):
        print()
        print('=====Programmer의 pPrintInfo()처리함=====')

    # def wPrintInfo(self):
    #     print('Programmer 클래스에서 Worker()클래스의 wPrintInfo를 오버라이딩 함\n 주석 처리 후 출력 해보면서 비교할 것')

#########################################################
pro=Programmer(35)
print()
print('=====pro.say,pro.age=====')
print(pro.say,pro.age)

print()
print('=====pro.pPrintInfo=====')
pro.printInfo()

print()
print('=====pro.wPrintInfo=====')
pro.wPrintInfo()
#########################################################


print('======클래스 타입 확인======')
a=3; print(type(a)) # <class 'int'> : Maker가 만든 기본 타입

print()
print('=====type(pro)확인=====')
print(type(pro))

print()
print('=====type(wor)확인=====')
print(type(wor))
## 출력
# ======클래스 타입 확인======
# <class 'int'>

# =====type(pro)확인=====
# <class '__main__.Programmer'>

# =====type(wor)확인=====
# <class '__main__.Worker'>

print("=====다른 클래스들 상위 클래스 확인=====")
print(Person.__bases__) ##(<class 'object'>,) #모든 클래스의 최상의 클래스는 objcet클래스
print(Employee.__bases__)
print(Worker.__bases__)
print(Programmer.__bases__)
