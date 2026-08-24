"""
여러개의 부품 객체를 조립해 완성차 생성
클래스의포함 관계 사용 = 자원의 재활용
포함 관계 : 다른 클래스(객체)를 마치 자신의 멤버처럼 선언하고 사용
"""

import test24PohamHandle # 를 써서 다른 클래스 호출  
from test24PohamHandle import PohamHandle

class PohamCar:
    turnShowMessage="정지" # PohamCar의 고유 멤버

    def __init__(self, ownerName): #오너네임은 여기서만씀
        self.ownerName=ownerName
        self.handle = PohamHandle() # 이 안에서 선언한 handle에 외부 클래스의 값을 받아옴. 포함관계(has a)

    def turnHandle(self,q):
        #회전량(q): 회전량(q): 양수면 우회전, 회전량(q): 음수면 좌회전, 0이면 직진이라고 가정
        if q>0:
            self.turnShowMessage=self.handle.rightTurn(q) ### 보통 self."멤버"로 호출하는데 포함은 self."멤버".다른 클래스에서 받아올 값 이렇게 씀
            #양수면 정지였던 turnShowMessage가 위에서 불러온 PohamHandle안에 선언된 rightTurn값을 받아 저장

              #turnShowMessage=self.handle.rightTurn(q) # self.turnShowMessage안하면 어케됨??
        elif q<0:
            self.turnShowMessage=self.handle.leftTurn(q)
        elif q==0:
            self.turnShowMessage="직진"


if __name__ == "__main__":
    tom =PohamCar("톰") # pohamCar의 틀로 tom이 생성됨 #owner name으로 들어감 tom이 self로 들어감 -> self.ownerName=ownerName도 톰, self.handel = PohamHandle()도 톰
    tom.turnHandle(10) #turnHandle의 q값으로 들어감 -> right or left trun의q로 들어감 -> self.quantity=quantity에 들어감
    #여기서 self의 기능은? => 톰.턴핸들해서 self로 들어감->이거 맞음?
    print(tom.ownerName + '의 회전량은'+ tom.turnShowMessage +" "+ str(tom.handle.quantity))

    print()
    alex =PohamCar("알렉스") 
    alex.turnHandle(-20) 
    print(alex.ownerName + '의 회전량은'+ alex.turnShowMessage +" "+ str(alex.handle.quantity)) #str(alex.handle.quantity) 이거는 뭐임?
    #직진
    print()
    alex.turnHandle(0) 
    print(alex.ownerName + '의 회전량은'+ alex.turnShowMessage +" 0 ")