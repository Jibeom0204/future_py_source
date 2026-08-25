"""
다중 상속
"""

class Animal: #최상위 클래스
    def move(self):
        print("동물은 움직인다")
        print()

class Dog(Animal): #Animal에서 move() 받아오기
    def __init__(self,name):
        print(f"나는 {name} 이다.")
        self.name=name

    def move(self):#Animal() 클래스의 move()메서드와 이름만 갖고 기능은 다른 오버라이딩
        print("개는 기분 좋으면 꼬리를 흔든다")

    def showData(self):
            print("==========개 소개하기==========")
            print(self.name)
            self.move()
            print()

class Cat(Animal): #Animal에서 move() 받아오기
    def __init__(self,name):
        print(f"나는 {name} 이다.")
        self.name=name

    def move(self):#Animal() 클래스의 move()메서드와 이름만 갖고 기능은 다른 오버라이딩
        print("고양이는 그루밍을 한다")

    def showData(self):
        print("==========고양이 소개하기==========")
        print(self.name) #print(self.name()) 이렇게 써서 TypeError: 'str' object is not callable 알람뜸 name()에서 ()지우기
        self.move()
        print()

class Wolf(Dog, Cat):
    def cha(self):
        print("늑대는 개과 동물")

    def showData(self):
        print("==========늑대 소개하기==========")
        self.cha()
        print("==========늑대의 move()는?==========") #Dog()로 나올거임
        super().move()
        print()

class Fox(Cat,Dog):
    def foxMethod(self):
        print("아리는 꼬리가 9개")
        
    def showData(self):
        print("\n==========Fox()의 고유 FoxMethod==========")
        self.foxMethod()

        print("\n==========Fox의 상위 클래스 Cat의 움직임==========")
        super().move()
        print()

if __name__ =="__main__":

    #각 객체 생성완료
    a=Animal()
    d=Dog("개")
    c=Cat("고양이")
    w=Wolf("늑대")
    f=Fox("여우")

    #각 객체 별 소개
    Animal().move()  # 클래스의 이름으로 멤버를 호출 오우 이 설명이 술술나오네
    d.showData()
    c.showData()
    w.showData()
    f.showData()
