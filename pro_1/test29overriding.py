"""
메서드 오버라이딩 = 메서드 재정의
부모에서 정의된 메서드를 자식이 동일명의 메소드로 내용만 변경해 ㅅ요
부모 메소드의 기능을 대체하는 새ㅐ로운기능
동작의 구체화(공통 틀은 부모가, 실제 행동은 자식) 실현
Polymorphism(다형성)- 같은 메소드나 객체에 따라 다른 기능을 수행
확장, 유지 보수에 도움 - 부모 코드는 유지한 채 자식 코드만 변경
"""

class Parent: #용도: 부모 클래스
    def printData(self): #내용이 없는 메소드
        pass # 자식 클래스에서 오버라이딩을 시키기 위함

class Child1(Parent): #최상위 슈퍼 클래스인 오브젝트 하위지만 독립적임. Parent에 종속되지 않음
    def abc():
        print('Child 클래스의 고유 메소드')

    def printData(self): #Parent()클래스에서 동일 이름으로 선언된 메서드를 오버라이딩
        su =6
        a= 5+su
        print('■■■■■■■Child1에서 printData 오버라이딩■■■■■■■')

class Child2(Parent):
    good ='Excellent'

    def printData(self):
        print('◆◆◆◆◆Child2에서 printData 오버라이딩◆◆◆◆◆')
        msg = "부모와 동일 메소드 이름이지만 내용은 다르다"
        print()
        print("=====msg 출력=====")
        print(msg)

c1=Child1()
c1.printData()
print('====================')
c2=Child2()
c2.printData()

print('\n')
print("◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆다형성 구현해보기◆◆◆◆◆◆◆◆◆◆◆◆◆◆◆\n")
par=Parent()
par=c1
print()
print('=====par=c1 선언하고 par.printData() 확인=====')
par.printData()

par=c2
print()
print('=====par=c2 선언하고 par.printData() 확인=====')
par.printData()

print()
print('///////////////////////////////////////////////')
imsi =c1
print()
print('=====imsi.printData() 확인=====')
imsi.printData()

imsi = c2
print()
print('=====imsi.printData() 확인=====')
imsi.printData()
