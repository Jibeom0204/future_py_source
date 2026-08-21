class Car:      #showData와 printHandle 두 생성자를 가짐?
    handle=1
    speed=0 #클래스 안에서 전역변수
    #여기에 있는건 다 car에 멤버

    def __init__(self,name,speed):
        self.name=name # 현재 객체의 name에게 name(지역변수) 인자값 치환
        self.speed=speed

    def showData(self):
        km="킬로미터"
        msg="속도" +str(self.speed) #그냥 speed 쓰면 안됨 위의 값을 쓰고 싶으면 self.speed
        # 문자열이랑 타입이 안 맞아서 맞춰줘야함 str()
        return msg

    def printHandle(self):
        return self.handle

print("car.handel값:")
print(Car.handle) # 원형(프로토타입) 클래스의 멤버 호출 Car 클래스의 변수(멤버)인 handle 호출
#printHandle(self): 이거를 지금 부를 수는 없음 -> 왜냐? self가 없어서..!


print()
car1 = Car('tom',10) # car1은 Car('tom',10)의 주소가 저장이 됨 
# ##################
#  def __init__(self,name,speed):
#         self.name=name # 현재 객체의 name에게 name(지역변수) 인자값 치환
#         self.speed=speed
#         self에 car1의 주소, name에 tom speed에 10 저장 #name과 speed는 지역변수

#     self.name 하면 self  때문에 새로운 객체의 주소가 생성이 됨
#       그럼 새롭게 넣는 값은 새롭게 생성된 주소를 저장하는 객체에 저장
#      self를 타고 들어와서 클래스 내에 존재하는데 실질적으로 car1, car2 등의 이름을 타고 새롭게 객채가 형성이 되니 그 객체의 멤버가 된다
#      말이 줜나게 헷갈린다
# ##################

print('car1 객체주소',car1)
print('car1 : ', car1.name, ' ', car1.speed, ' ', car1.handle)
# 클래스: . 찍으면 그 이후에 멤버 나옴
# car1.name, ' ', car1.speed, 이거는 새롭게 만든 객체 car1 안에 멤버에 저장되어 있음
# car1.handle: 애는 car1에 멤버로 없음 -> 이럴 때 프로토타입에서 호출

car1.color = '파랑' # 원형 클래스에는 존재하지 않음 그냥 따로 선언한건데 car1 객체의 성질로 들어간다
print('car1.color: ',car1.color)
print('=============================')
print('=============================')
car2 = Car('orca', 20) #생성자 호출
print('car2 객체주소',car1)
print('car2 : ', car2.name, ' ', car2.speed, ' ', car2.handle)
##################
#  def __init__(self,name,speed):
#         self.name=name # 현재 객체의 name에게 name(지역변수) 인자값 치환
#         self.speed=speed
#         self에 car2의 주소, name에 orca speed에 20 저장 #name과 speed는 지역변수 -> 지역변수라는건 car2의 변수라는건가? (Y/N)
##################
# print('car2.color: ',car2.color)
#  print('car2.color: ',car2.color)
# #                          ^^^^^^^^^^
# # AttributeError: 'Car' object has no attribute 'color'
# # 객체 속성도 없어서 원형 찾아봤는데 거기도 없음 -> 에러메시지

print(Car,car1,car2)
print("Car 클래스 주소, car1의 주소, car2의 주소")
print(id(Car),id(car1),id(car2),)
# 2430993843248 2430991683264 2430991601168

print()
print("print(car1.__dict__)로 각 객체의 멤버 확인하기")
print(car1.__dict__) #{'name': 'tom', 'speed': 10, 'color': '파랑'}
print(car2.__dict__) #{'name': 'orca', 'speed': 20}

"""여기까지 멤버에 대해서 설명함"""
########################################################

########################################################
"""메서드 설명함"""
print()
print("============메서드 설명============")
print('car1 speed: ', car1.showData()) # Bond message call ==> car1.showData() 이렇게 하면 앞에 car1이 showData()의 ()안에 들어가서 호출
print('car2 speed: ', car2.showData())

car1.speed=60 #속도 바꿔주기
car2.speed=110

print()
print("'car1.speed=60 car2.speed=110으로 속도 덮어 쓰고 새롭게 출력'")
print('car1 speed: ', car1.showData()) 
print('car2 speed: ', car2.showData())

print()
print("'car1.handle, car2.handle 출력'")
print('car1 speed: ', car1.printHandle()) #1
print('car2 speed: ', car2.printHandle()) #1

#원형 클래스 공유멤버 손대기
Car.handle =2
print()
print("'원형 클래스 공유멤버 handle 2로 수정하고 car1.handle, car2.handle 출력'")
print('car1 speed: ', car1.printHandle()) #2
print('car2 speed: ', car2.printHandle()) #2

