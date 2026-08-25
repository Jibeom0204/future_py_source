"""
클래스의 다중 상속 : 부모 클래스가 복수(순서에 유의)

"""

class Tiger:
    data = "호랑이 세상"

    def cry(self):
        print("호랑이 울음소리")

    def eat(self):
        print("맹수는 육식동물")
        print("아침에 닭고기, 점심에 소고기, 저녁에 양고기")

class Lion():
    def cry(self):
        print('사자 울음소리')

    def hobby(self):
        print("백수의 왕은 낮잠이 취미")


class Liger1(Tiger,Lion): # 자식 클래스
    pass

a1=Liger1()
print()
print('=====a1.date확인=====')
print(a1.data)

print()
print('===내부 메서드 확인===')
a1.eat()
a1.hobby()
a1.cry() # 동일멤버인 경우 첫번째 클래스의 멤버를 취함 => 첫번째로 상속 받는게 Tiger라서 호랑이 울음소리 받아옴

print("#######################순서 바꾸기#######################")


def hobby():
    print("모듈의 멤버인 일반함수 hobby") #모듈은 기능을 하는 하나의 파일로 보셈

class Liger2(Lion, Tiger):
    data = "라이거 만세"

    def play(self):
        print("라이거의 공유 메서드 ==> play")

    def hobby(self): #Lion()클래스의 오버라이딩
        print("라이거의 취미는 공원산책하는거임  ==> 오버라이딩")

    def showData(self):
        print()
        print("=====self.hobby() 확인=====")
        self.hobby() #Liger()로 형성된 객체x를 self로 받은 x.hobby 메서드

        print()
        print("=====super().hobby() 확인=====")
        super().hobby() #Tiger()에는 없고 Lion()에서만 있는 부모의 메서드

        print()
        print("=====hobby() 확인=====")
        hobby() #클래스에 포함 되지 않는 외부 모듈에서 호출 // function()

        print()
        print("=====self.eat()확인=====")
        self.eat()

        print()
        print("=====super().eat()확인=====")
        super().eat()

        print(f"data 출력: {self.data}, super.data 출력{super().data}")

a2=Liger2()
a2.cry()
a2.showData()