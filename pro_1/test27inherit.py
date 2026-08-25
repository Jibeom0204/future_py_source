"""
상속: 바원의 재활용을 목적으로 특정 클래스의 멤버를 가져다 쓰는 것
코드 재사용
확장성: 기존 클래스에 새 기능을 추가한 새로운 클래스 생성
구조적 설계: 공통 개념은 부모클래스, 구체적 내용은 자식 클래스에서 구현
다형성 구사: 메소드 오버라이딩
"""

class Animal: #동물들이 가져야 할 공통 속성과 행위를 선언
    age = 1

    def __init__(self):
        print('Animal 생성자')

    def move(self):
        print('움직이는 생물')

##상속 - Animal : 부모, 조상, super, parent, 상위 클래스
    #  - Dog : 자식, 자손, sub,child, 파생, 하위 클래스

class Dog(Animal): #Animal 부모, Dog 자녀 클래스
    def __init__(self):
        print("Dog 생성자: 이걸 통해서 객체가 생성됨 ->  self를 통해 받는건 다 얘를 통한다")
        # ani=Animal() #이렇게 하면 포함관계 클래스 이름()안에 Animal 하면 상속

    def my(self):
        print('댕댕이라고 해요')
dog1=Dog()
dog1.my()# Dog의 메서드는 만들어 놓은 init 과 my 밖에 없음  #my()는 Dog() 클래스 내에 있던 고유 멤버, 고유 메서드
# class Dog(Animal)로 Animal 클래스를 상솓ㄱ하면 Animal 클래스 내의 멤버들을 사용할 수 있다
# 아래에 age, move가 뜬다
# #멤버: 특정 영역(클래스 또는 모듈)에 소속되어 있는 모든 구성 요소를 뜻합니다. (예: 클래스의 변수와 메서드)
dog1.move()# Dog()클래스에서 먼저 move()를 찾음 -> 없으면 부모 클래스에 가서 찾는다
print('Animal  Class에서 가져온 dog1의 나이 age: ', dog1.age)
print()
dog2 =Dog()
dog2.my()
dog2.move()
print('dog2 의 age: ', dog2.age) # .으로 객체 내에 있는 멤버를 호출한다 => 아주 정확히 맞는 설명. 멤버에 대한 개념 정립 완료

##########################################
class Horese(Animal) :
    pass # 클래스 내에 멤버가 없다 => 변수, 메서드 같은게 없다

horse1 = Horese()
horse1.move()