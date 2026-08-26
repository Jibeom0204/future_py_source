"""
추상 클래스(abstract class)
추상 메소드를 가진 클래스를 추상 클래스라고 하며
얘는 인스턴스 할 수 없다 = 객체 생성 불가
오직 부모클래스로만 사용 됨
추상 클래스는 직접 객체를 만들려고 존재하는 클래스가 아니라
자식 클래스들이 반드시 지켜야 할 공통 규칙을 정하는 클래스이다
추상 클래스 = 자식 클래스에게 규칙을 강제(메서드 오버라이딩)하는 부모 클래스

파이썬은 함수 중심_함수: 성격이 비스한 것들을 하나로 묶자
계속해서 반복되는 내용은 단위 프로그램으로 만들자 = 클래스 => 새로운 타입을 만들 수 있는 설계도 (속성과 행위를 포함)
만들어진 어떤 객체서 작동하는지를 알 수 있게끔 self.로 알 수 있게함
생성자는 초기화만 하는 작업, 너무 많은 코드를 작성하지 않는게 좋음 = > 별도의 메소드, 객체변수를 사용하기

메서드 오버라이드라 원활히 이뤄지지 않아 다형성이 구현되지 않았을 때 추상 클래스를 선언하면 인스턴스,즉 객체 생성을 불가하게 하면
반드시 추상 클래스의 메서드를 오버라이딩 해야함
"""

from abc import *

class AbstractClass(metaclass =ABCMeta): #metaclass =ABCMeta 추상 클래스로 선언 #이 클래스의 이름으로는 객체 생성 불가
    @abstractmethod #이 클래스를 추상 메서드로 선언 => 추상 메서드를 가지는 클래스는 
    def abcMethod(self): #@abstractmethod 이걸로 추상 메서드의 자격을 얻음
        pass ## 메서드 안에 내용이 없다? 다른 클래스에서 오버라이딩 할 용도로 만든 부모 클래스의 메서드

    def normalMethod(self): 
        print('추상 클래스 내의 일반 메소드 : 자식 클래스에서 오버라이딩 선택')

parent=AbstractClass() # 이거 불가함 = > 추상 클래스 자체로 객체 생성이 안되기때문
#@abstractmethod 이거 주석처리하면 객체생성 가능
# metaclass =ABCMeta없어도 객체 생성 가능 
# metaclass =ABCMeta 있고 @abstractmethod 있으면 객체 생성 x
# metaclass =ABCMeta 있고 @abstractmethod 없으면 객체 생성 o
# metaclass =ABCMeta 없고 @abstractmethod 있으면 객체 생성 o
# metaclass =ABCMeta 없고 @abstractmethod 없으면 객체 생성 o
# ##TypeError: Can't instantiate abstract class AbstractClass without an implementation for abstract method 'abcMethod'


class Child1(AbstractClass):
    name = '난 어린이 1'

    def abcMethod(self):
        print("부모가 가진 추상 메소드를 재정의 - 강요 당함 ㅠㅠ")
        # 추상 부모 클래스의 추상 메서드를 오버라이딩 하지 않으면 자식 클래스도 추상클래스가 되어버리기 때문에
        # 기능을 쓰건 안쓰건 일단 오버라이딩해서 초기화 시키는 안전장치
        # 왜냐고? 자식 클래스도 추상 클래스로 변해버리면 인스턴스 할 수 없고 그럼 객체 생성이 안되기 때문이지
#c1 = Child1()
# 추상 메서드를 오버라이딩 하지 않으면 타입 에러
# Child1() 클래스는 추상클래스로 선언하지 않았지만 추상 클래스를 부모 클래스로서 상속 받아 자식 클래스도 추상 클래스가 됨
 
ch1=Child1()
print('name : ', ch1.name)
ch1.abcMethod()
ch1.normalMethod()

print()

class Child2(AbstractClass):
    def abcMethod(self): #오버라이딩을 강요당함
        # @abstractmethod #이 클래스를 추상 메서드로 선언해서 이 메서드는 반드시 오버라이딩 해야함
        #     def abcMethod(self)
        print("오버라이딩 강제당함: Child2에서 수행할 로직 장성")

    def normalMethod(self):
        print('부모의 일반 메서드를 내 의지로 오버라이딩 하여 내 마음대로 내용 변경해 사용')

    def show(self):
        print(" Child2의 고유 메서드")

ch2 = Child2()
ch2.abcMethod()
ch2.normalMethod()
ch2.show()
print()

print("====== 다형성 구현 =====")
happy= ch1
happy.abcMethod()
print()
happy=ch2
happy.abcMethod()
# 부모가 가진 추상 메소드를 재정의 - 강요 당함 ㅠㅠ
# 오버라이딩 강제당함: Child2에서 수행할 로직 장성
# hpaay로 여러 메서드를 불러옴